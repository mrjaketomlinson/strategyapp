# Generated by Django 5.0.6 on 2024-07-20 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='is_chosen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='businessproblem',
            name='is_public',
            field=models.BooleanField(default=True, verbose_name='public'),
        ),
    ]
