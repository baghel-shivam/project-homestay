# Generated by Django 3.2.6 on 2024-03-09 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_auto_20240309_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='about_this_room',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]
