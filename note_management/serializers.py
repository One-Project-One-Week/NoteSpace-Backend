from note_management.models import Summary, Note
from core.serializers import UserSerializer
from rest_framework import serializers

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['content']


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    summary = SummarySerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'user', 'summary', 'title', 'content', 'is_public', 'created_at', 'updated_at']


