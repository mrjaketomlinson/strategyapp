# Generated by Django 5.0.6 on 2024-11-05 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strategy', '0008_alter_planningeventbusinessproblem_final_score'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planningeventproject',
            old_name='override_score',
            new_name='rank',
        ),
        migrations.RenameField(
            model_name='planningeventstrategy',
            old_name='override_score',
            new_name='rank',
        ),
        migrations.AlterField(
            model_name='planningeventproject',
            name='final_score',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='planningeventstrategy',
            name='final_score',
            field=models.FloatField(null=True),
        ),
    ]
