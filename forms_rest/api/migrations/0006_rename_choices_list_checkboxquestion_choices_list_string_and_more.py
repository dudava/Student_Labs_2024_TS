# Generated by Django 5.0.3 on 2024-03-31 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_checkboxquestion_choices_list_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkboxquestion',
            old_name='choices_list',
            new_name='choices_list_string',
        ),
        migrations.RenameField(
            model_name='radioquestion',
            old_name='choices_list',
            new_name='choices_list_string',
        ),
    ]