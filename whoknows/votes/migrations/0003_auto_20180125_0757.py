# Generated by Django 2.0.1 on 2018-01-25 07:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votes', '0002_auto_20180123_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vote',
            old_name='user',
            new_name='voter',
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together={('voter', 'object_id')},
        ),
    ]
