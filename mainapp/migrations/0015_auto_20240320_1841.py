# Generated by Django 3.2.6 on 2024-03-20 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0014_auto_20240320_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetail',
            name='booking_id',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='nearest_attraction_1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='nearest_attraction_2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]