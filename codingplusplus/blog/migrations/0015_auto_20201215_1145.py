# Generated by Django 3.0.7 on 2020-12-15 11:45

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_codingpost_gamingpost_newspost_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentrypage',
            name='CoverImage',
            field=wagtail.core.fields.StreamField([('cover_image', wagtail.core.blocks.StructBlock([('image', wagtail.core.blocks.StructBlock([('Image', wagtail.images.blocks.ImageChooserBlock(blank=True, null=True, required=False)), ('ImageViaUrl', wagtail.core.blocks.URLBlock(blank=True, null=True, required=False)), ('ImageOverride', wagtail.core.blocks.BooleanBlock(blank=True, help_text='Use Image Via url Instead of Image uploaded', null=True, required=False)), ('AltText', wagtail.core.blocks.TextBlock(blank=True, null=True, required=False)), ('Position', wagtail.core.blocks.ChoiceBlock(blank=True, choices=[('center', 'center'), ('top', 'top'), ('left', 'left'), ('right', 'right')], help_text='No Effect On Cover Image', null=True, required=False)), ('ClearFix', wagtail.core.blocks.BooleanBlock(blank=True, help_text='Pushes content Down instead of wraping around it', null=True, required=False))], block_counts={'AltText': {'max_num': 1}, 'Image': {'max_num': 1}, 'ImageViaUrl': {'max_num': 1}, 'position': {'max_num': 1}}))])), ('ScreenWidthCoverImage', wagtail.core.blocks.BooleanBlock(help_text='Cover Image Should Be of Screen Width', required=False))], verbose_name='Cover Image'),
        ),
    ]