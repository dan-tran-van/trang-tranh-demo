from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("comic/<int:pk>", views.comic_detail, name="comic-detail"),
    path("chapter/<int:pk>", views.chapter_detail, name="chapter-detail"),
    path("chapter/<int:pk>/<str:lang>", views.chapter_translation_detail, name="chapter-translation-detail"),
]
