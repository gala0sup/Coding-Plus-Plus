# Generated by Django 3.0.7 on 2020-07-09 04:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20200709_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogentrypage',
            name='category',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='blog.BlogPageCategory'),
        ),
    ]
