from django.db import models
from core.models import User
from uuid import uuid4

# Create your models here.
class Note(models.Model):
      
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200, default="Untitled")
    content = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notes')
        
    def __str__(self):
        return f"{self.title} written by {self.user.username}"
    
class Summary(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    note = models.OneToOneField(
        Note,
        on_delete=models.CASCADE,
        related_name="summary"
    )
    content = models.TextField()
    graph = models.JSONField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for {self.note.title}"
    
<<<<<<< HEAD
class Bookmark(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} bookmarked {self.note.title}"
=======
    
>>>>>>> 1fea6f17b60f749ef4e634cf7e530d9431ddf3b7
