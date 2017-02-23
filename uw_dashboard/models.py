from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Agencies(models.Model):
    agency_andar_number = models.IntegerField(default=0, primary_key=True)
    agency_name = models.CharField(max_length=128)


class Program(models.Model):
    agency_andar_number = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    program_andar_number = models.IntegerField(default=0, primary_key=True)
    program_name = models.CharField(max_length=128)
    grant_start_date = models.DateField()
    grant_end_date = models.DateField()
    program_description = models.CharField(max_length=128)
    program_planner = models.CharField(max_length=128)
    funds = models.CharField(max_length=128)
    focus_area = models.CharField(max_length=128)
    strategic_outcome = models.CharField(max_length=128)
    funding_stream = models.CharField(max_length=128)
    allocation = models.FloatField(default=0)
    year = models.IntegerField(default=2016)
    website = models.CharField(max_length=128)


class Target_Population(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    target_population = models.CharField(max_length=128)


class Geo_Focus_Area(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    percent_of_focus = models.IntegerField(default=0)


class Donor_Engagement(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    donor_engagement = models.CharField(max_length=128)


class Totals(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    total_clients = models.IntegerField(default=0)
    early_years = models.IntegerField(default=0)
    middle_years = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    seniors = models.IntegerField(default=0)
    parent_caregivers = models.IntegerField(default=0)
    families = models.IntegerField(default=0)
    contacts = models.IntegerField(default=0)
    meals_snacks = models.IntegerField(default=0)
    counselling_sessions = models.IntegerField(default=0)
    mentors_tutors = models.IntegerField(default=0)
    workshops = models.IntegerField(default=0)
    volunteers = models.IntegerField(default=0)


class Program_Elements(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    element_name = models.CharField(max_length=128)
    specific_element = models.CharField(max_length=128)


class Location(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    location = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=128)


# Separate table for extra user information we need that is not used for authentication
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def username(self):
        return self.user.get_username()

    def password(self):
        return self.user.password

    def email(self):
        return self.user.email

    def change_password(self, password):
        self.user.set_password(password)
        self.user.save()

    def addUser(self, email, username, password):
        user = User.objects.create_user(username, email, password)
        user.save()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()





