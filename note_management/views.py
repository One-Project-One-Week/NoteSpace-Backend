from rest_framework import viewsets, permissions, status
from note_management.serializers import NoteSerializer
from note_management.models import Note
from .permissions import IsNoteOwner
from rest_framework.decorators import action
from rest_framework.response import Response

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
        
        
    
    
    
    