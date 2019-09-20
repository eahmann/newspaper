from django import forms

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.core.blocks import StreamBlock, TextBlock
#from wagtailmarkdown.blocks import MarkdownBlock
#from wagtailcodeblock.blocks import CodeBlock
from wagtail.admin.edit_handlers import (
    FieldPanel,)

class ImageFormatChoiceBlock(blocks.FieldBlock):
    field = forms.ChoiceField(choices=(
        ('left', 'Wrap left'),
        ('right', 'Wrap right'),
        ('half', 'Half width'),
        ('full', 'Full width'),
    ))


class ImageBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    alignment = ImageFormatChoiceBlock()
    caption = blocks.CharBlock()
    attribution = blocks.CharBlock(required=False)

    class Meta:
        template = "streams/streamfield.html"
        icon = "image"


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add additional text")
    choices = (
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right')
    )

    alignment = FieldPanel(field_name='choices', widget=forms.ChoiceField(choices=choices))

    class Meta: # noqa
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"

class TitleWithBreak(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, help_text="Add your title")



    class Meta: # noqa
        template = "streams/title_with_break.html"
        icon = "edit"
        label = "Title with line break"


class CenteredTitle(blocks.StructBlock):
    """Title and text and nothing else."""

    title = blocks.CharBlock(required=True, max_length=75, help_text="Add your title")
    subtitle = blocks.TextBlock(required=False, help_text="Add subtitle text")

    class Meta: # noqa
        template = "streams/centered_title.html"
        icon = "edit"
        label = "Centered Title"


class SimpleRichTextBlock(blocks.RichTextBlock):
    """Rich text block"""

    def __init__(self, required=True, help_text=None, editor='default', features=None, **kwargs):
        super().__init__(**kwargs)
        self.features = ['bold', 'italic', 'link', ]
        
    class Meta:
        template = "streams/rich_text_block.html"
        icon = "edit"
        label = "Simple RichText"        


class CardBlock(blocks.StructBlock):
    """ Cards with images, text, and a button. """

    title = blocks.CharBlock(required=True, help_text="Add your title")
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("image", ImageChooserBlock(required=True)),
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("text", SimpleRichTextBlock(required=True, max_length=150)),
                ("button_page", blocks.PageChooserBlock(required=False)),
                ("button_url", blocks.URLBlock(
                    required=False,
                    help_text="If the button page above is selected, that will be used first.")),
                ("button_text", blocks.CharBlock(
                    required=False,
                    max_length=30, 
                    default="See more", 
                    help_text="Enter some text for the button")),
            ]
        )
    )

    class Meta:
        template = "streams/card_block.html"
        icon = "placeholder"
        label = "Bootstrap Card Deck"


class RichTextBlock(blocks.RichTextBlock):
    """Rich text block"""

    class Meta:
        template = "streams/rich_text_block.html"
        icon = "doc-full"
        label = "Full RichText"


class CTABlock(blocks.StructBlock):
    """ Call to artion block """

    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, max_length=200, features=['bold', 'italic'])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False, help_text="If the button page above is selected, that will be used first.")
    button_text = blocks.CharBlock(required=False, max_length=30, default="See more", help_text="Enter some text for the button")

    class Meta:
        template = "streams/cta_block.html"
        icon = "placeholder"
        label = "Call to action"


class LinkStructValue(blocks.StructValue):
    """Additional logic for our urls."""

    def url(self):
        button_page = self.get('button_page')
        button_url = self.get('button_url')
        if button_page:
            return button_page.url
        elif button_url:
            return button_url

        return None


class ButtonBlock(blocks.StructBlock):
    button_page = blocks.PageChooserBlock(required=False, help_text="If selected, this page will be used")
    button_url = blocks.URLBlock(required=False, help_text="If added, this URL will be used instead.")
    button_text = blocks.CharBlock(required=True, max_length=30, help_text="Enter some text for the button")

    class Meta:
        template = "streams/button_block.html"
        icon = "placeholder"
        label = "Button"
        value_class = LinkStructValue


class ImageCarouselBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    caption = blocks.TextBlock(required=False)

    class Meta:
        template = 'streams/image_carousel.html'
        icon = 'image'


# class MarkdownBlock(StreamBlock):
#     markdown = MarkdownBlock(icon="code")


# class ContentStreamBlock(StreamBlock):
#     heading = TextBlock()
#     paragraph = TextBlock()
#     code = CodeBlock(label='Code')

class BlockQuote(blocks.StructBlock):
    text = blocks.TextBlock(required=False)

    class Meta:
        template = 'streams/block_quote.html'