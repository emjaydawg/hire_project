# Generated by Django 3.1.5 on 2021-01-30 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hireapp', '0004_job_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='slug',
            field=models.SlugField(default='', editable=False, max_length=116, unique=True),
        ),
    ]
