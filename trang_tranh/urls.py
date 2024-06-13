from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("comic/<int:pk>", views.comic_detail, name="comic-detail"),
    path("chapter/<int:pk>", views.chapter_detail, name="chapter-detail"),
    path(
        "chapter/<int:pk>/<str:lang>",
        views.chapter_translation_detail,
        name="chapter-translation-detail",
    ),
    path("feed", views.feed, name="feed"),
    path("post/<int:pk>", views.post_detail, name="post-detail"),
    path("profile/<int:pk>", views.profile_detail, name="profile-detail"),
    path("notifications", views.notification, name="notifications"),
    path("settings", views.settings, name="settings"),
]
