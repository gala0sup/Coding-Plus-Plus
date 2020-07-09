# Generated by Django 3.0.7 on 2020-07-06 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200706_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogentrypage',
            name='templates',
            field=models.CharField(choices=[('blog/blog_entry_page.html', 'Stable template'), ('blog/blog_entry_page_exp.html', 'unstable template')], default='blog/blog_entry_page.html', max_length=255),
        ),
    ]