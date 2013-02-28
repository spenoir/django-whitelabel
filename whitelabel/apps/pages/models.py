from datetime import datetime
from django.core.files.storage import FileSystemStorage
import os
import re
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from html_field.db.models import HTMLField
from html_field import html_cleaner
from taggit.managers import TaggableManager

cleaner = html_cleaner.HTMLCleaner(allow_tags=settings.ALLOWED_TAGS)


class Page(models.Model):
    """ A page is the overall page that can have child pages but
        doesn't have to so can be used for static pages too """

    class Meta:
        abstract = True

    title = models.CharField(max_length=510, help_text="""
        The page title
    """)
    slug = models.SlugField(unique=True, max_length=510,
        blank=True, null=True, help_text="""
        Where on the site does the page exist
    """)
    live = models.BooleanField(default=True, help_text="""
        Is the page currently live on the site?
    """)
    template = models.FilePathField(path=os.path.join(settings.DJANGO_ROOT, 'templates/pages'),
        default='pages/default.html', help_text="""
            Choose which template you would like to use for the content and inner layout of this page.
        """)
    base_template = models.FilePathField(path=os.path.join(settings.DJANGO_ROOT, 'templates/base'),
        default='base/page_detail.html', help_text="""
            Choose which template you would like to use for the base layout of this page.
        """)
    content = HTMLField(cleaner, blank=True)
    weight = models.DecimalField(blank=True, null=True,
        max_digits=7, decimal_places=2, help_text="""
        Set this to determine the pages order in its respective nav.
        It will default to the order in which they are added
    """)
    parent = models.ForeignKey('self', blank=True, null=True,
        related_name='subpages')
    top_nav = models.BooleanField(default=False, help_text="""
        Does the page appear in the top nav?
    """)
    main_nav = models.BooleanField(default=False, help_text="""
        Does the page appear in the main nav at the top level?
    """)
    footer_nav = models.BooleanField(default=False, help_text="""
        Does the page appear in the footer navigation? The weight value also applies to footer nav.
    """)

    pub_date = models.DateTimeField(default=datetime.now(), help_text="""
      The date this page was last edited
    """)

    def is_top_level(self):
        return self.parent is None


    def __unicode__(self):
        return u'%s' % self.title

    def get_absolute_url(self):
        if self.slug and self.parent:
            return "/%s/%s/" % (self.parent.slug, self.slug)
        if self.slug:
            return "/%s/" % self.slug
        else:
            return "/"

    def clean(self):
        # check for a valid slug
        if self.slug:
            slug_regex = re.compile('^[-\w]+$')
            if not re.match(slug_regex, self.slug):
                raise ValidationError('The slug %s is not valid, please try again' % self.slug)

            # limit slugs to max 254 chars
            self.slug = self.slug[:254]

        self.title = self.title[:254]

        if not self.weight:
            self.weight = self.pk

    def save(self, **kwargs):
        self.full_clean()

        return super(Page, self).save(**kwargs)


class WebPage(Page):
    pass


class Image(models.Model):
    """
    Base Image
    """
    class Meta:
        abstract = True

    title = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True)
    caption = models.TextField(blank=True)
    date = models.DateField(default=datetime.now())
    tags = TaggableManager()
    live = models.BooleanField(default=True, help_text="""
        Is the page currently live on the site?
    """)

    def __unicode__(self):
        return u'%s' % self.image.name

    def get_absolute_url(self):
        if getattr(self, 'image'):
            return self.image.path
        else:
            return self.title

class PageImage(Image):
    """
    An Image that is specific to a Page
    """
    image = models.ImageField(upload_to='img/pages')
    page = models.ForeignKey('WebPage', related_name='images')


class GalleryImage(Image):
    image = models.ImageField(upload_to='img/gallery')


class HeardFrom(models.Model):
    value = models.CharField(max_length=50)
    frequency = models.IntegerField(editable=False, default=0)

    def __unicode__(self):
        return self.value
