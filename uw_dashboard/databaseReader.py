from django.db import connection, models

def my_custom_sql(query):
	with connection.cursor() as cursor:
        	cursor.execute(query)
                results = dictfetchall(cursor)
        return results

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
        	dict(zip(columns, row))
                for row in cursor.fetchall()
        ]

class DatabaseReader(models.Model):

	def __init__(self, filters):
		self.filters = filters

	def readData(self):
		filters = self.filters
		filters = dict(filters.iterlists())
		query = "SELECT p.*, GROUP_CONCAT(DISTINCT pe.element_name SEPARATOR ',') as element_names, GROUP_CONCAT(DISTINCT pe.specific_element SEPARATOR ','), GROUP_CONCAT(DISTINCT de.donor_engagement SEPARATOR ','), GROUP_CONCAT(DISTINCT t.target_population SEPARATOR ','), GROUP_CONCAT(DISTINCT l.postal_code SEPARATOR ','), SUM(DISTINCT p.allocation), MIN(DISTINCT p.grant_start_date), MAX(DISTINCT p.grant_end_date), t.target_population, gfa.city, gfa.city_grouping, a.agency_name"
		
		query += " FROM uw_dashboard_program AS p"
		query += " LEFT JOIN uw_dashboard_program_elements AS pe ON p.prgrm_andar_year = pe.prgrm_andar_year_id"
		query += " LEFT JOIN uw_dashboard_target_population AS t ON p.prgrm_andar_year = t.prgrm_andar_year_id"
		query += " LEFT JOIN uw_dashboard_geo_focus_area AS gfa ON p.prgrm_andar_year = gfa.prgrm_andar_year_id"
		query += " LEFT JOIN uw_dashboard_donor_engagement AS de ON p.prgrm_andar_year = de.prgrm_andar_year_id"
		query += " LEFT JOIN uw_dashboard_location AS l ON p.prgrm_andar_year = l.program_andar_number"
		query += " LEFT JOIN uw_dashboard_agencies AS a ON p.agency_andar_number_id = a.agency_andar_number WHERE"

		if 'funding_year' in filters.keys():
			query += " ("
			for i in filters['funding_year']:
				#query += " p.grant_start_date BETWEEN '" + str(i) + "-01-01' AND '" + str(i) + "-12-31' OR"
				query += " p.year = '" + str(filters['funding_year'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"
	
		if 'focus_area' in filters.keys():
			query += " ("
			for i in range(len(filters['focus_area'])):
				query += " p.focus_area = '" + str(filters['focus_area'][i]) + "' OR"
			query = query[:-2]
			query += " ) AND"

		if 'target_population' in filters.keys():
			query += " ("
			for i in range(len(filters['target_population'])):
				query += " t.target_population = '" + str(filters['target_population'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"

		if 'program_elements' in filters.keys():
			query += " ("
			for i in range(len(filters['program_elements'])):
				query += " pe.specific_element = '" + str(filters['program_elements'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"

		if 'gfa' in filters.keys():
			query += " ("
			for i in range(len(filters['gfa'])):
				query += " gfa.city = '" + str(filters['gfa'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"

		if 'city' in filters.keys():
			query += " ("
			for i in range(len(filters['city'])):
	                        query += " gfa.city_grouping = '" + str(filters['city'][i]) + "' OR"
	                query = query[:-2]
	                query += ") AND"	
	
		if 'donor' in filters.keys():
			query += " ("
			for i in range(len(filters['donor'])):
				query += " de.donor_engagement = '" + str(filters['donor'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"

		if 'money_invested' in filters.keys():
			query += " ("
			for i in filters['money_invested']:
				if '+' in i:
					i = i[:-1]
					query += " p.allocation > '" + str(i) + "' OR"
				elif '-' in i:
					nums = str(i).split('-')
					query += " (p.allocation >= '" + str(nums[0]) + "' AND p.allocation <= '" + str(nums[1]) + "') OR"
				else:
					query += " p.allocation < '" + str(i) + "' OR"
			query = query[:-2]
			query += ") AND"

		query += " TRUE GROUP BY p.prgrm_andar_year, pe.prgrm_andar_year_id, de.prgrm_andar_year_id, l.program_andar_number, p.grant_start_date"

		firstResults = my_custom_sql(query)
		
		programsReturned = [i['prgrm_andar_year'] for i in firstResults]
		programsReturned = list(set(programsReturned))

		tQuery = "SELECT SUM(p.allocation) AS invested, COUNT(p.prgrm_andar_year) AS programs, COUNT(DISTINCT p.agency_andar_number_id) AS agencies, SUM(t.early_years) AS early_years, SUM(t.middle_years) AS middle_years, SUM(t.seniors) AS seniors, SUM(t.parent_caregivers) AS parent_caregivers, SUM(t.families) AS families, SUM(t.meals_snacks) as meals_snacks, SUM(t.counselling_sessions) AS counselling_sessions, SUM(t.mentors_tutors) AS mentors_tutors, SUM(t.workshops) as workshops, SUM(t.volunteers) AS volunteers FROM uw_dashboard_program as p, uw_dashboard_totals as t WHERE"

		tQuery += " p.prgrm_andar_year = t.prgrm_andar_year_id AND"

		if len(programsReturned) != 0:
			tQuery += " ("
			for i in programsReturned:
				tQuery += " p.prgrm_andar_year = '" + str(i) + "' OR"
			tQuery = tQuery[:-2]
			tQuery += ") AND"
		tQuery += " TRUE"

		tResults = my_custom_sql(tQuery)

		return {'results': firstResults, 'totals': tResults, 'query': query, 'tquery': tQuery, 'filters': filters}	
