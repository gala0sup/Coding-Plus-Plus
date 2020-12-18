from django.db import models
from django import forms
from django.utils.text import slugify

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet

from .edit_handlers import ReadOnlyPanel

import pathlib
from django.utils.safestring import mark_safe


@register_snippet
class BlogPageCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=80)

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class BlogEntryPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogEntryPage", related_name="tagged_items", on_delete=models.CASCADE,
    )


class AddImageValue(blocks.StructValue):
    def get_img_tag(self, extra_css=""):
        try:
            has_image = True
            ImageUrl = self.get("Image").get_rendition("original").url
        except:
            has_image = False
            pass
        ImageViaUrl = self.get("Image_Via_Url")
        ImageOverride = self.get("Image_Override")
        AltText = self.get("Alt_Text")
        if ImageOverride == False and has_image:
            return mark_safe(str(" src=" + f'"{ImageUrl}"' + " alt=" + f'"{AltText}"'))
        else:
            return mark_safe(
                str(" src=" + f'"{ImageViaUrl}"' + " alt=" + f'"{AltText}"')
            )


class AddImage(blocks.StructBlock):
    Image = ImageChooserBlock(required=False, null=True, blank=True)
    Image_Via_Url = blocks.URLBlock(required=False, null=True, blank=True)
    Image_Override = blocks.BooleanBlock(
        required=False,
        null=True,
        blank=True,
        help_text="Use Image Via url Instead of Image uploaded",
    )
    Screen_Width_Cover_Image = blocks.BooleanBlock(
        required=False,
        help_text="Cover Image Should Be of Screen Width",
    )

    Alt_Text = blocks.TextBlock(required=False, null=True, blank=True)
    Position = blocks.ChoiceBlock(
        choices=[
            ("center", "center"),
            ("top", "top"),
            ("left", "left"),
            ("right", "right"),
        ],
        required=False,
        null=True,
        blank=True,
        help_text="No Effect On Cover Image",
    )
    Clear_Fix = blocks.BooleanBlock(
        required=False,
        null=True,
        blank=True,
        help_text="Pushes content Down instead of wraping around it",
    )
    def func(self):
        return str("<p>asdsadad</p>")
    class Meta:
        icon = "image"
        label = "Add Image Block"
        required = False
        block_counts = {"AltText": {"max_num": 1}, "position": {"max_num": 1}}
        template = "blocks/add_image.html"
        help_text = "ImageViaUrl will not be used if Image is provided unless overrided"
        value_class = AddImageValue
        closed = True

class CoverImageBlock(blocks.StructBlock):
    image = AddImage(
                        block_counts={
                            "Image": {"max_num": 1},
                            "ImageViaUrl": {"max_num": 1},
                            "AltText": {"max_num": 1},
                            "position": {"max_num": 1},
                        }
                    )

    class Meta:
        template='blocks/cover_image.html'

class BlogIndexPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    parent_page_types = [Page]
    subpage_types = [
        "blog.posts",
        "blog.CodingPost",
        "blog.NewsPost",
        "blog.GamingPost",
    ]


class Posts(Page):

    slug = "posts"

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    parent_page_types = ["blog.BlogIndexPage"]
    max_count = 1

    @property
    def template(self):
        return "blog/category.html"


class CodingPost(Page):

    slug = "coding"

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    parent_page_types = ["blog.BlogIndexPage"]
    max_count = 1

    @property
    def template(self):
        return "blog/category.html"


class NewsPost(Page):

    slug = "news"

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    parent_page_types = ["blog.BlogIndexPage"]
    max_count = 1

    @property
    def template(self):
        return "blog/category.html"


class GamingPost(Page):

    slug = "gaming"

    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by("-first_published_at")
        context["blogpages"] = blogpages
        return context

    parent_page_types = ["blog.BlogIndexPage"]
    max_count = 1

    @property
    def template(self):
        return "blog/category.html"


class BlogEntryPage(Page):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = ClusterTaggableManager(through=BlogEntryPageTag, blank=True)
    category = models.ForeignKey(
        "blog.BlogPageCategory",
        null=True,
        blank=False,
        default=1,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    body = StreamField(
        [
            ("Title", blocks.CharBlock(null=True, blank=False)),
            ("body", blocks.RichTextBlock(null=True, blank=True, closed=True)),
            ("image", AddImage(min_num=1, max_num=1, null=True, blank=True,)),
        ]
    )

    CoverImage = StreamField(
        blocks.StreamBlock(
            [
                (
                    "cover_image",
                    CoverImageBlock()
                ),
            ],
            max_num=1,
            min_num=1,
        ),
        verbose_name="Cover Image",
        
    )
    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("tags"), FieldPanel("category", widget=forms.RadioSelect)],
            heading="meta",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                StreamFieldPanel("CoverImage", classname="full"),
                StreamFieldPanel("body", classname="full"),
            ],
            heading="Main Content Of post",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                ReadOnlyPanel("created", classname="full"),
                ReadOnlyPanel("updated", classname="full"),
            ],
            "DateTimeField",
        ),
    ]

    parent_page_types = [
        "blog.Posts",
        "blog.CodingPost",
        "blog.NewsPost",
        "blog.GamingPost",
    ]

    def get_context(self, request):
        context = super().get_context(request)
        recents = []
        last = self.get_last_sibling()

        if last.specific != self:

            recents.append(self.get_last_sibling())
            recents.append(self.get_prev_sibling())
            recents.append(self.get_next_sibling())
        else:

            recents.append(self.get_prev_sibling())
            recents.append(self.get_next_sibling())
            recents.append(self.get_prev_sibling().get_prev_sibling())

        context["recents"] = recents
        return context

