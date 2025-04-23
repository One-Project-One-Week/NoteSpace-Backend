from rest_framework import permissions

class IsNoteOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user