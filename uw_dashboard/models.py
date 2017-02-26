from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv


class Agencies(models.Model):
    agency_andar_number = models.IntegerField(default=0, primary_key=True)
    agency_name = models.CharField(max_length=128)


class Program(models.Model):
    agency_andar_number = models.ForeignKey(Agencies, on_delete=models.CASCADE)
    program_andar_number = models.IntegerField(default=0, primary_key=True)
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
    program_andar_number = models.IntegerField(default=0)
    location = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=128)
    website = models.CharField(max_length=128)


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


class Parser:

    def __init__(self, cur_file, year, overwrite):
        self.cur_file = cur_file
        self.year = year
        self.overwrite = overwrite

        self.content = []
        self.column_names = []
        self.output_index = {
            'Funds': -1,
            'Focus Area': -1,
            'Strategic Outcome': -1,
            'Funding stream': -1,
            'Agency Andar #': -1,
            'Agency Name': -1,
            'Program Andar #': -1,
            'Program Name': -1,
            'Allocation': -1,
            'Grant Start Date': -1,
            'Grant End Date': -1,
            'Short Program Description': -1,
            'Planner': -1,
            'Target Population': -1,
            'TP Other': -1,
            'Program Elements': -1,
            'PE End': -1,
            'Geographic Focus Area': -1,
            'GFA Other': -1,
            'Donor Engagement': -1,
            'DE Other': -1,
            'Outputs': -1,
            'Outputs End': -1
        }
        self.postal_index = {
                'Agency Andar #': -1,
                'Agency Name': -1,
                'Program Andar #': -1,
                'Program Name': -1,
                'Website': -1,
                'Description': -1,
                '# Locations': -1,
                'Postal Code': -1
            }

    # Gets the core indexes for the postal file
    def get_postal_index(self, column_list, sheet_name):
        if 'program' in sheet_name:
            for column in column_list:
                if 'Agency Andar #' == column:
                    self.postal_index['Agency Andar #'] = column_list.index(column)
                elif 'Agency Name' == column:
                    self.postal_index['Agency Name'] = column_list.index(column)
                elif 'Program Andar #' == column:
                    self.postal_index['Program Andar #'] = column_list.index(column)
                elif 'Program Name' == column:
                    self.postal_index['Program Name'] = column_list.index(column)
                elif 'Website' == column:
                    self.postal_index['Website'] = column_list.index(column)
                elif 'Description' == column:
                    self.postal_index['Description'] = column_list.index(column)
                elif '# Locations' == column:
                    self.postal_index['# Locations'] = column_list.index(column)

        elif 'agency' in sheet_name:
            for column in column_list:
                if 'Agency Andar #' == column:
                    self.postal_index['Agency Andar #'] = column_list.index(column)
                elif 'Agency Name' == column:
                    self.postal_index['Agency Name'] = column_list.index(column)
                elif 'Program Andar #' == column:
                    self.postal_index['Program Andar #'] = column_list.index(column)
                elif 'Program Name' == column:
                    self.postal_index['Program Name'] = column_list.index(column)
                elif 'Postal Code' == column:
                    self.postal_index['Postal Code'] = column_list.index(column)

    # Gets the core indexes for the output file
    def get_output_index(self, column_list):
        if len(column_list) != 158:
            print "Columns have been removed or added, system may not work"
        for column in column_list:
            if "Funds" == column:
                self.output_index['Funds'] = column_list.index(column)
            elif "Focus Area" == column:
                self.output_index['Focus Area'] = column_list.index(column)
            elif "Strategic Outcome" == column:
                self.output_index['Strategic Outcome'] = column_list.index(column)
            elif "Funding Stream" == column:
                self.output_index['Funding stream'] = column_list.index(column)
            elif "Agency Andar #" == column:
                self.output_index['Agency Andar #'] = column_list.index(column)
            elif "Agency Name" == column:
                self.output_index['Agency Name'] = column_list.index(column)
            elif "Program Name" == column:
                self.output_index['Program Name'] = column_list.index(column)
            elif "Program Andar #" == column:
                self.output_index['Program Andar #'] = column_list.index(column)
            elif "Allocation" in column:
                self.output_index['Allocation'] = column_list.index(column)
            elif "Grant Start Date" == column:
                self.output_index['Grant Start Date'] = column_list.index(column)
            elif "Grant End Date" == column:
                self.output_index['Grant End Date'] = column_list.index(column)
            elif "Short Program Description" == column:
                self.output_index['Short Program Description'] = column_list.index(column)
            elif "Planner" == column:
                self.output_index['Planner'] = column_list.index(column)
            elif "Target Population" == column:
                self.output_index['Target Population'] = column_list.index(column)
            elif self.output_index['Target Population'] != -1 and self.output_index['Program Elements'] == -1 and "Other" == column:
                self.output_index['TP Other'] = column_list.index(column)
            elif "Program Elements" == column:
                self.output_index['Program Elements'] = column_list.index(column)
            elif "Information and Referral" == column:
                self.output_index['PE End'] = column_list.index(column)
            elif "Geographic Focus Area" == column:
                self.output_index['Geographic Focus Area'] = column_list.index(column)
            elif "Other Areas" == column:
                self.output_index['GFA Other'] = column_list.index(column) + 1
            elif "Donor Engagement" == column:
                self.output_index['Donor Engagement'] = column_list.index(column)
            elif self.output_index['Donor Engagement'] != -1 and self.output_index['Outputs'] == -1 and "Other" == column:
                self.output_index['DE Other'] = column_list[self.output_index['Donor Engagement']:].index(column) + self.output_index['Donor Engagement']
            elif "Outputs" == column:
                self.output_index['Outputs'] = column_list.index(column)

        self.output_index['Outputs End'] = len(column_list) - 1

    def drop_program_table(self):
        Program.objects.filter(year=self.year).delete()

    def drop_location_table(self):
        Location.objects.all().delete()

    def insert_row(self, row):
        self.insert_agency(row)
        self.insert_program(row)
        self.insert_donor_engagement(row)
        self.insert_totals(row)
        self.insert_target_population(row)
        self.insert_geo_focus(row)
        self.insert_program_elements(row)

    # Collapses binary columns and returns them as a list of column names
    def collapse_binary(self, row, start, end):
        collapsed_columns = []
        for curindex in range(start, end):
            if row[curindex] == '1':
                collapsed_columns.append(self.column_names[curindex])
        return collapsed_columns

    # Used for debugging
    def get_table_row(self, row, index, end_index):
        index = self.output_index[index]
        start = index + 1
        end = self.output_index[end_index] + 1
        table_row = []
        for x in range(start, end):
            table_row.append(row[x])
        return table_row

    # Checks that the cell isn't empty
    def check_empty(self, value):
        if value == '':
            return 0
        else:
            return value

    # Gets all the locations(name, postal code) for a program
    def get_locations(self, row):
        index = self.postal_index['# Locations']
        locations = []
        if row[index] != "None" and row[index] != '':
            for num in range(0, int(row[index])):
                location = row[(index + num * 2) + 1]
                postcode = row[(index + num * 2) + 2]
                locations.append([location, postcode])
        return locations

    # Inserts target population into database
    def insert_target_population(self, row):
        collapsed_row = self.collapse_binary(row, self.output_index['Target Population'] + 1,
                                             self.output_index['TP Other'] + 1)
        program = Program.objects.get(program_andar_number=row[self.output_index['Program Andar #']])
        if collapsed_row:
            for current_population in collapsed_row:
                check = Target_Population.objects.filter(program_andar_number=program,
                                                         target_population=current_population).exists()
                if not check:
                    target = Target_Population(program_andar_number=program,
                                               target_population=current_population)
                    target.save()

    # TODO NOTE DOES NOT DEAL WITH First Nation Territories CD
    # Inserts geographical focus area into database
    def insert_geo_focus(self, row):
        program = Program.objects.get(program_andar_number=row[self.output_index['Program Andar #']])
        for curindex in range(self.output_index['Geographic Focus Area'] + 2, self.output_index['GFA Other']):
            curcity = self.column_names[curindex]
            curpercent = self.check_empty(row[curindex])
            if curpercent != 0:
                check = Geo_Focus_Area.objects.filter(program_andar_number=program, city=curcity).exists()
                if not check:
                    focus = Geo_Focus_Area(program_andar_number=program,
                                           city=curcity,
                                           percent_of_focus=curpercent)
                    focus.save()
                    # else:
                    #     print 'If we wanted to update during appends we would do it here'

    # Inserts donor engagements into database
    def insert_donor_engagement(self, row):
        collapsed_row = self.collapse_binary(row, self.output_index['Donor Engagement'] + 1,
                                             self.output_index['DE Other'] + 1)
        program = Program.objects.get(program_andar_number=row[self.output_index['Program Andar #']])
        if collapsed_row:
            for current_donor in collapsed_row:
                check = Donor_Engagement.objects.filter(program_andar_number=program,
                                                        donor_engagement=current_donor).exists()
                if not check:
                    donor = Donor_Engagement(program_andar_number=program,
                                             donor_engagement=current_donor)
                    donor.save()
                    # else:
                    #     print 'If we wanted to update during appends we would do it here'

    # Inserts totals into the database
    def insert_totals(self, row):
        start = self.output_index['Outputs'] + 1
        program = Program.objects.get(program_andar_number=row[self.output_index['Program Andar #']])
        check = Totals.objects.filter(program_andar_number=program).exists()
        if not check:
            total = Totals(program_andar_number=program,
                           total_clients=self.check_empty(row[start]),
                           early_years=self.check_empty(row[start + 1]),
                           middle_years=self.check_empty(row[start + 2]),
                           children=self.check_empty(row[start + 3]),
                           seniors=self.check_empty(row[start + 4]),
                           parent_caregivers=self.check_empty(row[start + 5]),
                           families=self.check_empty(row[start + 6]),
                           contacts=self.check_empty(row[start + 7]),
                           meals_snacks=self.check_empty(row[start + 8]),
                           counselling_sessions=self.check_empty(row[start + 9]),
                           mentors_tutors=self.check_empty(row[start + 10]),
                           workshops=self.check_empty(row[start + 11]),
                           volunteers=self.check_empty(row[start + 12]))
            total.save()
            # else:
            #     print 'Exists and if we wanted to update we would do that here'

    # Inserts program element into database
    def insert_program_elements(self, row):
        temp = []
        colnames = []
        # Gets the column index for the Program Element Levels
        for curindex in range(self.output_index['Program Elements'] + 1, self.output_index['PE End'] + 1):
            if row[curindex] != '' and row[curindex] != '1':
                colname = self.column_names[curindex]
                colnames.append(colname)
                temp.append(curindex)
        # For each level
        for curindex in range(0, len(colnames) - 1):
            # Collapse the binary column
            cursection = (self.collapse_binary(row, temp[curindex], temp[curindex + 1]))
            if cursection:
                level = row[temp[curindex]]
                element_name = colnames[curindex]
                specific_element = cursection
                program = Program.objects.get(program_andar_number=row[self.output_index['Program Andar #']])
                for curelement in specific_element:
                    check = Program_Elements.objects.filter(program_andar_number=program,
                                                            level=level,
                                                            element_name=element_name,
                                                            specific_element=curelement).exists()
                    if not check:
                        element = Program_Elements(program_andar_number=program,
                                                   level=level,
                                                   element_name=element_name,
                                                   specific_element=curelement)
                        element.save()
                        # else:
                        #     print 'Exists and if we wanted to update we would do that here'

    # Should only need to insert since program table will be dropped if overwrite; during append we should just update if there are no tables existing
    def insert_program(self, row):
        check = Program.objects.filter(program_andar_number=row[self.output_index['Program Andar #']]).exists()
        if not check:
            agency = Agencies.objects.get(agency_andar_number=row[self.output_index['Agency Andar #']])
            date = row[self.output_index['Grant Start Date']]
            start_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            date = row[self.output_index['Grant End Date']]
            end_date = date[:4] + '-' + date[4:6] + '-' + date[6:]
            program = Program(agency_andar_number=agency,
                              program_andar_number=row[self.output_index['Program Andar #']],
                              program_name=row[self.output_index['Program Name']],
                              grant_start_date=start_date,
                              grant_end_date=end_date,
                              program_description=row[self.output_index['Short Program Description']],
                              program_planner=row[self.output_index['Planner']],
                              funds=row[self.output_index['Funds']],
                              focus_area=row[self.output_index['Focus Area']],
                              strategic_outcome=row[self.output_index['Strategic Outcome']],
                              funding_stream=row[self.output_index['Funding stream']],
                              allocation=row[self.output_index['Allocation']],
                              year=self.year)
            program.save()
            # else:
            # print 'Exists and if we wanted to update we would do that here'

    # Inserts agency data into the database, this is the only table that is never dropped.
    def insert_agency(self, row):
        check = Agencies.objects.filter(agency_andar_number=row[self.output_index['Agency Andar #']]).exists()
        # Agency already exists if we are overwriting so we update the agency name if needed
        if check:
            if self.overwrite:
                agency = Agencies.objects.get(agency_andar_number=row[self.output_index['Agency Andar #']])
                cur_agency = row[self.output_index['Agency Name']]
                if agency.agency_name != cur_agency:
                    agency.agency_name = cur_agency
                    agency.save()
        else:
            # If agency does not exists then we create it in database
            agency = Agencies(agency_andar_number=row[self.output_index['Agency Andar #']],
                              agency_name=row[self.output_index['Agency Name']])
            agency.save()

    # Inserts program location data into database
    def insert_program_location(self, row):
        locations = self.get_locations(row)
        for location in locations:
            loc_name = location[0]
            loc_post = location[1]
            # Check that the location is not empty
            if loc_name != 'None' and loc_name != '':
                # Check that location does not already exist
                check = Location.objects.filter(program_andar_number=row[self.postal_index['Program Andar #']], location=loc_name,
                                                postal_code=loc_post).exists()
                # Insert data into database
                if not check:
                    loc = Location(program_andar_number=row[self.postal_index['Program Andar #']],
                                   location=loc_name,
                                   postal_code=loc_post,
                                   website=row[self.postal_index['Website']])
                    loc.save()
                    # else:
                    #     print 'Exists and if we wanted to update we would do that here'

    # Checks that the file is a CSV
    def validate_file(self):
        pfile = self.cur_file
        if pfile.endswith('.csv'):
            return True
        else:
            return False

    # Inserts the parsed contents into the database
    def insert_file(self):
        if self.content:
            if "outputs" in self.cur_file.lower():
                if self.overwrite:
                    self.drop_program_table()
                for row in self.content:
                    self.insert_row(row)
            elif "postal" in self.cur_file.lower():
                if self.overwrite:
                    self.drop_location_table()
                for row in self.content:
                    self.insert_program_location(row)
        else:
            raise Exception("Nothing to insert")

    # Parses the file
    def parse_file(self):
        pfile = self.cur_file
        if "outputs" in pfile.lower():
            with open(pfile, 'rb') as f:
                reader = csv.reader(f)
                self.column_names = reader.next()
                self.get_output_index(self.column_names)
                for row in reader:
                    self.content.append(row)

        elif "postal" in pfile.lower():
            with open(pfile, 'rb') as f:
                reader = csv.reader(f)
                self.column_names = reader.next()
                self.get_postal_index(self.column_names, 'program')
                for row in reader:
                    self.content.append(row)
