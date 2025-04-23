from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from note_management.serializers import NoteSerializer
from note_management.models import Note
from .permissions import IsNoteOwner
from .utils.summarizer.summarizer_util import summarize

class NotesViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    
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
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path='summary')
    def summarise(self, request, pk=None):
        note = get_object_or_404(Note, pk=pk)
        # Summarize
        note_content = note.content if note.content else ""
        summary = summarize(note_content).strip()
        if not summary:
            return Response({"error": "Unable to generate summary."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        #Create a new summary object or Update the existing one
        #Call the function to generate a map based on this summary
        return Response(
            {
                "summary": summary
            }
        )
        
        
        
        
    
    
    
    