from django.urls import path, include
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"notes", views.NotesViewSet, basename="notes")

bookmarkRouter = routers.DefaultRouter()
bookmarkRouter.register(r"bookmarks", views.BookmarkViewSet, basename="bookmarks")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(bookmarkRouter.urls))
]