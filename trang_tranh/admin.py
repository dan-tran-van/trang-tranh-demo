from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    ChapterPage,
    Comic,
    ComicAuthor,
    ComicChapter,
    ComicChapterTranslation,
    ComicTranslation,
    Language,
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
    list_display = ("title", "display_author", "publisher")
    list_filter = ("status", "schedule")
    search_fields = ["title"]
    inlines = [ComicTranslationInline, ComicChapterInline]


@admin.register(ComicTranslation)
class ComicTranslationAdmin(admin.ModelAdmin):
    pass


@admin.register(ComicAuthor)
class ComicAuthorAdmin(admin.ModelAdmin):
    pass


class ComicChapterTranslationInline(admin.TabularInline):
    model = ComicChapterTranslation
    extra = 0
    show_change_link = True


@admin.register(ComicChapter)
class ComicChapterAdmin(admin.ModelAdmin):
    list_display = ("comic", "title", "chapter_number")
    list_filter = ("published_date",)
    search_fields = ["title"]
    inlines = [ComicChapterTranslationInline]


@admin.register(ChapterPage)
class ChapterPageAdmin(admin.ModelAdmin):
    pass


@admin.register(ComicChapterTranslation)
class ComicChapterTranslationAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
