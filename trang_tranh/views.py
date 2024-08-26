from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from .forms import PostForm, SignUpForm
from .models import Chapter, Comic, Post, PostMedia, User, UserProfile
from .tokens import account_activation_token
from django.core.exceptions import ValidationError
# Create your views here.


def index(request):
    """View function for home page of site."""
    page_number = request.GET.get("page", 1)
    paginator = Paginator(Chapter.objects.all().order_by("-published_date"), 20)
    updated_chapters = paginator.get_page(page_number)
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


@login_required
def feed(request):
    page_number = request.GET.get("page", 1)
    paginator = Paginator(Post.objects.all().order_by("-created_time"), 5)
    new_posts = paginator.get_page(page_number)
    # new_posts = Post.objects.all().order_by("-created_time")[:5]

    context = {
        "new_posts": new_posts,
    }
    return render(request, "trang_tranh/feed.html", context=context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    page_number = request.GET.get("page", 1)
    paginator = Paginator(post.post_set.all().order_by("-created_time"), 3)
    new_replies = paginator.get_page(page_number)

    context = {
        "post": post,
        "new_replies": new_replies,
    }

    return render(request, "trang_tranh/post_detail.html", context=context)


def profile_detail(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)
    page_number = request.GET.get("page", 1)
    paginator = Paginator(profile.post_set.all().order_by("-created_time"), 5)
    profile_posts = paginator.get_page(page_number)

    context = {
        "profile": profile,
        "profile_posts": profile_posts,
    }

    return render(request, "trang_tranh/profile_detail.html", context=context)


def profile_chapter_updates(request, pk):
    profile = get_object_or_404(UserProfile, pk=pk)

    context = {
        "profile": profile,
    }

    return render(request, "trang_tranh/profile_chapter_updates.html", context=context)


@login_required
def notification(request):
    return render(request, "trang_tranh/notifications.html")


def settings(request):
    return render(request, "trang_tranh/settings.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = _("Activate Your Trang tranh Account")
            message = render_to_string(
                "registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            user.email_user(subject, message)
            return redirect("account-activation-sent")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def account_activation_sent(request):
    return render(request, "registration/account_activation_sent.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        return render(request, "registration/account_activation_complete.html")
    else:
        return render(request, "registration/account_activation_invalid.html")


class PostCreateView(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = "trang_tranh/post_form.html"
    success_url = reverse_lazy("feed")

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        text_content = form.cleaned_data["text_content"]
        images = form.cleaned_data["media"]
        writing_mode = form.cleaned_data["writing_mode"]
        try:
            user_profile = get_object_or_404(UserProfile, user=self.request.user)
            new_post = Post(user_profile=user_profile, text_content=text_content, writing_mode=writing_mode)
            new_post.save()
            for i in images:
                new_post_media = PostMedia(post=new_post, image=i, alt_text="test")
                new_post_media.save()
            return super().form_valid(form)
        except :
            raise ValidationError("Error")


@login_required
def post_update(request, pk):
    pass


def post_delete(request, pk):
    pass
