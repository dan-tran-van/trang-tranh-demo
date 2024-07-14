from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class User(AbstractUser):
    pass


GENRES = (
    ("adventure", _("Adventure")),
    ("sci-fi", _("Science Fiction")),
    ("mystery", _("Mystery")),
    ("fantasy", _("Fantasy")),
    ("action", _("Action")),
    ("romance", _("Romance")),
)

WRITING_MODE = (
        ("h-tb", _("horizontal-tb")),
        ("v-rl", _("vertical-rl")),
        ("v-lr", _("vertical-lr")),
    )

class Genre(models.Model):
    name = models.CharField(
        _("name"),
        max_length=100,
        choices=GENRES,
    )

    class Meta:
        verbose_name = _("Genre")
        verbose_name_plural = _("Genres")
        constraints = [
            UniqueConstraint(fields=['name'],name="unique_genre_name")
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Genre_detail", kwargs={"pk": self.pk})


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, verbose_name=_("user"), on_delete=models.CASCADE
    )
    name = models.CharField(_("profile name"), max_length=200)
    email_confirmed = models.BooleanField(default=False)

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
    bio = models.TextField(_("profile bio"), max_length=500, blank=True, null=True)
    bio_writing_mode = models.CharField(_("bio writing mode"), max_length=50, choices=WRITING_MODE, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("profile-detail", kwargs={"pk": self.pk})


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, name=instance.username)
    instance.userprofile.save()


class Comic(models.Model):
    """
    Model representing a comic series.
    """

    title = models.CharField(_("title"), max_length=200)

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
        blank=True,
        null=True,
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

    author = models.ManyToManyField("Author", verbose_name=_("author"))

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    publisher = models.ForeignKey(
        "UserProfile", verbose_name=_("publisher"), on_delete=models.PROTECT
    )

    summary = models.TextField(_("summary"), max_length=1000, blank=True, null=True)

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
        _("schedule"),
        max_length=1,
        default="w",
        choices=SERIALIZED_SCHEDULE,
        help_text=_("Serializing schedule"),
    )

    status = models.CharField(
        _("status"),
        max_length=1,
        choices=SERIALIZED_STATUS,
        default="o",
        help_text=_("Serializing status"),
    )

    genre = models.ManyToManyField("Genre", verbose_name=_("genre"))

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

    def display_authors(self):
        representative_authors = []
        for author in self.author.all():
            if author.authortranslation_set.all():
                found = False
                for translation in author.authortranslation_set.all():
                    if translation.language == self.default_language:
                        representative_authors.append(translation.pen_name)
                        found = True
                        break
                if not found:
                    representative_authors.append(author.pen_name)
            else:
                representative_authors.append(author.pen_name)

        return " | ".join(representative_authors)

    def display_total_chapter(self):
        return self.chapter_set.all().count()

    display_total_chapter.short_description = "Total chapter"

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this comic series."""
        return reverse("comic-detail", kwargs={"pk": self.pk})

    def is_valid(self):
        valid_chapter_counter = 0
        for chapter in self.chapter_set.all():
            if chapter.is_valid():
                valid_chapter_counter += 1
                break

        return valid_chapter_counter != 0


class Author(models.Model):
    pen_name = models.CharField(
        _("pen name"), max_length=200, help_text=_("Enter the (pen) name of the author")
    )

    default_language = models.CharField(
        _("default language"),
        max_length=10,
        choices=settings.LANGUAGES,
        default="en",
    )

    def __str__(self):
        """String for representing the comic author"""
        return self.pen_name


class AuthorTranslation(models.Model):
    author = models.ForeignKey(
        "Author", verbose_name=_("author"), on_delete=models.PROTECT
    )

    language = models.CharField(
        _("translation language"),
        max_length=10,
        choices=settings.LANGUAGES,
        default="en",
    )

    pen_name = models.CharField(_("pen name"), max_length=200)

    def clean(self):
        if self.language == self.author.default_language:
            raise ValidationError(
                {
                    "language": _(
                        "Translation language can not be the same as the default language"
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.language} - {self.author}    "

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["author", "language"],
                name="unique_author_language",
            )
        ]


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

    title = models.CharField(
        _("translated title"),
        max_length=200,
        help_text=_("Enter a translated title for the comic"),
    )

    summary = models.TextField(
        _("translated summary"),
        max_length=1000,
        help_text=_("Enter a translated summary for the comic"),
    )

    def display_authors(self):
        representative_authors = []
        for author in self.comic.author.all():
            if author.authortranslation_set.all():
                found = False
                for translation in author.authortranslation_set.all():
                    if translation.language == self.language:
                        representative_authors.append(translation.pen_name)
                        found = True
                        break
                if not found:
                    representative_authors.append(author.pen_name)
            else:
                representative_authors.append(author.pen_name)

        return " | ".join(representative_authors)

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

    def is_valid(self):
        valid_chapter_counter = 0
        for chapter in self.chaptertranslation_set.all():
            if chapter.is_valid():
                valid_chapter_counter += 1
                break

        return valid_chapter_counter != 0


class Chapter(models.Model):
    """
    Model representing a comic chapter.
    """

    comic = models.ForeignKey(
        "Comic", verbose_name=_("comic"), on_delete=models.PROTECT
    )

    cover = models.ImageField(
        _("cover"),
        upload_to="chapter-covers/",
        height_field=None,
        width_field=None,
        max_length=None,
    )
    title = models.CharField(_("title"), max_length=200)

    number = models.PositiveSmallIntegerField(
        _("number"),
        default=1,
        blank=True,
        null=True,
    )

    counter = models.PositiveSmallIntegerField(_("counter"), default=1)

    extra = models.BooleanField(_("is extra chapter?"), default=False)

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    def is_valid(self):
        return self.page_set.all().count() != 0

    def __str__(self):
        """String for representing a comic chapter"""
        return _("Chapter ") + f"{self.number} - {self.comic}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["comic", "number"],
                name="unique_chapter_number",
            ),
            UniqueConstraint(
                fields=["comic", "counter"],
                name="unique_chapter_counter",
            ),
            UniqueConstraint(
                fields=["comic", "counter", "number"],
                name="unique_chapter_counter_and_chapter_number",
            ),
            CheckConstraint(
                check=(Q(number__isnull=True) & Q(extra__exact=True))
                | (Q(number__isnull=False) & Q(extra__exact=False)),
                name="chapter_number_is_null_when_extra_chapter_is_true",
            ),
        ]

    def get_absolute_url(self):
        return reverse("chapter-detail", kwargs={"pk": self.pk})

    @property
    def sorted_page_set(self):
        return self.page_set.order_by("number")


class ChapterTranslation(models.Model):
    """Model representing a chapter translation"""

    chapter = models.ForeignKey(
        "Chapter", verbose_name=_("chapter"), on_delete=models.PROTECT
    )

    comic_translation = models.ForeignKey(
        "ComicTranslation",
        verbose_name=_("comic translation"),
        on_delete=models.PROTECT,
    )

    title = models.CharField(_("translated title"), max_length=200)

    published_date = models.DateField(
        _("published date"), auto_now=False, auto_now_add=True
    )

    read_count = models.PositiveIntegerField(_("read count"), default=0, editable=False)

    def display_chapter_counter(self):
        return self.chapter.counter

    display_chapter_counter.short_description = "counter"

    def display_chapter_number(self):
        return self.chapter.number

    display_chapter_number.short_description = "number"

    def __str__(self):
        return _("Chapter ") + f"{self.chapter.number} - {self.comic_translation}"

    def is_valid(self):
        return self.pagetranslation_set.all().count() != 0

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["chapter", "comic_translation"],
                name="unique_chapter_per_comic_translation",
            )
        ]

    def clean(self) -> None:
        if self.chapter.comic != self.comic_translation.comic:
            raise ValidationError(
                _("Chapter's comic must be the same as Comic translation's comic")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "chapter-translation-detail",
            kwargs={
                "pk": self.chapter.pk,
                "lang": self.comic_translation.language,
            },
        )

    @property
    def sorted_page_set(self):
        return self.pagetranslation_set.order_by("number")


class Page(models.Model):
    """Model representing the default language chapter page"""

    chapter = models.ForeignKey(
        "Chapter", verbose_name=_("chapter"), on_delete=models.PROTECT
    )

    image = models.ImageField(
        _("image"),
        upload_to="page-images/",
        # height_field=None,
        # width_field=None,
        max_length=None,
    )

    webp_image = ResizedImageField(
        verbose_name="webp image",
        upload_to="webp-page-images/",
        force_format="WEBP",
        quality=100,
        blank=True,
        null=True,
    )

    number = models.PositiveSmallIntegerField(_("number"), default=1)

    def display_chapter_counter(self):
        return self.chapter.counter

    display_chapter_counter.short_description = "Chapter counter"

    def __str__(self):
        return _("Page ") + f"{self.number} - {self.chapter}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["chapter", "number"],
                name="unique_page_number",
            )
        ]


class PageTranslation(models.Model):
    """Model representing a chapter page translation"""

    chapter_translation = models.ForeignKey(
        "ChapterTranslation",
        verbose_name=_("chapter translation"),
        on_delete=models.PROTECT,
    )

    image = models.ImageField(
        _("page image"),
        upload_to="page-image-translations/",
        # height_field=None,
        # width_field=None,
        max_length=None,
    )

    webp_image = ResizedImageField(
        verbose_name="webp image",
        upload_to="webp-page-image-translations/",
        force_format="WEBP",
        quality=100,
        blank=True,
        null=True,
    )

    number = models.PositiveSmallIntegerField(_("page number"), default=1)

    def __str__(self):
        return _("Page ") + f"{self.number} - {self.chapter_translation}"

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["chapter_translation", "number"],
                name="unique_page_translation_number",
            )
        ]



class Post(models.Model):
    user_profile = models.ForeignKey(
        "UserProfile", verbose_name=_("user profile"), on_delete=models.CASCADE
    )
    text_content = models.TextField(_("text content"), max_length=1000)
    created_time = models.DateTimeField(
        _("created time"), auto_now=False, auto_now_add=True
    )
    last_modified = models.DateTimeField(
        _("last modified"), auto_now=True, auto_now_add=False
    )

    

    writing_mode = models.CharField(
        _("writing mode"),
        max_length=10,
        choices=WRITING_MODE,
        default="h-tb",
    )

    like = models.IntegerField(_("like count"), editable=False, default=0)

    reply_to = models.ForeignKey(
        "self",
        verbose_name=_("reply to"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    about_comic = models.ForeignKey(
        "Comic",
        verbose_name=_("about comic"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    about_chapter = models.ForeignKey(
        "Chapter",
        verbose_name=_("about chapter"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})


class PostMedia(models.Model):
    post = models.ForeignKey(
        "Post", verbose_name=_("post media"), on_delete=models.CASCADE
    )

    image = models.ImageField(
        _("image"),
        upload_to="post-images",
        height_field=None,
        width_field=None,
        max_length=None,
    )

    webp_image = ResizedImageField(
        verbose_name="webp image",
        upload_to="webp-post-images/",
        force_format="WEBP",
        quality=100,
        blank=True,
        null=True,
    )

    alt_text = models.TextField(_("alternative text"), max_length=1000)


class Language(models.Model):
    name = models.CharField(
        _("name"),
        max_length=10,
        choices=settings.LANGUAGES,
    )

    

    writing_mode = models.CharField(
        _("writing mode"), max_length=10, choices=WRITING_MODE
    )

    class Meta:
        constraints = [UniqueConstraint(fields=["name"], name="unique_language")]

    def __str__(self):
        return self.get_name_display()


class Notification(models.Model):
    user_profile = models.ForeignKey(
        "UserProfile", verbose_name=_("user profile"), on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user_profile
