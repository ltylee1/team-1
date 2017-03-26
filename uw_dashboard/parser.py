import csv
import models
import requests


class Parser:
    existingInstances = []

    def __init__(self, cur_file, year, overwrite, file_type):
        if isinstance(cur_file, str) and isinstance(year, int) and isinstance(overwrite, bool) and isinstance(file_type,
                                                                                                              str):
            self.cur_file = cur_file
            self.year = year
            self.overwrite = overwrite
            self.type = file_type
            # Add to existing instances and determine if there is currently a user updating the db
            if self.type == 'output':
                if self.overwrite and self.year in self.existingInstances:
                    self.existingInstances.append(self.year)
                    raise Exception("Error in overwriting: Existing user is updating database, unable to overwrite")
                else:
                    self.existingInstances.append(self.year)
            elif self.type == 'postal':
                if self.overwrite and self.type in self.existingInstances:
                    self.existingInstances.append(self.type)
                    raise Exception("Error in overwriting: Existing user is updating database, unable to overwrite")
                else:
                    self.existingInstances.append(self.type)
        else:
            if not isinstance(year, int):
                raise Exception("Error in parsing: Year input is invalid")
            if not isinstance(overwrite, bool):
                raise Exception("Error in parsing: Overwrite input is invalid")
            if not isinstance(file_type, str):
                raise Exception("Error in parsing: Type input is invalid")
            raise Exception("Error in parsing: File input is invalid")

        self.content = []
        self.column_names = []
        self.output_index = {
            'Funds': -1,
            'Focus Area': -1,
            'Strategic Outcome': -1,
            'Funding Stream': -1,
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

    def __del__(self):
        # Remove from existingInstances
        try:
            if self.type == 'output' and self.year in self.existingInstances:
                self.existingInstances.remove(self.year)
            elif self.type == 'postal' and self.type in self.existingInstances:
                self.existingInstances.remove(self.type)
        except Exception:
            pass

    # Gets the core indexes for the postal file
    def get_postal_index(self, column_list):
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

    # Gets the core indexes for the output file
    def get_output_index(self, column_list):
        for column in column_list:
            if "Funds" == column:
                self.output_index['Funds'] = column_list.index(column)
            elif "Focus Area" == column:
                self.output_index['Focus Area'] = column_list.index(column)
            elif "Strategic Outcome" == column:
                self.output_index['Strategic Outcome'] = column_list.index(column)
            elif "Funding Stream" == column:
                self.output_index['Funding Stream'] = column_list.index(column)
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
                self.output_index['DE Other'] = column_list[self.output_index['Donor Engagement']:].index(column) + \
                                                self.output_index['Donor Engagement']
            elif "Outputs" == column:
                self.output_index['Outputs'] = column_list.index(column)

        self.output_index['Outputs End'] = len(column_list) - 1

    # Drops the part of the program table corresponding to the year
    def drop_program_table(self):
        models.Program.objects.filter(year=self.year).delete()

    # Drops the entire location table
    def drop_location_table(self):
        models.Location.objects.all().delete()

    # Inserts data into the database
    def insert_data(self):
        self.insert_agency()
        self.insert_program()
        self.insert_donor_engagement()
        self.insert_totals()
        self.insert_target_population()
        self.insert_geo_focus()
        self.insert_program_elements()

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

    def get_counts(self):
        cur_counts = {}
        if self.type == 'output':
            cur_counts = {'agencies': models.Agencies.objects.all().count(),
                          'program': models.Program.objects.all().count(),
                          'donor': models.Donor_Engagement.objects.all().count(),
                          'totals': models.Totals.objects.all().count(),
                          'target': models.Target_Population.objects.all().count(),
                          'gfa': models.Geo_Focus_Area.objects.all().count(),
                          'pe': models.Program_Elements.objects.all().count()}
        elif self.type == 'postal':
            cur_counts = {'locations': models.Location.objects.all().count()}

        return cur_counts

    def generate_primary_key(self, program_andar_number, year):
        andar = str(program_andar_number)
        year = str(year)
        return andar + year

    # Gets all the locations(name, postal code) for a program
    def get_locations(self, row):
        index = self.postal_index['# Locations']
        locations = []
        if row[index] != "None" and row[index] != '':
            for num in range(0, int(row[index])):
                location = row[(index + num * 2) + 1]
                postcode = row[(index + num * 2) + 2]
                if postcode != '':
                    check = models.Location.objects.filter(
                            location=location,
                            postal_code=postcode).exists()
                    if not check:
                        # try:
                        params = {'address': str(postcode)}
                        url = 'https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyAuvN-VnGnbsgVsF5aDaNtlmqWisnJ0AoE&address=' + str(
                            postcode + ',ca')
                        r = requests.get(url, params=params)
                        results = r.json()['results']
                        glocation = results[0]['geometry']['location']
                        address = results[0]['formatted_address']
                        # Temp fix for google api not being able to query properly
                        if '0' in postcode[4]:
                            result = address.split('BC ', 1)
                            address = result[0]+'BC '+postcode+', Canada'
                        locations.append([location, postcode, glocation['lat'], glocation['lng'], address])
                    # print(str(glocation['lat']) + "," + str(glocation['lng']))
                # except IndexError, e:
                #     print("Can't geocode" + str(postcode))
        return locations

    def get_city_grouping(self, city):
        first_nation_territories = ['First Nation Territories', 'Tsawwassen First Nation',
                                    'Sechelt Indian Government District (Part-Sunshine Coast)']
        fraser_cascade = ['Mission', 'Hope', 'Kent', 'Harrison Hot Springs', 'Boston Bar / North Bend',
                          'Dogwood Valley / Emory Creek / Choate / Sunshine Valley / Laidlaw / Spuzzum',
                          'Lake Errock / Harrison Mills / Hemlock Valley,Popkum / Bridal Falls',
                          'Slesse Park / Baker Trails / Bell Acres,Miracle Valley / Hatzic Prairie']
        langley = ['Langley, City of', 'Langley, District Municipality']
        maple_ridge = ['Maple Ridge', 'Pitt Meadows']
        northshore = ['North Vancouver, City of', 'North Vancouver, District Municipality', 'West Vancouver',
                      'Bowen Island']
        sea_to_sky = ['Lions Bay', 'Lillooet', 'Pemberton', 'Squamish', 'Whistler']
        sunshine_coast = ['Elphinstone', 'Gibsons', 'Halfmoon Bay', 'Pender Harbour / Egmont / Madeira Park',
                          'Roberts Creek', 'Sechelt District Municipality',
                          'Sechelt Indian Government District (Part-Sunshine Coast)',
                          "West Howe Sound (Langdale, Port Mellon, Williamson's Landing, Granthams Landing, Soames, Hopkins Landing, and Gambier and Keats Islands)",
                          "West Howe Sound (Langdale, Port Mellon, Williamson?s Landing, Granthams Landing, Soames, Hopkins Landing, and Gambier and Keats Islands)"]
        surrey = ['Surrey', 'White Rock']
        tri_cities = ['Anmore', 'Belcarra', 'Coquitlam', 'Port Coquitlam', 'Port Moody']
        other_areas = ['Other Areas']

        if city in first_nation_territories:
            return 'First Nation Territories'
        elif city in fraser_cascade:
            return 'Fraser Cascade'
        elif city in langley:
            return 'Langley'
        elif city in maple_ridge:
            return 'Maple Ridge/Pitt Meadows'
        elif city in northshore:
            return 'Northshore'
        elif city in other_areas:
            return 'Other Areas in BC'
        elif city in sea_to_sky:
            return 'Sea to Sky'
        elif city in sunshine_coast:
            return 'Sunshine Coast'
        elif city in surrey:
            return 'Surrey/White Rock'
        elif city in tri_cities:
            return 'Tri-cities'
        else:
            return city

    # Inserts target population into database
    def insert_target_population(self):
        target_list = []
        for row in self.content:
            collapsed_row = self.collapse_binary(row, self.output_index['Target Population'] + 1,
                                                 self.output_index['TP Other'] + 1)
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
            program = models.Program.objects.get(prgrm_andar_year=andar_year)
            if collapsed_row:
                for current_population in collapsed_row:
                    check = models.Target_Population.objects.filter(prgrm_andar_year=program,
                                                                    target_population=current_population).exists()
                    if not check:
                        target = models.Target_Population(prgrm_andar_year=program,
                                                          target_population=current_population)
                        if target not in target_list:
                            target_list.append(target)
        models.Target_Population.objects.bulk_create(target_list)

    # Inserts geographical focus area into database
    def insert_geo_focus(self):
        colnames = ['First Nation Territories', 'Fraser Valley Regional District', 'Metro Vancouver Regional District',
                    'Squamish-Lillooet Regional District', 'Sunshine Coast Regional District', 'Other Areas']
        focus_list = []
        for row in self.content:
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
            temp = []
            for col in colnames:
                temp.append(self.column_names.index(col))
            temp.append(self.output_index['GFA Other'] + 1)
            program = models.Program.objects.get(prgrm_andar_year=andar_year)
            for index in range(0, len(colnames)):
                for curindex in range(temp[index] + 1, temp[index + 1]):
                    level = self.column_names[temp[index]]
                    curcity = self.column_names[curindex]
                    citygrouping = self.get_city_grouping(curcity)
                    curpercent = self.check_empty(row[curindex])
                    if curpercent != 0:
                        check = models.Geo_Focus_Area.objects.filter(prgrm_andar_year=program, city=curcity).exists()
                        if not check:
                            focus = models.Geo_Focus_Area(prgrm_andar_year=program,
                                                          city=curcity,
                                                          percent_of_focus=curpercent,
                                                          level_name=level,
                                                          city_grouping=citygrouping)
                            if focus not in focus_list:
                                focus_list.append(focus)
        models.Geo_Focus_Area.objects.bulk_create(focus_list)

    # Inserts donor engagements into database
    def insert_donor_engagement(self):
        de_list = []
        for row in self.content:
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
            collapsed_row = self.collapse_binary(row, self.output_index['Donor Engagement'] + 1,
                                                 self.output_index['DE Other'] + 1)
            program = models.Program.objects.get(prgrm_andar_year=andar_year)
            if collapsed_row:
                for current_donor in collapsed_row:
                    check = models.Donor_Engagement.objects.filter(prgrm_andar_year=program,
                                                                   donor_engagement=current_donor).exists()
                    if not check:
                        donor = models.Donor_Engagement(prgrm_andar_year=program,
                                                        donor_engagement=current_donor)
                        if donor not in de_list:
                            de_list.append(donor)
        models.Donor_Engagement.objects.bulk_create(de_list)

    # Inserts totals into the database
    def insert_totals(self):
        totals_list = []
        for row in self.content:
            start = self.output_index['Outputs'] + 1
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
            program = models.Program.objects.get(prgrm_andar_year=andar_year)
            check = models.Totals.objects.filter(prgrm_andar_year=program).exists()
            if not check:
                total = models.Totals(prgrm_andar_year=program,
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
                if total not in totals_list:
                    totals_list.append(total)
        models.Totals.objects.bulk_create(totals_list)

    # Inserts program element into database
    def insert_program_elements(self):
        pe_list = []
        for row in self.content:
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
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
                    program = models.Program.objects.get(prgrm_andar_year=andar_year)
                    for curelement in specific_element:
                        check = models.Program_Elements.objects.filter(prgrm_andar_year=program,
                                                                       level=level,
                                                                       element_name=element_name,
                                                                       specific_element=curelement).exists()
                        if not check:
                            element = models.Program_Elements(prgrm_andar_year=program,
                                                              level=level,
                                                              element_name=element_name,
                                                              specific_element=curelement)
                            if element not in pe_list:
                                pe_list.append(element)
        models.Program_Elements.objects.bulk_create(pe_list)

    # Should only need to insert since program table will be dropped if overwrite; during append we should just update if there are no tables existing
    def insert_program(self):
        program_list = []
        for row in self.content:
            andar = row[self.output_index['Program Andar #']]
            andar_year = self.generate_primary_key(andar, self.year)
            check = models.Program.objects.filter(prgrm_andar_year=andar_year).exists()
            if not check:
                agency = models.Agencies.objects.get(agency_andar_number=row[self.output_index['Agency Andar #']])
                start_date = row[self.output_index['Grant Start Date']]
                end_date = row[self.output_index['Grant End Date']]
                if '-' not in start_date and '-' not in end_date:
                    start_date = start_date[:4] + '-' + start_date[4:6] + '-' + start_date[6:]
                    end_date = end_date[:4] + '-' + end_date[4:6] + '-' + end_date[6:]
                program = models.Program(prgrm_andar_year=andar_year,
                                         agency_andar_number=agency,
                                         program_andar_number=row[self.output_index['Program Andar #']],
                                         program_name=row[self.output_index['Program Name']],
                                         grant_start_date=start_date,
                                         grant_end_date=end_date,
                                         program_description=row[self.output_index['Short Program Description']],
                                         program_planner=row[self.output_index['Planner']],
                                         funds=row[self.output_index['Funds']],
                                         focus_area=row[self.output_index['Focus Area']],
                                         strategic_outcome=row[self.output_index['Strategic Outcome']],
                                         funding_stream=row[self.output_index['Funding Stream']],
                                         allocation=row[self.output_index['Allocation']],
                                         year=self.year)
                if program not in program_list:
                    program_list.append(program)
        models.Program.objects.bulk_create(program_list)

    # Inserts agency data into the database, this is the only table that is never dropped.
    def insert_agency(self):
        agency_list = []
        for row in self.content:
            check = models.Agencies.objects.filter(
                agency_andar_number=row[self.output_index['Agency Andar #']]).exists()
            # Agency already exists if we are overwriting so we update the agency name if needed
            if check:
                if self.overwrite:
                    agency = models.Agencies.objects.get(agency_andar_number=row[self.output_index['Agency Andar #']])
                    cur_agency = row[self.output_index['Agency Name']]
                    if agency.agency_name != cur_agency:
                        agency.agency_name = cur_agency
                        agency.save()
            else:
                # If agency does not exists then we create it in database
                agency = models.Agencies(agency_andar_number=row[self.output_index['Agency Andar #']],
                                         agency_name=row[self.output_index['Agency Name']])
                if agency not in agency_list:
                    agency_list.append(agency)
        models.Agencies.objects.bulk_create(agency_list)

    # Inserts program location data into database
    def insert_program_location(self):
        pro_loc_list = []
        for row in self.content:
            locations = self.get_locations(row)
            for location in locations:
                loc_name = location[0]
                loc_post = location[1]
                loc_lat = location[2]
                loc_lon = location[3]
                address = location[4]
                # Check that the location is not empty
                if loc_name != 'None' and loc_name != '' and loc_post != 'None' and loc_post != '' and loc_lat != 'None' and loc_lat != '' and loc_lon != 'None' and loc_lon != '':
                    # Check that location does not already exist
                    check = models.Location.objects.filter(
                        program_andar_number=row[self.postal_index['Program Andar #']],
                        program_name=row[self.postal_index['Program Name']],
                        location=loc_name,
                        postal_code=loc_post,
                        latitude=loc_lat,
                        longitude=loc_lon).exists()
                    # Insert data into database
                    if not check:
                        loc = models.Location(program_andar_number=row[self.postal_index['Program Andar #']],
                                              program_name=row[self.postal_index['Program Name']],
                                              location=loc_name,
                                              postal_code=loc_post,
                                              latitude=loc_lat,
                                              longitude=loc_lon,
                                              address=address,
                                              website=row[self.postal_index['Website']])
                        if loc not in pro_loc_list:
                            pro_loc_list.append(loc)
        models.Location.objects.bulk_create(pro_loc_list)

    # Checks that columns have the correct column length and that it contains the expected columns
    def check_columns(self):
        output_columns = ['Funds', 'Focus Area', 'Strategic Outcome', 'Funding Stream', 'Agency Andar #', 'Agency Name',
                          'Program Andar #', 'Program Name', 'Grant Start Date', 'Grant End Date',
                          'Short Program Description', 'Planner', 'Target Population', 'Program Elements',
                          'Geographic Focus Area', 'Donor Engagement', 'Outputs', 'First Nation Territories',
                          'Metro Vancouver Regional District', 'Fraser Valley Regional District',
                          'Squamish-Lillooet Regional District', 'Sunshine Coast Regional District', 'Other Areas']
        program_postal_columns = ['Agency Andar #', 'Agency Name', 'Program Andar #', 'Program Name', 'Website',
                                  'Description',
                                  '# Locations']
        pfile = self.cur_file
        with open(pfile, 'rb') as f:
            reader = csv.reader(f)
            columns = reader.next()
            if self.type == 'postal':
                if len(columns) != 37:
                    print "Columns have been removed or added, system may not work"
                for col_name in program_postal_columns:
                    if col_name not in columns:
                        raise Exception('Error in parsing: Column %s is missing' % col_name)
            elif self.type == 'output':
                if len(columns) != 159:
                    print "Columns have been removed or added, system may not work"
                for col_name in output_columns:
                    if col_name not in columns:
                        raise Exception('Error in parsing: Column %s is missing' % col_name)
        return True

    # checks that the type of the file is either postal or output
    def check_type(self):
        if str(self.type) != 'postal' and str(self.type) != 'output':
            raise Exception('Error in parsing: File type is incorrect')
        return True

    # Checks that the file is a CSV
    def validate_file(self):
        pfile = self.cur_file
        if pfile.endswith('.csv') and self.check_columns() and self.check_type():
            return True
        else:
            raise Exception("Error in parsing: Failed to validate file")

    # Inserts the parsed contents into the database
    def insert_file(self):
        if self.content:
            if 'output' in self.type:
                if self.overwrite:
                    self.drop_program_table()
                prev_counts = self.get_counts()
                self.insert_data()
                new_counts = self.get_counts()
            elif 'postal' in self.type:
                if self.overwrite:
                    self.drop_location_table()
                prev_counts = self.get_counts()
                self.insert_program_location()
                new_counts = self.get_counts()

            # Return success messages
            if self.overwrite and prev_counts != new_counts:
                return "Upload complete, data has been overwritten"
            elif prev_counts != new_counts:
                return "Upload complete, new data has been added to database "
            elif prev_counts == new_counts:
                return "Upload complete, no new data has been added to database"
            else:
                return "Update complete, database has been overwritten but no data added"

        else:
            raise Exception("Error in parsing: Nothing to insert")

    # Parses the file
    def parse_file(self):
        pfile = self.cur_file
        if "output" in self.type:
            with open(pfile, 'rb') as f:
                reader = csv.reader(f)
                self.column_names = reader.next()
                self.get_output_index(self.column_names)
                for row in reader:
                    # Beginning of row is not filled, consider empty
                    if row[0] is not '':
                        self.content.append(row)

        elif "postal" in self.type:
            with open(pfile, 'rb') as f:
                reader = csv.reader(f)
                self.column_names = reader.next()
                self.get_postal_index(self.column_names)
                for row in reader:
                    # Beginning of row is not filled, consider empty
                    if row[0] is not '':
                        self.content.append(row)
