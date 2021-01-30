# Generated by Django 3.1.5 on 2021-01-30 05:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hireapp', '0011_auto_20210130_0457'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='company',
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.RESTRICT, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='score',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)]),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='HiringManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='hireapp.company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
