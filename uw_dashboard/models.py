from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from uw_dashboard.parser import Parser
from uw_dashboard.databaseReader import DatabaseReader

class Agencies(models.Model):
    agency_andar_number = models.IntegerField(default=0, primary_key=True)
    agency_name = models.CharField(max_length=128)


class Program(models.Model):
    agency_andar_number = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    prgrm_andar_year = models.CharField(max_length=128, primary_key=True)
    program_andar_number = models.IntegerField(default=0)
    program_name = models.CharField(max_length=128)
    grant_start_date = models.DateField()
    grant_end_date = models.DateField()
    program_description = models.CharField(max_length=300)
    program_planner = models.CharField(max_length=128)
    funds = models.CharField(max_length=128)
    focus_area = models.CharField(max_length=128)
    strategic_outcome = models.CharField(max_length=128)
    funding_stream = models.CharField(max_length=128)
    allocation = models.FloatField(default=0)
    year = models.IntegerField(default=2016)


class Target_Population(models.Model):
    prgrm_andar_year = models.ForeignKey(Program, on_delete=models.CASCADE)
    target_population = models.CharField(max_length=128)


class Geo_Focus_Area(models.Model):
    prgrm_andar_year = models.ForeignKey(Program, on_delete=models.CASCADE)
    city = models.CharField(max_length=150)
    percent_of_focus = models.IntegerField(default=0)
    level_name = models.CharField(max_length=150)
    city_grouping = models.CharField(max_length=150)


class Donor_Engagement(models.Model):
    prgrm_andar_year = models.ForeignKey(Program, on_delete=models.CASCADE)
    donor_engagement = models.CharField(max_length=128)


class Totals(models.Model):
    prgrm_andar_year = models.ForeignKey(Program, on_delete=models.CASCADE)
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
    prgrm_andar_year = models.ForeignKey(Program, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)
    element_name = models.CharField(max_length=128)
    specific_element = models.CharField(max_length=128)


class Location(models.Model):
    program_andar_number = models.IntegerField(default=0)
    program_name = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=128)
    website = models.CharField(max_length=128)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)


class Search_History(models.Model):
    focus_area = models.CharField(max_length=512)
    target_population = models.CharField(max_length=512)
    program_elements = models.CharField(max_length=512)
    city_groupings = models.CharField(max_length=512)
    geographic_focus_area = models.CharField(max_length=512)
    donor_engagement = models.CharField(max_length=512)
    money_invested= models.CharField(max_length=512)
    funding_year = models.CharField(max_length=512)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)


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
        if instance.is_staff:
            Profile.objects.create(user=instance, is_admin = True)
        else:
            Profile.objects.create(user=instance, is_admin = False)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Reporting_Service:
    
    def __init__(self, user):
        self.user = user

    def import_data(self, file, year, overwrite, type):
        file  = str(file)
        parser = Parser(file, year, overwrite, type)
        if parser.validate_file():
            parser.parse_file()
            parser.insert_file()
            return True
        else:
            return False

    def query_data(self, filters):
        # query the data
        dbReader = DatabaseReader(filters)
        results = dbReader.readData()
        return results

    def queryMap(self):
        postal_codes = []
        location_name = []
        program_names = []
        location_lat = []
        location_lon = []
        locations = Location.objects.all()
        for location in locations:
            postal_codes.append(str(location.postal_code))
            location_name.append(str(location.location))
            program_names.append(str(location.program_name))
            location_lat.append(str(location.latitude))
            location_lon.append(str(location.longitude))
        return [postal_codes, location_name, program_names, location_lat, location_lon]

    def create_dashboard(self):
        # call the dashboard generator
        return True

    def log_in(self, username, hashed_pass):
        return True

    def log_out(self):
        return True

