from django.db import models
from django.shortcuts import render
from django.http import Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Orderable, Page
from wagtail.admin.edit_handlers import (FieldPanel, PageChooserPanel,
                                         InlinePanel, MultiFieldPanel)

from core.models import ArticlePage
from modelcluster.fields import ParentalKey


class HomePage(Page):
    # Configuration
    templates = "home/home_page.html"
    max_count = 1
    # subpage_types = [
    #     'core.ArticleIndexPage',
    #     'people.StaffPage',
    # ]
    parent_page_type = [
        'wagtailcore.Page'
    ]

    # Fields
    tagline = models.CharField(max_length=250, blank=False, null=True)

    # Methods
    def get_posts(self):
        return ArticlePage.objects.all().live()

    # Panels
    content_panels = Page.content_panels + [
        FieldPanel("tagline"),
        # MultiFieldPanel([
        #     InlinePanel(
        #         'carousel_items',
        #         max_num=5,
        #         label="Featured Atricles"
        #     )
        # ], heading='Carousel Items')
    ]

    # Context
    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        all_posts = ArticlePage.objects.live().public().order_by('-date')
        paginator = Paginator(all_posts, 10)
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

    # settings_panels = Page.settings_panels+[
    #     menupage_panel
    # ]

    class Meta:

        verbose_name = "Home Page"
        verbose_name_plural = "Home Pages"