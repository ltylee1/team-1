from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.test import Client
from django.core.urlresolvers import reverse
import models
import datetime
import os
from parser import Parser

# class UserProfileTest(TestCase):
#     def setUp(self):
#         User.objects.create_user('john', password='password')
#
#     def test_create_user_create_profile(self):
#         self.assertTrue(Profile.objects.filter(user__username = 'john').exists())
#
#     def test_delete_user_delete_profile(self):
#         User.objects.get(username = 'john').delete()
#         self.assertFalse(Profile.objects.filter(user__username='john').exists())

#
# class LoginTest(TestCase):
#     def setUp(self):
#         self.credentials = {
#             'username': 'testuser',
#             'password': 'secret'}
#         User.objects.create_user(**self.credentials)
#         self.client = Client()
#
#     def test_login(self):
#         # login
#         response = self.client.post(reverse('login'), **self.credentials)
#
#         # should be logged in now, fails however
#         user = User.objects.get(username = response.request["username"])
#         self.assertTrue(user.is_authenticated)
#
#     def test_incorrect_password(self):
#         # login
#         response = self.client.post(reverse('login'), username = 'testuser', password = 'incorrect')
#
#         # should be logged in now, fails however
#         print list(response.context)
#         user = User.objects.get(username = response.request["username"])
#         self.assertFalse(user.is_authenticated)

class ParserTestWithoutDBSETUP(TestCase):

    def setUp(self):
        self.dir = os.getcwd()
        self.file = os.path.join(self.dir, 'media', '201516_Inventory_and_Outputs.Feb_update.csv')

    def testInvalidFileType(self):
        Invalid = os.path.join(self.dir, 'media', '201516_Inventory_and_Outputs.Feb_update.xlsx')
        parser = Parser(Invalid, 2017, True, 'output')
        self.assertFalse(parser.validate_file())

    def testInvalidType(self):
        with self.assertRaises(Exception) as context:
            Parser(self.file, 2017, True, 2017)
        self.assertTrue('type is invalid' in str(context.exception))

    def testInvalidFile(self):
        Invalid = 2013
        with self.assertRaises(Exception) as context:
            Parser(Invalid, 2017, True, 'zsadsf')
        self.assertTrue('file invalid' in str(context.exception))

    def testInvalidOverwrite(self):
        with self.assertRaises(Exception) as context:
            Parser(self.file, 2017, 'true', 'postal')
        self.assertTrue('overwrite invalid' in str(context.exception))

    def testInvalidYear(self):
        with self.assertRaises(Exception) as context:
            Parser(self.file, '2017', True, 'postal')
        self.assertTrue('year invalid' in str(context.exception))


class ParserTestWithDBSETUP(TestCase):
    # Test end cases, Test Update, Test Overwrite, Test Append, Test Endpoints, Test first, last, middle value
    def setUp(self):
        self.dir = os.getcwd()
        Inv = os.path.join(self.dir, 'media', '201516_Inventory_and_Outputs.Feb_update.csv')
        Post = os.path.join(self.dir, 'media', 'Postal.csv')

        rs = models.Reporting_Service('')
        rs.import_data(Inv, 2017, True, 'output')
        rs.import_data(Post, 2017, True, 'postal')

    # Get first, middle and last entry
    def testPostal(self):
        check = models.Location.objects.all()
        self.assertEqual(check.count(), 67)

        first = models.Location.objects.first()
        self.assertEqual(first.location, 'Atira Development Society')
        self.assertEqual(first.postal_code, 'V6A 1K7')
        self.assertEqual(first.website, '')
        self.assertEqual(first.program_andar_number, 5990569)

        last = models.Location.objects.last()
        self.assertEqual(last.location, 'Valley Community Services')
        self.assertEqual(last.postal_code, 'V0B 1G5')
        self.assertEqual(last.website, '')
        self.assertEqual(last.program_andar_number, 5606579)

        random = check[28]
        self.assertEqual(random.location, 'Strathcona Park Club House')
        self.assertEqual(random.postal_code, 'V6A 2K5')
        self.assertEqual(random.website, '')
        self.assertEqual(random.program_andar_number, 5649744)

    def testOutput(self):
        check = models.Program.objects.all()
        self.assertEqual(check.count(), 30)

        first = models.Program.objects.first()
        self.assertEqual(first.agency_andar_number.agency_andar_number, 184986)
        self.assertEqual(first.program_andar_number, 4962759)
        self.assertEqual(first.program_name, 'Better at Home Langley')
        self.assertEqual(first.grant_start_date, datetime.date(2015, 4, 1))
        self.assertEqual(first.grant_end_date, datetime.date(2016, 3, 31))
        self.assertEqual(first.program_description, 'Better at Home funding mobilizes local resources, networks and volunteers to support seniors living in their homes and enabling them to remain at home longer.')
        self.assertEqual(first.program_planner, 'Yves Trudel')
        self.assertEqual(first.funds, 'GOV')
        self.assertEqual(first.focus_area, 'Strong Communities')
        self.assertEqual(first.strategic_outcome, 'Helping Seniors to Live Independently')
        self.assertEqual(first.funding_stream, 'Better at Home')
        self.assertEqual(first.allocation, 180000)
        self.assertEqual(first.year, 2017)

        random = check[3]
        self.assertEqual(random.agency_andar_number.agency_andar_number, 1891)
        self.assertEqual(random.program_andar_number, 5121926)
        self.assertEqual(random.program_name, 'Better at Home Burnaby')
        self.assertEqual(random.grant_start_date, datetime.date(2015, 4, 1))
        self.assertEqual(random.grant_end_date, datetime.date(2016, 3, 31))
        self.assertEqual(random.program_description, 'Better at Home funding mobilizes local resources, networks and volunteers to support seniors living in their homes and enabling them to remain at home longer.')
        self.assertEqual(random.program_planner, 'Angie Osachoff')
        self.assertEqual(random.funds, 'GOV')
        self.assertEqual(random.focus_area, 'Strong Communities')
        self.assertEqual(random.strategic_outcome, 'Helping Seniors to Live Independently')
        self.assertEqual(random.funding_stream, 'Better at Home')
        self.assertEqual(random.allocation, 227500)
        self.assertEqual(random.year, 2017)

        last = models.Program.objects.last()
        self.assertEqual(last.agency_andar_number.agency_andar_number, 252510)
        self.assertEqual(last.program_andar_number, 6017495)
        self.assertEqual(last.program_name, 'Maple Ridge Pitt Meadows Community School Partnership')
        self.assertEqual(last.grant_start_date, datetime.date(2015, 12, 1))
        self.assertEqual(last.grant_end_date, datetime.date(2016, 6, 30))
        self.assertEqual(last.program_description, 'Funding of Community School Coordinator to facilitatie provision of out of school time programming to children to keep them safe and supervised as well as provide opportunities for self-development.')
        self.assertEqual(last.program_planner, 'Angie Osachoff')
        self.assertEqual(last.funds, 'UWLM')
        self.assertEqual(last.focus_area, 'All That Kids Can Be')
        self.assertEqual(last.strategic_outcome, 'Helping School-Aged Children Succeed')
        self.assertEqual(last.funding_stream, 'Community Schools')
        self.assertEqual(last.allocation, 25000)
        self.assertEqual(last.year, 2017)

        check = models.Program_Elements.objects.all()
        self.assertEqual(check.count(), 209)
        first = models.Program_Elements.objects.first()
        self.assertEqual(first.program_andar_number.program_andar_number, 5121926)
        self.assertEqual(first.level, 100)
        self.assertEqual(first.element_name, 'Social and Emotional Health ')
        self.assertEqual(first.specific_element, 'Independence')

        random = check[100]
        self.assertEqual(random.program_andar_number.program_andar_number, 5649488)
        self.assertEqual(random.level, 100)
        self.assertEqual(random.element_name, 'System Change')
        self.assertEqual(random.specific_element, 'Policy work')

        last = models.Program_Elements.objects.last()
        self.assertEqual(last.program_andar_number.program_andar_number, 5989751)
        self.assertEqual(last.level, 200)
        self.assertEqual(last.element_name, 'Address Program Barriers/Access')
        self.assertEqual(last.specific_element, 'Transportation')

        check = models.Agencies.objects.all()
        self.assertEqual(check.count(), 29)

        first = models.Agencies.objects.first()
        self.assertEqual(first.agency_andar_number, 1891)
        self.assertEqual(first.agency_name, 'City of Burnaby')

        random = check[12]
        self.assertEqual(random.agency_andar_number, 174235)
        self.assertEqual(random.agency_name, 'Mount Pleasant Neighbourhood House')

        last = models.Agencies.objects.last()
        self.assertEqual(last.agency_andar_number, 6014294)
        self.assertEqual(last.agency_name, 'Atira Development Society')

        check = models.Target_Population.objects.all()
        self.assertEqual(check.count(), 49)
        first = models.Target_Population.objects.first()
        self.assertEqual(first.program_andar_number.program_andar_number, 5121926)
        self.assertEqual(first.target_population, 'Seniors')

        random = check[23]
        self.assertEqual(random.program_andar_number.program_andar_number, 5816343)
        self.assertEqual(random.target_population, 'Families')

        last = models.Target_Population.objects.last()
        self.assertEqual(last.program_andar_number.program_andar_number, 5989751)
        self.assertEqual(last.target_population, 'Families')

        check = models.Geo_Focus_Area.objects.all()
        self.assertEqual(check.count(), 49)
        first = models.Geo_Focus_Area.objects.first()
        self.assertEqual(first.program_andar_number.program_andar_number, 5121926)
        self.assertEqual(first.city, 'Burnaby')
        self.assertEqual(first.percent_of_focus, 100)
        self.assertEqual(first.level_name, 'Metro Vancouver Regional District')
        self.assertEqual(first.city_grouping, 'Burnaby')

        random = check[23]
        self.assertEqual(random.program_andar_number.program_andar_number, 5649512)
        self.assertEqual(random.city, 'North Vancouver, District Municipality')
        self.assertEqual(random.percent_of_focus, 20)
        self.assertEqual(random.level_name, 'Metro Vancouver Regional District')
        self.assertEqual(random.city_grouping, 'Northshore')

        last = models.Geo_Focus_Area.objects.last()
        self.assertEqual(last.program_andar_number.program_andar_number, 5989751)
        self.assertEqual(last.city, 'Vancouver')
        self.assertEqual(last.percent_of_focus, 100)
        self.assertEqual(last.level_name, 'Metro Vancouver Regional District')
        self.assertEqual(last.city_grouping, 'Vancouver')

        check = models.Donor_Engagement.objects.all()
        self.assertEqual(check.count(), 54)
        first = models.Donor_Engagement.objects.first()
        self.assertEqual(first.program_andar_number.program_andar_number, 5846167)
        self.assertEqual(first.donor_engagement, 'Volunteer Opps')
        random = check[17]
        self.assertEqual(random.program_andar_number.program_andar_number, 5988456)
        self.assertEqual(random.donor_engagement, 'Volunteer Opps')
        last = models.Donor_Engagement.objects.last()
        self.assertEqual(last.program_andar_number.program_andar_number, 5989751)
        self.assertEqual(last.donor_engagement, 'Impact Story')

        check = models.Totals.objects.all()
        self.assertEqual(check.count(), 30)
        first = models.Totals.objects.first()
        self.assertEqual(first.program_andar_number.program_andar_number, 5121926)
        self.assertEqual(first.total_clients, 198)
        self.assertEqual(first.early_years, 0)
        self.assertEqual(first.middle_years, 0)
        self.assertEqual(first.children, 0)
        self.assertEqual(first.seniors, 198)
        self.assertEqual(first.parent_caregivers, 0)
        self.assertEqual(first.families, 0)
        self.assertEqual(first.contacts, 4865)
        self.assertEqual(first.meals_snacks, 0)
        self.assertEqual(first.counselling_sessions, 0)
        self.assertEqual(first.mentors_tutors, 0)
        self.assertEqual(first.workshops, 0)
        self.assertEqual(first.volunteers, 0)

        random = check[14]
        self.assertEqual(random.program_andar_number.program_andar_number, 5649512)
        self.assertEqual(random.total_clients, 0)
        self.assertEqual(random.early_years, 0)
        self.assertEqual(random.middle_years, 0)
        self.assertEqual(random.children, 0)
        self.assertEqual(random.seniors, 0)
        self.assertEqual(random.parent_caregivers, 0)
        self.assertEqual(random.families, 0)
        self.assertEqual(random.contacts, 0)
        self.assertEqual(random.meals_snacks, 0)
        self.assertEqual(random.counselling_sessions, 0)
        self.assertEqual(random.mentors_tutors, 0)
        self.assertEqual(random.workshops, 0)
        self.assertEqual(random.volunteers, 0)

        last = models.Totals.objects.last()
        self.assertEqual(last.program_andar_number.program_andar_number, 5989751)
        self.assertEqual(last.total_clients, 288)
        self.assertEqual(last.early_years, 132)
        self.assertEqual(last.middle_years, 21)
        self.assertEqual(last.children, 153)
        self.assertEqual(last.seniors, 0)
        self.assertEqual(last.parent_caregivers, 135)
        self.assertEqual(last.families, 132)
        self.assertEqual(last.contacts, 15840)
        self.assertEqual(last.meals_snacks, 15900)
        self.assertEqual(last.counselling_sessions, 642)
        self.assertEqual(last.mentors_tutors, 20)
        self.assertEqual(last.workshops, 490)
        self.assertEqual(last.volunteers, 34)

    def testOverwrite(self):
        Updated = os.path.join(self.dir, 'media', '201516_Inventory_and_Outputs.Feb_update shorter append.csv')
        UpdatedPost = os.path.join(self.dir, 'media', 'Postal - Updated.csv')
        rs = models.Reporting_Service('')

        rs.import_data(Updated, 2017, True, 'output')
        rs.import_data(UpdatedPost, 2017, True, 'postal')

        check = models.Program.objects.all()
        self.assertEqual(check.count(), 16)

        random = check[9]
        self.assertEqual(random.agency_andar_number.agency_andar_number, 174227)
        self.assertEqual(random.program_andar_number, 5649678)
        self.assertEqual(random.program_name, 'Westside Seniors Kitchen Project')
        self.assertEqual(random.grant_start_date, datetime.date(2015, 4, 1))
        self.assertEqual(random.grant_end_date, datetime.date(2016, 3, 31))
        self.assertEqual(random.program_description, 'Reduces barriers of accessibility to nutritious food and enables isolated seniors to connect with others.')
        self.assertEqual(random.program_planner, 'Beverley Pitman')
        self.assertEqual(random.funds, 'UWLM')
        self.assertEqual(random.focus_area, 'Poverty to Possibility')
        self.assertEqual(random.strategic_outcome, 'Giving Skills to Feed Families')
        self.assertEqual(random.funding_stream, 'Food for All')
        self.assertEqual(random.allocation, 19625)
        self.assertEqual(random.year, 2017)

        last = models.Program.objects.last()
        self.assertEqual(last.agency_andar_number.agency_andar_number, 252510)
        self.assertEqual(last.program_andar_number, 6017495)
        self.assertEqual(last.program_name, 'Maple Ridge Pitt Meadows Community School Partnership')
        self.assertEqual(last.grant_start_date, datetime.date(2015, 12, 1))
        self.assertEqual(last.grant_end_date, datetime.date(2016, 6, 30))
        self.assertEqual(last.program_description, 'Funding of Community School Coordinator to facilitatie provision of out of school time programming to children to keep them safe and supervised as well as provide opportunities for self-development.')
        self.assertEqual(last.program_planner, 'Angie Osachoff')
        self.assertEqual(last.funds, 'UWLM')
        self.assertEqual(last.focus_area, 'All That Kids Can Be')
        self.assertEqual(last.strategic_outcome, 'Helping School-Aged Children Succeed')
        self.assertEqual(last.funding_stream, 'Community Schools')
        self.assertEqual(last.allocation, 25000)
        self.assertEqual(last.year, 2017)
    #
    #     Inv = 'C:\Users\Ty\Desktop\CPSC 319\\201516_Inventory_and_Outputs.Feb_update.csv'
    #     Post = 'C:\Users\Ty\Desktop\CPSC 319\\Postal.csv'

        # rs = models.Reporting_Service('')
        # rs.import_data(Inv, 2016, True)
        # rs.import_data(Post, 2016, True)
        #
        # check = models.Program.objectsfilter(year='2017')
        # self.assertEqual(check.count(), 16)