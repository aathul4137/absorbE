# Generated by Django 5.0.6 on 2024-08-06 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsorbEapp', '0006_remove_homework_is_finished_todo'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='status',
            field=models.CharField(default='pending', max_length=20),
        ),
    ]