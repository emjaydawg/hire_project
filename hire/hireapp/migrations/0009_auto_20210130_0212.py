# Generated by Django 3.1.5 on 2021-01-30 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hireapp', '0008_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Staff'), (2, 'Company Contact'), (3, 'Future Employee'), (4, 'Undefined Profile')], null=True),
        ),
    ]