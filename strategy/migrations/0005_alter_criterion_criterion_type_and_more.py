# Generated by Django 5.0.6 on 2024-09-05 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0004_criterion_planningevent_criterionweight_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='criterion',
            name='criterion_type',
            field=models.CharField(choices=[('max', 'Maximize'), ('min', 'Minimize')], max_length=50),
        ),
        migrations.AlterField(
            model_name='planningevent',
            name='score_type',
            field=models.CharField(choices=[('individual', 'Individual'), ('team', 'Team')], max_length=50),
        ),
        migrations.AlterField(
            model_name='planningevent',
            name='score_value_type',
            field=models.CharField(choices=[('tshirt', 'T-shirt'), ('fibonacci', 'Fibonacci'), ('scale', '1-10 Scale')], max_length=50),
        ),
    ]
