# Generated by Django 4.1.1 on 2022-10-03 17:11

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('tasks', '0007_rutag_rutaggeditem_alter_todoitem_tags'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RuTag',
        ),
        migrations.DeleteModel(
            name='RuTaggedItem',
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]