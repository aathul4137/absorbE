# Generated by Django 5.0.6 on 2024-07-15 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adsorbEapp', '0003_homework'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='is_finesed',
            new_name='is_finised',
        ),
    ]
