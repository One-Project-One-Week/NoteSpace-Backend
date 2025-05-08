from django.shortcuts import get_object_or_404
from django.core.cache import cache
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
            cache_key = f"notes_ids_{self.request.user.id}"
            cached_ids = cache.get(cache_key)
            if cached_ids is not None:
                print(">>>>> From Cache: NOTE IDS <<<<<")
                return Note.objects.filter(id__in=cached_ids)
            
            queryset = Note.objects.filter(user=self.request.user)
            cached_ids = [note.id for note in queryset]
            cache.set(cache_key, cached_ids, timeout=(60 * 5))
            print(">>>>>> CACHED: NOTE IDS <<<<<<<")
            return queryset
        
        if self.action == "public":
            cache_key = "public_notes_ids"
            cached_ids = cache.get(cache_key)
            
            if cached_ids is not None:
                print(">>>>>> FROM CACHE: PUBLIC NOTES IDS <<<<<<<")
                return Note.objects.filter(id__in=cached_ids)
            
            queryset = Note.objects.filter(is_public=True)
            cached_ids = [note.id for note in queryset]
            cache.set(cache_key, cached_ids, timeout=(60 * 30))
            print(">>>>>> CACHED: PUBLIC NOTES IDS <<<<<<<")
            return queryset
        
        return Note.objects.all()
    
    def perform_create(self, serializer):
        note = serializer.save(user=self.request.user)
        cache.delete(f'notes_ids_{self.request.user.id}')
        cache.delete(f'test_notes_{self.request.user.id}')
        if note.is_public:
            cache.delete('public_notes_ids')

    def perform_update(self, serializer):
        note = serializer.save()
        cache.delete(f'notes_ids_{self.request.user.id}')
        cache.delete(f'test_notes_{self.request.user.id}')
        if note.is_public:
            cache.delete('public_notes_ids')

    def perform_destroy(self, instance):
        is_public = instance.is_public
        instance.delete()
        cache.delete(f'notes_ids_{self.request.user.id}')
        cache.delete(f'test_notes_{self.request.user.id}')
        if is_public:
            cache.delete('public_notes_ids')
        
    @action(detail=False, methods=['GET'], url_path='test')
    def test(self, request):
        #Create unique cache key
        cache_key = f"test_notes_{request.user.id}"
        
        #Check if it's cached
        cache_response = cache.get(cache_key)
        if cache_response is not None:
            print(">>>>>> FROM CACHE <<<<<<<")
            return Response(cache_response)
        
        import time
        time.sleep(2)
        notes=Note.objects.filter(user=request.user).count()
        response = {'message': f"You have {notes} notes at {time.time()}"}
        
        cache.set(cache_key, response, timeout=30)
        print(">>>>>> CACHED <<<<<<<")
        return Response(response)
    
    @action(detail=False, methods=['GET'])
    def public(self, request):
        queyrset = self.get_queryset()
        filtered_notes = self.filter_queryset(queyrset)
        serializer = NoteSerializer(filtered_notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["POST"])
    def bookmark(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        
        if not note.is_public:
            return Response({ "detail": "Private notes cannot be bookmarked"})
        
        if Bookmark.objects.filter(user=request.user, note=note).exists():
            Bookmark.objects.get(user=request.user, note=note).delete()
            cache.delete(f'bookmarks_ids_{request.user.id}')  # Invalidate cache
            print(">>>>>> CLEARED: BOOKMARKS IDS CACHE <<<<<<<")
            return Response({"code": "deleted"})
        
        Bookmark.objects.create(user=request.user, note=note)
        cache.delete(f'bookmarks_ids_{request.user.id}')  # Invalidate cache
        print(">>>>>> CLEARED: BOOKMARKS IDS CACHE <<<<<<<")
        return Response({"code": "added"})
    
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
            return Response({
                "error": str(err),
                "type": type(err).__name__,
                "trace": traceback.format_exc()
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
                return Response({
                    "error": str(err),
                    "type": type(err).__name__,
                    "trace": traceback.format_exc()
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)           

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'delete']
    serializer_class = BookmarkSerializer
    
    def get_queryset(self):
        if self.action == "list":
            cache_key = f"bookmarks_ids_{self.request.user.id}"
            cached_ids = cache.get(cache_key)
            if cached_ids is not None:
                print(">>>>>> FROM CACHE: BOOKMARKS IDS")
                return Bookmark.objects.filter(id__in=cached_ids)
            
            queryset = Bookmark.objects.filter(user=self.request.user)
            cached_ids = [bookmark.id for bookmark in queryset]
            cache.set(cache_key, cached_ids, timeout=(60 * 5))
            print(">>>>>> CACHED: BOOKMARKS IDS <<<<<")
            return queryset
        
        return Bookmark.objects.all()
        
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        cache.delete(f'bookmarks_ids_{self.request.user.id}')
        