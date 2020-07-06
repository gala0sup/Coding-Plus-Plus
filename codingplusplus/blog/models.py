from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from .edit_handlers import ReadOnlyPanel



from django.utils.safestring import mark_safe


class BlogEntryPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogEntryPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

class AddImageValue(blocks.StructValue):
    def get_img_tag(self,extra_css=''):
        ImageUrl = self.get('Image').get_rendition("original").url
        ImageViaUrl = self.get('ImageViaUrl')
        ImageOverride =self.get('ImageOverride')
        AltText =self.get('AltText')
        if ImageOverride == False:
            return mark_safe(str(
                " src="+f'"{ImageUrl}"'+
                " alt="+f'"{AltText}"'
                ))
        else:
            return mark_safe(str(
                " src="+f'"{ImageViaUrl}"'+
                " alt="+f'"{AltText}"'
                ))            
                



class AddImage(blocks.StructBlock):
    Image = ImageChooserBlock(required=False,null=True,blank=True)
    ImageViaUrl = blocks.URLBlock(required=False,null=True,blank=True)
    ImageOverride = blocks.BooleanBlock(required=False,null=True,blank=True,help_text="Use Image Via url Instead of Image uploaded")
    AltText = blocks.TextBlock(required=False,null=True,blank=True)
    Position = blocks.ChoiceBlock(choices=[
        ('center','center'),
        ('top','top'),
        ('left','left'),
        ('right','right'),

    ],required=False,null=True,blank=True,help_text='No Effect On Cover Image')
    ClearFix = blocks.BooleanBlock(required=False,null=True,blank=True,help_text="Pushes content Down instead of wraping around it")


    class Meta:
        icon = 'image'
        label = "Add Image Block"
        required = False
        block_counts={
                        'AltText':{'max_num' : 1},
                        'position':{'max_num': 1}   
                    }
        template = "blocks\\add_image.html"
        help_text = "ImageViaUrl will not be used if Image is provided unless overrided"
        value_class = AddImageValue
        closed = True

class BlogIndexPage(Page):

    def get_context(self,request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context

    parent_page_types = []

class BlogEntryPage(Page):

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = ClusterTaggableManager(through=BlogEntryPageTag, blank=True)

    body = StreamField([
        ('Title',blocks.CharBlock(null=True,blank=False)),
        ('body',blocks.RichTextBlock(null=True,blank=True,closed=True)),
        ('image',AddImage(
                            min_num=1,
                            max_num=1,
                            null=True,
                            blank=True,
                        )
            )
    ])

    CoverImage = StreamField(
        blocks.StreamBlock([
        ('cover_image',AddImage(
                                block_counts=
                                {
                                    'Image':{'max_num':1},
                                    'ImageViaUrl':{'max_num':1},
                                    'AltText':{'max_num' : 1},
                                    'position':{'max_num': 1}
                                })
            )],max_num=1,min_num=1)
        ,verbose_name="Cover Image")


    content_panels = Page.content_panels + [
        MultiFieldPanel([
            StreamFieldPanel('CoverImage',classname='full'),
            StreamFieldPanel('body',classname='full')
        ],heading="Main Content Of post",
        classname="collapsible"
        ),

        MultiFieldPanel([
            FieldPanel("tags"),
            ReadOnlyPanel('created',classname='full'),
            ReadOnlyPanel('updated',classname='full'),
        ],'DateTimeField')

    ]
    
    parent_page_types = ['blog.BlogIndexPage']

    @property
    def template(self):
        ctemplate = "blog\\blog_entry_page_copy.html"
        return ctemplate