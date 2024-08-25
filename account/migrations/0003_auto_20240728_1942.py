# Generated by Django 5.0.6 on 2024-07-28 19:37

from django.db import migrations


def fill_team_users(apps, schema_editor):
    Team = apps.get_model("account", "Team")
    for team in Team.objects.all():
        team.created_by = team.organization.user_set.first()
        team.modified_by = team.organization.user_set.first()
        team.save()

def reverse_fill_team_users(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_team_created_by_team_modified_by'),
    ]

    operations = [
        migrations.RunPython(fill_team_users, reverse_fill_team_users)
    ]