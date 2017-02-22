from __future__ import unicode_literals

from django.db import models

class Agencies(models.Model):
    agency_andar_number = models.IntegerField(default=0)
    agency_name = models.CharField(max_length=128)

class Program(models.Model):
    agency_andar_number = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    program_andar_number = models.IntegerField(default=0)
    program_name = models.CharField(max_length=128)
    grant_start_date = models.DateField()
    grant_end_date = models.DateField()
    program_discription = models.CharField(max_length=128)
    program_planner = models.CharField(max_length=128)
    funds = models.CharField(max_length=128)
    focus_area = models.CharField(max_length=128)
    strategic_outcome = models.CharField(max_length=128)
    funding_stream = models.CharField(max_length=128)
    allocation = models.IntegerField(max_length=128)
    year = models.IntegerField(default=2016)
    website = models.CharField(max_length=128)

class Target_Population(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    target_Population = models.CharField(max_length=128)

class Geo_Focus_Area(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    city = models.CharField(max_length=128)
    percent_of_focus = models.IntegerField(default=0)

class Doner_Engagement(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    doner_engagement = models.CharField(max_length=128)

class Totals(models.Model):
    program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
    early_years = models.IntegerField(default=0)
    middle_years = models.IntegerField(default=0)
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
    element_name = models.IntegerField(default=0)
    specific_element = models.IntegerField(default=0)

class Location(models.Model):
	program_andar_number = models.ForeignKey(Program, on_delete=models.CASCADE)
	location = models.CharField(max_length=128)
	postal_code = models.CharField(max_length=128)
