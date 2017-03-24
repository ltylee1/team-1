# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-24 05:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agencies',
            fields=[
                ('agency_andar_number', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('agency_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='DatabaseReader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Donor_Engagement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_engagement', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Geo_Focus_Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=150)),
                ('percent_of_focus', models.IntegerField(default=0)),
                ('level_name', models.CharField(max_length=150)),
                ('city_grouping', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program_andar_number', models.IntegerField(default=0)),
                ('program_name', models.CharField(max_length=128)),
                ('location', models.CharField(max_length=128)),
                ('postal_code', models.CharField(max_length=128)),
                ('website', models.CharField(max_length=128)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_admin', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('prgrm_andar_year', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('program_andar_number', models.IntegerField(default=0)),
                ('program_name', models.CharField(max_length=128)),
                ('grant_start_date', models.DateField()),
                ('grant_end_date', models.DateField()),
                ('program_description', models.CharField(max_length=300)),
                ('program_planner', models.CharField(max_length=128)),
                ('funds', models.CharField(max_length=128)),
                ('focus_area', models.CharField(max_length=128)),
                ('strategic_outcome', models.CharField(max_length=128)),
                ('funding_stream', models.CharField(max_length=128)),
                ('allocation', models.FloatField(default=0)),
                ('year', models.IntegerField(default=2016)),
                ('agency_andar_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Agencies')),
            ],
        ),
        migrations.CreateModel(
            name='Program_Elements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('element_name', models.CharField(max_length=128)),
                ('specific_element', models.CharField(max_length=128)),
                ('prgrm_andar_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Search_History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('focus_area', models.CharField(max_length=512)),
                ('target_population', models.CharField(max_length=512)),
                ('program_elements', models.CharField(max_length=512)),
                ('city_groupings', models.CharField(max_length=512)),
                ('geographic_focus_area', models.CharField(max_length=512)),
                ('donor_engagement', models.CharField(max_length=512)),
                ('money_invested', models.CharField(max_length=512)),
                ('funding_year', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='Target_Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_population', models.CharField(max_length=128)),
                ('prgrm_andar_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Program')),
            ],
        ),
        migrations.CreateModel(
            name='Totals',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_clients', models.IntegerField(default=0)),
                ('early_years', models.IntegerField(default=0)),
                ('middle_years', models.IntegerField(default=0)),
                ('children', models.IntegerField(default=0)),
                ('seniors', models.IntegerField(default=0)),
                ('parent_caregivers', models.IntegerField(default=0)),
                ('families', models.IntegerField(default=0)),
                ('contacts', models.IntegerField(default=0)),
                ('meals_snacks', models.IntegerField(default=0)),
                ('counselling_sessions', models.IntegerField(default=0)),
                ('mentors_tutors', models.IntegerField(default=0)),
                ('workshops', models.IntegerField(default=0)),
                ('volunteers', models.IntegerField(default=0)),
                ('prgrm_andar_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Program')),
            ],
        ),
        migrations.AddField(
            model_name='geo_focus_area',
            name='prgrm_andar_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Program'),
        ),
        migrations.AddField(
            model_name='donor_engagement',
            name='prgrm_andar_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uw_dashboard.Program'),
        ),
    ]
