from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.validators import ValidationError
from note_management.serializers import NoteSerializer, UploadFileSerializer, SummarySerializer
from note_management.models import Note
from .permissions import IsNoteOwner
from .utils.summarizer.summarizer_util import summarize
from .utils.generator.notes_generator import generate_notes
from .utils.processor.text_extractor import extract_texts_from_files
from .utils.processor.llm_input_preprocessor import tokenize_and_split_text

class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title']
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsNoteOwner()]
        
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
    
    @action(detail=True, methods=['GET'], url_path='summary')
    def summarise(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        
        # Summarize
        note_content = note.content if note.content else ""
        summary = summarize(note_content)
        if not summary:
            return Response({"error": "Unable to generate summary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        #Create a new summary object or Update the existing one
        serializer = SummarySerializer(data={"content": summary})
        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer.save(note=note)
        
        #Call the function to generate a map based on this summary
        return Response(
            {
                "summary": summary
            }
        )
        
    @action(detail=False, methods=['POST'], url_path='upload', serializer_class=UploadFileSerializer)
    def generate_notes(self, request):
        
        serializer = UploadFileSerializer(data=request.data)
        
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        
        uploaded_file = serializer.validated_data["file"]
        
        try:
            
            extracted_content = extract_texts_from_files(uploaded_file)
                
            content_chunks = tokenize_and_split_text(extracted_content)
            
            #generate notes for each chunk
            notes = [generate_notes(model="qwen/qwen-2.5-7b-instruct:free", content=chunk) for chunk in content_chunks]
            
            #combine notes into one by a new line
            note_data = {
                "title": uploaded_file.name.split(".")[0],
                "content": "\n".join(notes),
            }
            
            serializer = NoteSerializer(data=note_data)
            
            if not serializer.is_valid():
                return Response(
                    {
                        "error": f"Error validating note data: {serializer.errors}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(user=self.request.user)
            
            return Response({"note": serializer.data["id"]})    
        
        except Exception as err:
            return Response(
                {
                    "error": f"Error occured while reading the file: {err}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )