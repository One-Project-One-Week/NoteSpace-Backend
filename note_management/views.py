from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, throttle_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.validators import ValidationError
from note_management.serializers import *
from note_management.models import Note, Summary, Bookmark
from .permissions import IsNoteOwner
from .utils.summarizer.summarizer_util import get_summary_and_graph
from .utils.generator.notes_generator import generate_notes
from .utils.processor.text_extractor import extract_texts_from_files
from .utils.processor.llm_input_preprocessor import tokenize_and_split_text
from .utils.assistant.chatbot_util import use_chatbot
from .throttles import *
import traceback

class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
    
    def get_throttles(self):
        if self.action in ['generate_notes']:
            return [GenerateNotesThrottle()]
        if self.action in ['chatbot']:
            return [ChatbotThrottle()]
        if self.action in ['summarise']:
            return [GenerateNotesSummaryThrottle()]
        return []
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNoteOwner()]
        
        if self.action == "public":
            return [permissions.AllowAny()]
        
        return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        if self.action == "list":
            return Note.objects.filter(user=self.request.user)
        
        return Note.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['GET'])
    def public(self, request):
        notes = Note.objects.filter(is_public=True)
        filtered_notes = self.filter_queryset(notes)
        serializer = NoteSerializer(filtered_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["POST"])
    def bookmark(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        
        if not note.is_public:
            return Response({ "detail": "Private notes cannot be bookmarked"})
        
        if Bookmark.objects.filter(user=request.user, note=note).exists():
            Bookmark.objects.get(user=request.user, note=note).delete()
            return Response({ "code": "deleted" })
        
        Bookmark.objects.create(
            user=request.user,
            note=note
        )
        return Response({ "code": "added" })   
    
    @action(detail=True, methods=['GET'], url_path='summary')
    def summarise(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        
        # Sanitize note content
        note_content = note.sanitize_html(note.content) if note.content else ""

        try:
            # Summarize and Get Graph data
            response = get_summary_and_graph(note_content)
            
            summary, created = Summary.objects.update_or_create(
                note=note, 
                defaults={
                    "content": response['summary'],
                    "graph": response['graph']
                }
            )

            # Serialize the resulting summary object
            serializer = SummarySerializer(summary)
            
            return Response(
                {
                    "summary": serializer.data
                }
            )
            
        except Exception as err:
            return Response({
                "error": str(err),
                "type": type(err).__name__,
                "trace": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['POST'], url_path='upload', serializer_class=UploadFileSerializer)
    def generate_notes(self, request):
        
        serializer = UploadFileSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        uploaded_file = serializer.validated_data["file"]
        
        # File Size Control
        FILE_SIZE_LIMIT = 2 * 1024 * 1024
        
        if uploaded_file.size > FILE_SIZE_LIMIT:
            return Response({"error": "File exceeds 2MB limit"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            
            extracted_content = extract_texts_from_files(uploaded_file)
                
            content_chunks = tokenize_and_split_text(extracted_content)
            
            #generate notes for each chunk
            notes = [generate_notes(content=chunk) for chunk in content_chunks]
            
            #combine notes into one by a new line
            note_data = {
                "title": uploaded_file.name.split(".")[0],
                "content": "\n".join(notes),
            }
            
            serializer = NoteSerializer(data=note_data)
            
            if not serializer.is_valid():
                raise ValidationError(serializer.errors)
            
            serializer.save(user=self.request.user)
            
            return Response({"note": serializer.data["id"]})    
        
        except Exception as err:
            return Response(
                {
                    "error": f"{err}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    @action(detail=True, methods=['POST'], url_path="chat", serializer_class=ChatbotSerializer)
    def chatbot(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        serializer = ChatbotSerializer(data=request.data)

        if serializer.is_valid():
            sanitized_note_content = note.sanitize_html(note.content)
            username = request.user.username
            message = serializer.validated_data["message"]
            chat_history = serializer.validated_data.get("chat_history", [])

            try:
                chat_response = use_chatbot(
                    username=username, 
                    message=message, 
                    chat_history=chat_history, 
                    notes=sanitized_note_content
                )
                
                return Response(
                    {
                        "prompt": message, 
                        "response": chat_response
                    }, 
                    status=status.HTTP_200_OK
                )
                
            except Exception as err:
                return Response(
                    {
                        "error": f"{err}"
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )                

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'delete']
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        if self.action == "list":
            return Bookmark.objects.filter(user=self.request.user)
        
        return Bookmark.objects.all()