# Generated by Django 4.2.5 on 2023-09-11 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='snippet',
            field=models.CharField(default='Click Link Above to Read Blog Post...', max_length=255),
        ),
    ]
