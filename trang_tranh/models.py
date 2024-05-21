from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint
from django.db.models.functions import Lower
from django.db.models import Q
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError
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

    def __str__(self):
        return self.name


class Comic(models.Model):
    """
    Model representing a comic series.
    """

    title = models.CharField(max_length=200, help_text=_("Enter a comic title"))

    vertical_cover = models.ImageField(
        _("vertical cover"),
        upload_to="comic-covers/vertical/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    horizontal_cover = models.ImageField(
        _("horizontal cover"),
        upload_to="comic-covers/horizontal/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    square_cover = models.ImageField(
        _("square cover"),
        upload_to="comic-covers/square/",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )

    author = models.ManyToManyField("ComicAuthor", verbose_name=_("comic author"))

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    publisher = models.ForeignKey(
        "UserProfile", verbose_name=_("publisher"), on_delete=models.PROTECT
    )

    summary = models.TextField(
        _("comic summary"), max_length=1000, blank=True, null=True
    )

    default_language = models.CharField(
        _("default language"), max_length=10, choices=settings.LANGUAGES, default="en"
    )

    SERIALIZED_STATUS = (
        ("o", _("Ongoing")),
        ("c", _("Complete")),
        ("h", _("Hiatus")),
    )

    SERIALIZED_SCHEDULE = (
        ("w", _("Weekly")),
        ("m", _("Monthly")),
        ("i", _("Indefinite")),
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
        return ", ".join(author.pen_name for author in self.author.all()[:3])

    display_author.short_description = "Author"

    def display_total_chapter(self):
        return self.comicchapter_set.all().count()

    display_total_chapter.short_description = "Total chapter"

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

    language = models.CharField(
        _("translation language"),
        max_length=10,
        choices=settings.LANGUAGES,
        default="en",
    )

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

    def clean(self):
        if self.language == self.comic.default_language:
            raise ValidationError(
                {
                    "language": _(
                        "Translation language must not be the same as default language"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comic", "language"],
                name="unique_comic_translation_language",
            )
        ]


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

    chapter_number = models.PositiveSmallIntegerField(
        _("chapter number"),
        default=1,
        blank=True,
        null=True,
    )

    chapter_counter = models.PositiveSmallIntegerField(_("chapter counter"), default=1)

    extra_chapter = models.BooleanField(_("extra chapter"), default=False)

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    def __str__(self):
        """String for representing a comic chapter"""
        return _("Chapter ") + f"{self.chapter_number} - {self.comic}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comic", "chapter_number"],
                name="unique_comic_chapter_number",
            ),
            UniqueConstraint(
                fields=["comic", "chapter_counter"],
                name="unique_comic_chapter_counter",
            ),
            UniqueConstraint(
                fields=["comic", "chapter_counter", "chapter_number"],
                name="unique_comic_chapter_counter_and_chapter_number",
            ),
            CheckConstraint(
                check=(Q(chapter_number__isnull=True) & Q(extra_chapter__exact=True))
                | (Q(chapter_number__isnull=False) & Q(extra_chapter__exact=False)),
                name="comic_chapter_number_is_null_when_extra_chapter_is_true",
            ),
        ]


class ComicChapterTranslation(models.Model):
    """Model representing a chapter translation"""

    comic_translation = models.ForeignKey(
        "ComicTranslation",
        verbose_name=_("comic translation"),
        on_delete=models.PROTECT,
    )

    chapter_number = models.PositiveSmallIntegerField(
        _("chapter number"),
        default=1,
        blank=True,
        null=True,
    )

    translated_title = models.CharField(_("translated title"), max_length=200)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    chapter_counter = models.PositiveSmallIntegerField(_("chapter counter"), default=1)

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    extra_chapter = models.BooleanField(_("extra chapter"), default=False)

    def __str__(self):
        return _("Chapter ") + f"{self.chapter_number} - {self.comic_translation}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comic_translation", "chapter_number"],
                name="unique_comic_translation_chapter_number",
            ),
            UniqueConstraint(
                fields=["comic_translation", "chapter_counter"],
                name="unique_comic_translation_chapter_counter",
            ),
            UniqueConstraint(
                fields=["comic_translation", "chapter_counter", "chapter_number"],
                name="comic_translation_chapter_counter_and_chapter_number",
            ),
        ]


class ChapterPage(models.Model):
    """Model representing the default language chapter page"""

    chapter = models.ForeignKey(
        "ComicChapter", verbose_name=_("comic chapter"), on_delete=models.PROTECT
    )

    page_image = models.ImageField(
        _("page image"),
        upload_to="page-images/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    page_number = models.PositiveSmallIntegerField(_("page number"), default=1)

    def display_chapter_counter(self):
        return self.chapter.chapter_counter

    display_chapter_counter.short_description = "Chapter counter"

    def __str__(self):
        return _("Page ") + f"{self.page_number} - {self.chapter}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["chapter", "page_number"],
                name="unique_chapter_page_number",
            )
        ]

    def clean(self):
        if self.page_number > self.chapter.chapterpage_set.all().count() + 1:
            raise ValidationError(
                {
                    "page_number": _(
                        "Page number can not be larger than the total number of pages"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class ChapterPageTranslation(models.Model):
    """Model representing a chapter page translation"""

    chapter_translation = models.ForeignKey(
        "ComicChapterTranslation",
        verbose_name=_("chapter translation"),
        on_delete=models.PROTECT,
    )

    page_image = models.ImageField(
        _("page image"),
        upload_to="page-image-translations/",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    page_number = models.PositiveSmallIntegerField(_("page number"), default=1)

    def __str__(self):
        return _("Page ") + f"{self.page_number} - {self.chapter_translation}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["chapter_translation", "page_number"],
                name="unique_chapter_translation_page_number",
            )
        ]

    def clean(self):
        if self.page_number > self.chapter_translation.chapterpagetranslation_set.all().count() + 1:
            raise ValidationError(
                {
                    "page_number": _(
                        "Page number can not be larger than the total number of pages"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

