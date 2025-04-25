from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"notes", views.NotesViewSet, basename="notes")
router.register(r"bookmarks", views.BookmarkViewSet, basename="bookmarks")

urlpatterns = [
    path('', include(router.urls)),
]