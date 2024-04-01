# Generated by Django 5.0.3 on 2024-03-31 19:15

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_checkboxquestion_radioquestion_textquestion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkboxquestion',
            name='choices_list',
            field=models.CharField(max_length=300, validators=[api.models.MultipleChoicesQuestion.validate_list]),
        ),
        migrations.AlterField(
            model_name='radioquestion',
            name='choices_list',
            field=models.CharField(max_length=300, validators=[api.models.MultipleChoicesQuestion.validate_list]),
        ),
    ]
