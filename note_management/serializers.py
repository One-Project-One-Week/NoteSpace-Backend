from note_management.models import Summary, Note, Bookmark
from core.serializers import UserSerializer
from rest_framework import serializers
import bleach

class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['content', 'graph', 'note', 'created_at', 'updated_at']
        read_only_fields = ['note', 'created_at', 'updated_at']

class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    summary = SummarySerializer(read_only=True)
    
    class Meta:
        model = Note
        fields = ['id', 'user', 'summary', 'title', 'content', 'is_public', 'created_at', 'updated_at']
    
    def validate_content(self, value):
        if value:
            allowed_tags = []
            allowed_attributes = {}
            # Sanitize the content using bleach with the custom allowed tags and attributes
            return bleach.clean(value, tags=allowed_tags, attributes=allowed_attributes)
        
class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()
    
    class Meta:
        fields = ['file']
        
    def validate_file(self, value):
        if not value.name.lower().endswith(('.txt', '.pdf')):
            raise serializers.ValidationError("File type not supported. Only .txt and .pdf files are supported at the moment.")
        return value
    
class ChatbotSerializer(serializers.Serializer):
    chat_history = serializers.ListField(required=False)
    message = serializers.CharField()
    
class BookmarkCreateSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    note = NoteSerializer(read_only=True)
    
    class Meta:
        model = Bookmark
        fields = ['id', 'note', 'user', 'created_at']
        
class BookmarkSerializer(serializers.ModelSerializer):
    note = NoteSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'note']

    def to_representation(self, instance):
        note_data = NoteSerializer(instance.note, context=self.context).data
        note_data['bookmark_id'] = instance.id  # Inject bookmark ID into the note
        return note_data