from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.core.fields import RichTextField, StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from .blocks import BaseStreamBlock


@register_snippet
class People(index.Indexed, ClusterableModel):
    """
    A Django model to store People objects.
    It uses the `@register_snippet` decorator to allow it to be accessible
    via the Snippets UI (e.g. /admin/snippets/base/people/)

    `People` uses the `ClusterableModel`, which allows the relationship with
    another model to be stored locally to the 'parent' model (e.g. a PageModel)
    until the parent is explicitly saved. This allows the editor to use the
    'Preview' button, to preview the content, without saving the relationships
    to the database.
    https://github.com/wagtail/django-modelcluster
    """
    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    job_title = models.CharField("Job title", max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname="col6"),
                FieldPanel('last_name', classname="col6"),
            ])
        ], "Name"),
        FieldPanel('job_title'),
        ImageChooserPanel('image')
    ]

    search_fields = [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    @property
    def thumb_image(self):
        # Returns an empty string if there is no profile pic or the rendition
        # file can't be found.
        try:
            return self.image.get_rendition('fill-50x50').img_tag()
        except:
            return ''

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'


@register_snippet
class FooterText(models.Model):
    """
    This provides editable text for the site footer. Again it uses the decorator
    `register_snippet` to allow it to be accessible via the admin. It is made
    accessible on the template via a template tag defined in base/templatetags/
    navigation_tags.py
    """
    body = RichTextField()

    panels = [
        FieldPanel('body'),
    ]

    def __str__(self):
        return "Footer text"

    class Meta:
        verbose_name_plural = 'Footer Text'


class StandardPage(Page):
    """
    A generic content page. On this demo site we use it for an about page but
    it could be used for any type of page content that only needs a title,
    image, introduction and body field
    """

    introduction = models.TextField(
        help_text='Text to describe the page',
        blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Landscape mode only; horizontal width between 1000px and 3000px.'
    )
    body = StreamField(
        BaseStreamBlock(), verbose_name="Page body", blank=True
    )
    content_panels = Page.content_panels + [
        FieldPanel('introduction', classname="full"),
        StreamFieldPanel('body'),
        ImageChooserPanel('image'),
    ]


class HomePage(Page):
    """
    The Home Page. This looks slightly more complicated than it is. You can
    see if you visit your site and edit the homepage that it is split between
    a:
    - Hero area
    - Body area
    - A promotional area
    - Moveable featured site sections
    """

    # Hero section of HomePage
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Homepage image'
    )
    hero_text = models.CharField(
        max_length=255,
        default='text here',
        help_text='Write an introduction for the bakery'
    )

    # Body section of the HomePage
    body = StreamField(
        BaseStreamBlock(), verbose_name="Home content block", blank=True
    )

    # Promo section of the HomePage
    promo_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Promo image'
    )
    promo_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    promo_text = RichTextField(
        null=True,
        blank=True,
        help_text='Write some promotional copy'
    )

    # Featured sections on the HomePage
    # You will see on templates/base/home_page.html that these are treated
    # in different ways, and displayed in different areas of the page.
    # Each list their children items that we access via the children function
    # that we define on the individual Page models e.g. BlogIndexPage
    featured_section_1_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_1 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='First featured section for the homepage. Will display up to '
                  'three child items.',
        verbose_name='Featured section 1'
    )

    featured_section_2_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_2 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Second featured section for the homepage. Will display up to '
                  'three child items.',
        verbose_name='Featured section 2'
    )

    featured_section_3_title = models.CharField(
        null=True,
        blank=True,
        max_length=255,
        help_text='Title to display above the promo copy'
    )
    featured_section_3 = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Third featured section for the homepage. Will display up to '
                  'six child items.',
        verbose_name='Featured section 3'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel('image'),
            FieldPanel('hero_text', classname="full"),
        ], heading="Hero section"),
        MultiFieldPanel([
            ImageChooserPanel('promo_image'),
            FieldPanel('promo_title'),
            FieldPanel('promo_text'),
        ], heading="Promo section"),
        StreamFieldPanel('body'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('featured_section_1_title'),
                PageChooserPanel('featured_section_1'),
            ]),
            MultiFieldPanel([
                FieldPanel('featured_section_2_title'),
                PageChooserPanel('featured_section_2'),
            ]),
            MultiFieldPanel([
                FieldPanel('featured_section_3_title'),
                PageChooserPanel('featured_section_3'),
            ])
        ], heading="Featured homepage sections", classname="collapsible")
    ]

    def __str__(self):
        return self.title
