# Generated by Django 2.0.1 on 2018-01-23 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0005_tag_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='votes',
        ),
    ]
