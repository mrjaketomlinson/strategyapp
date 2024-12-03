# Generated by Django 5.0.6 on 2024-12-03 03:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_project_owner'),
        ('strategy', '0011_alter_strategy_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='strategy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', related_query_name='project', to='strategy.strategy'),
        ),
    ]
