from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    ChapterPage,
    ChapterPageTranslation,
    Comic,
    ComicAuthor,
    ComicChapter,
    ComicChapterTranslation,
    ComicTranslation,
    User,
    UserProfile,
)

# Register your models here.

admin.site.register(User, UserAdmin)
# admin.site.register(Comic)
# admin.site.register(ComicTranslation)
# admin.site.register(ComicAuthor)
# admin.site.register(ComicChapter)
# admin.site.register(ChapterPage)
# admin.site.register(ComicChapterTranslation)
# admin.site.register(Language)
# admin.site.register(UserProfile)


class ComicTranslationInline(admin.TabularInline):
    model = ComicTranslation
    extra = 0
    show_change_link = True


class ComicChapterInline(admin.TabularInline):
    model = ComicChapter
    extra = 0
    show_change_link = True


@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "display_author",
        "publisher",
        "display_total_chapter",
        "is_valid",
    )
    list_filter = ("status", "schedule")
    search_fields = ["title"]
    inlines = [ComicTranslationInline, ComicChapterInline]


class ComicChapterTranslationInline(admin.TabularInline):
    model = ComicChapterTranslation
    extra = 0
    show_change_link = True


@admin.register(ComicTranslation)
class ComicTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "comic",
        "language",
        "is_valid",
    )
    inlines = [ComicChapterTranslationInline]


@admin.register(ComicAuthor)
class ComicAuthorAdmin(admin.ModelAdmin):
    search_fields = ["pen_name"]


class ChapterPageInline(admin.TabularInline):
    model = ChapterPage
    extra = 0
    show_change_link = True


@admin.register(ComicChapter)
class ComicChapterAdmin(admin.ModelAdmin):
    list_display = (
        "comic",
        "chapter_number",
        "chapter_counter",
        "title",
        "extra_chapter",
        "is_valid",
    )
    list_filter = ("published_date",)
    search_fields = ["title"]
    inlines = [ChapterPageInline]


@admin.register(ChapterPage)
class ChapterPageAdmin(admin.ModelAdmin):
    list_display = ("chapter", "display_chapter_counter", "page_number")
    search_fields = [
        "chapter__comic__title",
        "page_number",
        "chapter__chapter_number",
        "chapter__chapter_counter",
    ]


class ChapterPageTranslationInline(admin.TabularInline):
    model = ChapterPageTranslation
    extra = 0
    show_change_link = True


@admin.register(ComicChapterTranslation)
class ComicChapterTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "comic_translation",
        "chapter_number",
        "chapter_counter",
        "translated_title",
        "extra_chapter",
        "is_valid",
    )
    search_fields = ["translated_title"]
    list_filter = ("published_date",)
    inlines = [ChapterPageTranslationInline]


@admin.register(ChapterPageTranslation)
class ChapterPageTranslationAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
