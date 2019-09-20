from datetime import datetime
# Django imports
from django.db import models
from modelcluster.fields import ParentalManyToManyField, ParentalKey
from django.forms import CheckboxSelectMultiple
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# Wagtail core imports
from wagtail.core.blocks import (BlockQuoteBlock, CharBlock, ListBlock,
                                 RawHTMLBlock)
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    StreamFieldPanel,
    PageChooserPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.models import AbstractImage, AbstractRendition, Image
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

# Extension imports

# Local imports
from core.blocks import (ButtonBlock, CardBlock, CenteredTitle,
                         CTABlock, ImageCarouselBlock,
                         ImageChooserBlock, RichTextBlock, SimpleRichTextBlock,
                         TitleAndTextBlock, ImageFormatChoiceBlock, ImageBlock,
                         TitleWithBreak, BlockQuote)

@register_snippet
class ArticleCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class ArticleCategoryOrderable(Orderable):
    page = ParentalKey("BasePage", related_name="article_categories")
    article_category = models.ForeignKey(
        "ArticleCategory",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [SnippetChooserPanel("article_category")]


class CustomImage(AbstractImage):
    caption = models.CharField(max_length=255, blank=True)
    credit = models.CharField(max_length=255, blank=True)

    admin_form_fields = Image.admin_form_fields + (
        'credit',
        'caption',
    )

    @property
    def caption_text(self):
        return self.caption

    @property
    def credit_text(self):
        return self.credit


class CustomRendition(AbstractRendition):
    image = models.ForeignKey(
        'CustomImage',
        on_delete=models.CASCADE,
        related_name='renditions'
        )

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )

class Author(Orderable):
    page = ParentalKey('BasePage', related_name='authors')
    author = models.ForeignKey(
        'people.Person',
        on_delete=models.CASCADE,
        related_name='+',
    )

    panels = [
        SnippetChooserPanel('author'),
    ]

class BasePage(Page):
    # Fields
    # tags = ClusterTaggableManager(through='ArticlePageTag', blank=True)
    sub_title = models.CharField(max_length=500, blank=True)
    main_image = models.ForeignKey(
        'CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='An image for including on other pages'
    )
    date = models.DateField("Post date", default=datetime.today)
    allow_comments = models.BooleanField('allow comments', default=True)
    allow_main_image = models.BooleanField('Show main image on page', default=True)

    # Panels
    settings_panels = Page.settings_panels + [
        FieldPanel('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('sub_title'),
        MultiFieldPanel(
            [
                ImageChooserPanel('main_image'),
                FieldPanel('allow_main_image'),
            ],
            heading="Main Image",
        ),
    ]

    article_panels = [
        FieldPanel('allow_comments'),
        InlinePanel('authors', label="Author"),
        MultiFieldPanel(
            [
                InlinePanel('article_categories', label="Categories", min_num=1),
            ],
            heading="Category Options",
        ),
    ]




class ArticlePage(BasePage):
    # Configuration
    template = "articles/article_page.html"

    # Fields
    body = StreamField(
        [
            ('title_with_break', TitleWithBreak()),
            ('block_quote', BlockQuote()),

            ('title_and_text', TitleAndTextBlock()),
            ('centered_title', CenteredTitle()),
            ('full_richtext', RichTextBlock()),
            ('simple_richtext', SimpleRichTextBlock()),
            #('heading', CharBlock()),
            #('quote_block', BlockQuoteBlock()),
            ('image', ImageChooserBlock()),
            ('HTML', RawHTMLBlock()),
            ('cards', CardBlock()),
            ('cta', CTABlock()),
            ('button', ButtonBlock()),
            ('image_carousel', ListBlock(ImageCarouselBlock())),
            ('image_block', ImageBlock()),
            #('code_block', ContentStreamBlock()),
            #('equation', MathBlock()),
        ],
        null=True,
        blank=True,
    )

    # Panels
    content_panels = BasePage.content_panels + [
        StreamFieldPanel('body'),
    ]

    # Add custom tab to admin
    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(BasePage.article_panels, heading="Article Settings"),
            ObjectList(BasePage.settings_panels, heading='Publishing'),
            ObjectList(Page.promote_panels, heading='Promote'),
        ]
    )


class ArticleIndexPage(Page):
    subpage_types = [
        'core.ArticlePage',
    ]

    template = 'articles/article_index_page.html'
    font_awesome_icon = models.CharField(max_length=75, blank=True)

    def get_posts(self):
        return BasePage.objects.all().live()

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(date__year=year)
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)

    # settings_panels = Page.settings_panels+[
    #     menupage_panel
    # ]
    # def get_context(self, request):
    #     context = super().get_context(request)
    #     article_pages = ArticlePage.objects.filter(article_categories__article_category__slug=self.slug)
    #     #index = ArticleIndexPage.objects.get(slug='articles') # !! Used for reversing article URLs !!
    #     article_pages = article_pages.order_by('-date')
    #     context['article_pages'] = article_pages
    #     #context['index'] = index
    #     return context


    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        # Get all posts
        all_posts = ArticlePage.objects.filter(article_categories__article_category__slug=self.slug)
        # Paginate all posts by 2 per page
        paginator = Paginator(all_posts, 2)
        # Try to get the ?page=x value
        page = request.GET.get("page")
        try:
            # If the page exists and the ?page=x is an int
            posts = paginator.page(page)
        except PageNotAnInteger:
            # If the ?page=x is not an int; show the first page
            posts = paginator.page(1)
        except EmptyPage:
            # If the ?page=x is out of range (too high most likely)
            # Then return the last page
            posts = paginator.page(paginator.num_pages)

        # "posts" will have child pages; you'll need to use .specific in the template
        # in order to access child properties, such as youtube_video_id and subtitle
        context["posts"] = posts
        return context

    

    content_panels = Page.content_panels + [
        FieldPanel('font_awesome_icon')
    ]

    class Meta:  # noqa
        verbose_name = 'Article index page'
        verbose_name_plural = 'Article index pages'
