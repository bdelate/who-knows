# Generated by Django 2.0.1 on 2018-03-09 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_remove_question_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_views',
            field=models.IntegerField(default=0),
        ),
    ]
