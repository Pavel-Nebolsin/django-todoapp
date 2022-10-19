# Generated by Django 4.1.1 on 2022-10-14 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_delete_rutag_delete_rutaggeditem_alter_todoitem_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_slug', models.CharField(max_length=128)),
                ('tag_name', models.CharField(max_length=128)),
                ('tag_id', models.PositiveIntegerField(default=0)),
                ('tag_count', models.PositiveIntegerField(db_index=True, default=0)),
            ],
        ),
    ]
