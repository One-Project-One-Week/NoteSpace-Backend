from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(unique=True)
    
    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)
        

class Notes(models.Model):
      
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
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
    
    note = models.OneToOneField(
        Notes,
        on_delete=models.CASCADE,
    )
    content = models.TextField()

    def __str__(self):
        return f"Summary for {self.note.title}"