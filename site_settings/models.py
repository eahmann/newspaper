from django.db import models

from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel

from core.models import CustomImage

@register_setting
class SocialMediaSettings(BaseSetting):
    """Social media settings for our custom website."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")
    instagram = models.URLField(blank=True, null=True, help_text="Instagram URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),
            FieldPanel("instagram")
        ], heading="Social Media Settings")
    ]


@register_setting
class MainSiteSettings(BaseSetting):
    """General settings"""

    # SEO settings

    small_logo = models.ForeignKey(
        'core.CustomImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='An image for navbar'
    )

    panels = [
        ImageChooserPanel('small_logo'),
    ]
