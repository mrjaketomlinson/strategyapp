# Generated by Django 5.0.6 on 2024-11-24 22:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_timeperiod'),
        ('strategy', '0009_rename_override_score_planningeventproject_rank_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='strategy',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='strategy_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='planningevent',
            name='scoring_team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.team'),
        ),
        migrations.AlterField(
            model_name='planningevent',
            name='scoring_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
