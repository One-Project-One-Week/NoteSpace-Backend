from rest_framework import serializers
from core.models import Notes, User, Summary

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ['content']


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    Summary = SummarySerializer(read_only=True)
    
    class Meta:
        model = Notes
        fields = ['id', 'title', 'content', 'is_public', 'created_at', 'updated_at', 'user', 'summary']
        
    