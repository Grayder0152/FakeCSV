# Generated by Django 3.2.6 on 2021-08-17 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='column',
            old_name='type',
            new_name='column_type',
        ),
    ]