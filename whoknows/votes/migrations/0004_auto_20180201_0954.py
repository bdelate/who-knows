# Generated by Django 2.0.1 on 2018-02-01 09:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('votes', '0003_auto_20180125_0757'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('voter', 'content_type', 'object_id')},
        ),
    ]
