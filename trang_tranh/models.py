from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(_("profile name"), max_length=200)
    avatar = models.ImageField(
        _("profile avatar"),
        upload_to="profile-avatars/",
        height_field=None,
        width_field=None,
        max_length=None,
        help_text=_("Upload profile avatar"),
        blank=True,
        null=True,
    )
    bio = models.TextField(_("profile bio"), max_length=500)
    followers = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        blank=True,
        null=True,
    )
    following = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user}"


class Comic(models.Model):
    """
    Model representing a comic series.
    """

    title = models.CharField(max_length=200, help_text=_("Enter a comic title"))

    vertical_cover = models.ImageField(
        _("comic vertical cover"),
        upload_to="comic-covers/vertical/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    horizontal_cover = models.ImageField(
        _("comic horizontal cover"),
        upload_to="comic-covers/horizontal/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    author = models.ManyToManyField("ComicAuthor", verbose_name=_("comic author"))

    read_count = models.IntegerField(_("read count"), default=0)

    published_date = models.DateField(auto_now=False, auto_now_add=True)

    publisher = models.ForeignKey("UserProfile", on_delete=models.PROTECT)

    summary = models.TextField(_("comic summary"), blank=True, null=True)

    SERIALIZED_STATUS = (
        ("o", "Ongoing"),
        ("c", "Complete"),
        ("h", "Hiatus"),
    )

    SERIALIZED_SCHEDULE = (
        ("w", "Weekly"),
        ("m", "Monthly"),
        ("i", "Indefinite"),
    )

    schedule = models.CharField(
        _("serializing schedule"),
        max_length=1,
        default="w",
        choices=SERIALIZED_SCHEDULE,
        help_text=_("Serializing schedule"),
    )

    status = models.CharField(
        _("series status"),
        max_length=1,
        choices=SERIALIZED_STATUS,
        default="o",
        help_text=_("Serializing status"),
    )

    def __str__(self):
        """String for representing the comic"""
        return f"{self.title} - {self.publisher}"

    def display_author(self):
        """
        Create a string for the Author. This is required to display
        author in Admin.
        """
        return ', '.join(author.pen_name for author in self.author.all()[:3])

    display_author.short_description = 'Author'

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this comic series."""
        return reverse("comic-detail", kwargs={"pk": self.pk})


class ComicAuthor(models.Model):
    pen_name = models.CharField(
        _("pen name"), max_length=200, help_text=_("Enter the (pen) name of the author")
    )

    def __str__(self):
        """String for representing the comic author"""
        return self.pen_name


class ComicTranslation(models.Model):
    """
    Model representing a comic translation.
    """

    comic = models.ForeignKey(
        "Comic", verbose_name=_("comic"), on_delete=models.PROTECT
    )

    language = models.ForeignKey("Language", on_delete=models.PROTECT)
    # Foreign Key used because a comic translation can only have one
    # language, but languages can have multiple comic translations

    translated_title = models.CharField(
        _("translated title"),
        max_length=200,
        help_text=_("Enter a translated title for the comic"),
    )

    translated_summary = models.TextField(
        _("translated summary"),
        max_length=1000,
        help_text=_("Enter a translated summary for the comic"),
    )

    def __str__(self):
        """String for representing the comic translation"""
        return f"{self.language} - {self.comic}"


class ComicChapter(models.Model):
    """
    Model representing a comic chapter.
    """

    comic = models.ForeignKey(
        "Comic", verbose_name=_("comic"), on_delete=models.PROTECT
    )
    cover = models.ImageField(
        _("chapter cover"),
        upload_to="chapter-covers/",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    title = models.CharField(_("chapter title"), max_length=200)

    chapter_number = models.IntegerField(_("chapter number"))

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        """String for representing a comic chapter"""
        return f"[{self.chapter_number}] {self.title} - {self.comic}"


class ComicChapterTranslation(models.Model):
    """Model representing a chapter translation"""

    chapter = models.ForeignKey(
        "ComicChapter", verbose_name=_("comic chapter"), on_delete=models.PROTECT
    )
    language = models.ForeignKey(
        "Language", verbose_name=_("chapter language"), on_delete=models.PROTECT
    )
    translated_title = models.CharField(_("translated title"), max_length=200)

    def __str__(self):
        return f"{self.language} - {self.chapter}"


class ChapterPage(models.Model):
    """Model representing a chapter page"""

    comic_chapter_translation = models.ForeignKey(
        "ComicChapterTranslation", on_delete=models.PROTECT
    )
    page_image = models.ImageField(
        _("page image"),
        upload_to="page-images/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    page_number = models.IntegerField(_("page number"))

    def __str__(self):
        return f"{self.page_number} - {self.comic_chapter_translation}"


class Language(models.Model):
    """
    Model representing a language.
    """

    name = models.CharField(_("language name"), max_length=200)
    code = models.CharField(_("language code"), max_length=10)

    def __str__(self):
        return f"{self.name}({self.code})"
