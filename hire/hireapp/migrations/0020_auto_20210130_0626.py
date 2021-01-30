# Generated by Django 3.1.5 on 2021-01-30 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hireapp', '0019_application_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=60)),
                ('time_sent', models.DateTimeField(auto_now_add=True)),
                ('time_read', models.DateTimeField(blank=True, null=True)),
                ('message', models.TextField()),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Messages',
        ),
    ]
