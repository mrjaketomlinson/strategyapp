import django
import os
import sys

sys.path.append("/app")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "strategyapp.settings")
django.setup()

from account.models import Organization, User, Team, TeamMember
from strategy.models import BusinessProblem, Assumption, Strategy


# Organization
print("Creating organization...")
org = Organization.objects.create(name="Bould", domain="bould.co")
print("Done.")

# Users
print("Creating users...")
user1 = User.objects.create_user(
    email="jacob.tomlinson21@gmail.com",
    first_name="Jacob",
    last_name="Tomlinson",
    password="super!Password",
)
user1.organization = org
user1.is_staff = True
user1.save()

user2 = User.objects.create_user(
    email="wgradle@gmail.com",
    first_name="Wil",
    last_name="Gradle",
    password="super!Password",
)
user2.organization = org
user2.is_staff = True
user2.save()

user3 = User.objects.create_user(
    email="mscott@gmail.com",
    first_name="Michael",
    last_name="Scott",
    password="super!Password",
)
user3.organization = org
user3.save()
print("Done.")

# Teams
print("Creating teams...")
team1 = Team.objects.create(name="Leadership", organization=org)
team2 = Team.objects.create(name="All", organization=org)
print("Done.")

# Members
print("Creating team members...")
members_by_user = {
    user1: [{"team": team1, "role": "Admin"}, {"team": team2, "role": "Admin"}],
    user2: [{"team": team1, "role": "Admin"}, {"team": team2, "role": "Admin"}],
    user3: [{"team": team2, "role": "Member"}],
}
for user, memberships in members_by_user.items():
    for membership in memberships:
        TeamMember.objects.create(
            user=user, team=membership.get("team"), role=membership.get("role")
        )
print("Done.")

# Business problems
print("Creating business problems...")
problem1 = BusinessProblem.objects.create(
    summary="""Recruiting and Retaining talent is extremely difficult 
        and is a constraint on revenue if we can't meet customer demand.""",
    description="",
    organization=org,
    created_by=user1,
    modified_by=user1,
)
problem1.teams.set([team1])
problem2 = BusinessProblem.objects.create(
    summary="""Customer satisfaction is super low and hurting the bottom 
        line because customers aren't returning to us.""",
    description="",
    organization=org,
    created_by=user2,
    modified_by=user2,
)
problem2.teams.set([team2])
print("Done.")

# Assumptions
print("Creating assumptions...")
assumption1 = Assumption.objects.create(
    summary="""Social stigmas toward working in the trades are shifting and 
        young people are more willing to skip college""",
    organization=org,
    created_by=user1,
    modified_by=user1,
    business_problem=problem1,
)
assumption2 = Assumption.objects.create(
    summary="""It is easier for the business to retain talent than it is to 
        recruit it - our machines have proprietary technology that are difficult 
        to learn.""",
    organization=org,
    created_by=user1,
    modified_by=user1,
    business_problem=problem1,
)
assumption3 = Assumption.objects.create(
    summary="""Older, more experienced technicians are beginning to retire, so 
        the problem is becoming increasingly existential""",
    organization=org,
    created_by=user1,
    modified_by=user1,
    business_problem=problem1,
)
print("Done.")

# Strategies
print("Creating strategies...")
strategy1 = Strategy.objects.create(
    summary="Build a technical school for the trades.",
    description="""The costs are high, but it will give us a space to recruit 
        new talent, upskill our existing talent, and potentially make our 
        cost-center (training) a profit center (charging tuition for students 
        that don't end up working for us)""",
    organization=org,
    created_by=user1,
    modified_by=user1,
)
strategy1.business_problems.set([problem1])
strategy2 = Strategy.objects.create(
    summary="Accept employee churn, aka do nothing",
    description="""We don't see a way to retain talent, and we are going to 
        live with it.""",
    organization=org,
    created_by=user1,
    modified_by=user1,
)
strategy2.business_problems.set([problem1])
strategy3 = Strategy.objects.create(
    summary="""Win-back program that gears all sales customer success to 
        existing customers""",
    description="""Create a program to win back customers at a discount and 
        ensure their success with a customer success led onboarding session.""",
    organization=org,
    created_by=user1,
    modified_by=user1,
)
strategy3.business_problems.set([problem2])
strategy4 = Strategy.objects.create(
    summary="The customer isn't always right, aka do nothing",
    description="""We don't want to deal with these silly customers.""",
    organization=org,
    created_by=user1,
    modified_by=user1,
)
strategy4.business_problems.set([problem2])
print("Done.")

print("Script complete.")
