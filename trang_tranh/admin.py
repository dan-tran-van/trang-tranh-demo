from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Author,
    AuthorTranslation,
    Chapter,
    ChapterTranslation,
    Comic,
    ComicTranslation,
    Genre,
    Language,
    Page,
    PageTranslation,
    Post,
    PostMedia,
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

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    pass



class ComicTranslationInline(admin.TabularInline):
    model = ComicTranslation
    extra = 0
    show_change_link = True


class ChapterInline(admin.TabularInline):
    model = Chapter
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
    inlines = [ComicTranslationInline, ChapterInline]


class ChapterTranslationInline(admin.TabularInline):
    model = ChapterTranslation
    extra = 0
    show_change_link = True


@admin.register(ComicTranslation)
class ComicTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "comic",
        "language",
        "title",
        "is_valid",
        "display_authors",
    )
    inlines = [ChapterTranslationInline]


@admin.register(AuthorTranslation)
class AuthorTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "language",
        "pen_name",
    )


class AuthorTranslationInline(admin.TabularInline):
    model = AuthorTranslation
    extra = 0
    show_change_link = True


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "pen_name",
        "default_language",
    )
    search_fields = ["pen_name"]
    inlines = [AuthorTranslationInline]


class PageInline(admin.TabularInline):
    model = Page
    extra = 0
    show_change_link = True


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "comic",
        "number",
        "counter",
        "title",
        "extra",
        "is_valid",
    )
    list_filter = ("published_date",)
    search_fields = ["title"]
    inlines = [PageInline, ChapterTranslationInline]


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("chapter", "display_chapter_counter", "number")
    search_fields = [
        "chapter__comic__title",
        "number",
        "chapter__number",
        "chapter__counter",
    ]


class PageTranslationInline(admin.TabularInline):
    model = PageTranslation
    extra = 0
    show_change_link = True


@admin.register(ChapterTranslation)
class ChapterTranslationAdmin(admin.ModelAdmin):
    list_display = (
        "comic_translation",
        "display_chapter_number",
        "display_chapter_counter",
        "title",
        "is_valid",
    )
    search_fields = ["title"]
    list_filter = ("published_date",)
    inlines = [PageTranslationInline]


class PostMediaInline(admin.TabularInline):
    model = PostMedia
    show_change_link = True
    extra = 0

class PostInline(admin.TabularInline):
    model = Post
    show_change_link = True
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_profile",
        "writing_mode",
        "created_time",
        "last_modified",
        "reply_to",
    )
    inlines = [PostMediaInline, PostInline]

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass




@admin.register(PageTranslation)
class PageTranslationAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass
