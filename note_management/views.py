from rest_framework import viewsets
from note_management.serializers import NoteSerializer
from note_management.models import Note

class NotesViewSet(viewsets.ModelViewSet):
    
    serializer_class = NoteSerializer
    def get_queryset(self):
        if self.action == "list":
            return Note.objects.filter(user=self.request.user)
        
        return Note.objects.all()
    