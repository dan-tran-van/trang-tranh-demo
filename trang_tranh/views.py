from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Chapter, Comic, Post, UserProfile

# Create your views here.


def index(request):
    """View function for home page of site."""
    updated_chapters = Chapter.objects.all().order_by("-published_date")[:20]
    context = {
        "updated_chapters": updated_chapters,
    }
    return render(request, "index.html", context=context)


def comic_detail(request, pk):
    comic = get_object_or_404(Comic, pk=pk)
    if not comic.is_valid():
        raise Http404()

    if comic.default_language == request.LANGUAGE_CODE:
        context = {
            "comic": comic,
        }
        return render(request, "trang_tranh/comic_detail.html", context=context)
    else:
        if comic.comictranslation_set.all():
            found = False
            for comic_translation in comic.comictranslation_set.all():
                if (
                    comic_translation.language == request.LANGUAGE_CODE
                    and comic_translation.is_valid
                ):
                    found = True
                    context = {
                        "comic_translation": comic_translation,
                    }
                    return render(
                        request,
                        "trang_tranh/comic_translation_detail.html",
                        context=context,
                    )
            if not found:
                context = {
                    "comic": comic,
                }
                return render(
                    request, "trang_tranh/comic_not_available.html", context=context
                )
        else:
            context = {
                "comic": comic,
            }
            return render(
                request, "trang_tranh/comic_not_available.html", context=context
            )


def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, pk=pk)
    if not chapter.is_valid():
        raise Http404()

    if chapter.comic.default_language == request.LANGUAGE_CODE:
        context = {
            "chapter": chapter,
        }

        return render(request, "trang_tranh/chapter_detail.html", context=context)
    else:
        return HttpResponseRedirect(
            reverse(
                "chapter-translation-detail",
                kwargs={
                    "pk": pk,
                    "lang": request.LANGUAGE_CODE,
                },
            )
        )


def chapter_translation_detail(request, pk, lang):
    chapter = get_object_or_404(Chapter, pk=pk)

    if chapter.comic.default_language == lang:
        return HttpResponseRedirect(
            reverse(
                "chapter-detail",
                kwargs={
                    "pk": pk,
                },
            )
        )
    else:
        if chapter.chaptertranslation_set.all():
            found = False
            for chapter_translation in chapter.chaptertranslation_set.all():
                if (
                    chapter_translation.comic_translation.language == lang
                    and chapter_translation.is_valid
                ):
                    found = True
                    context = {
                        "chapter_translation": chapter_translation,
                    }
                    return render(
                        request,
                        "trang_tranh/chapter_translation_detail.html",
                        context=context,
                    )
            if not found:
                raise Http404()
        else:
            raise Http404()


def feed(request):
    new_posts = Post.objects.all().order_by("-created_time")[:5]

    context = {
        "new_posts": new_posts,
    }
    return render(request, "trang_tranh/feed.html", context=context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    context = {
        "post": post,
    }

    return render(request, "trang_tranh/post_detail.html", context=context)


def profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    context = {
        "profile": profile,
    }

    return render(request, "trang_tranh/profile_detail.html", context=context)


@login_required
def notification(request):
    return render(request, "trang_tranh/notifications.html")


def settings(request):
    return render(request, "trang_tranh/settings.html")
