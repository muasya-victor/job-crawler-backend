# Generated by Django 5.0.3 on 2024-03-08 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_scraper_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='job_level',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
