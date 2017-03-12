from django.db import connection, models


class DatabaseReader(models.Model):

	def __init__(self, filters):
		self.filters = filters

	def _my_custom_sql(self, query):
	        with connection.cursor() as cursor:
	                cursor.execute(query)
	                results = _dictfetchall(cursor)
	        return results

	def _dictfetchall(self, cursor):
	    "Return all rows from a cursor as a dict"
	    columns = [col[0] for col in cursor.description]
	    return [
	        dict(zip(columns, row))
	        for row in cursor.fetchall()
	    ]
	
	def readData(self):
		filters = self.filters
		filters = dict(filters.iterlists())
		query = "SELECT * FROM uw_dashboard_program AS p, uw_dashboard_program_elements AS pe, uw_dashboard_target_population AS t, uw_dashboard_geo_focus_area AS gfa, uw_dashboard_donor_engagement AS de WHERE"

		query += " p.program_andar_number = pe.program_andar_number_id AND p.program_andar_number = t.program_andar_number_id AND p.program_andar_number = gfa.program_andar_number_id AND p.program_andar_number = de.program_andar_number_id AND"

		if 'funding_year' in filters.keys():
			query += " ("
			for i in filters['funding_year']:
				query += " p.grant_start_date BETWEEN '" + str(i) + "-01-01' AND '" + str(i) + "-12-31' OR"
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
			for i in range(len(filters['money_invested'])):
				query += " p.funds = '" + str(filters['money_invested'][i]) + "' OR"
			query = query[:-2]
			query += ") AND"

		query += " TRUE"

		firstResults = _my_custom_sql(query)
		
		programsReturned = [i[0] for i in firstResults]

		tQuery = "SELECT SUM(p.funds) AS invested, COUNT(p.program_andar_number) AS programs, COUNT(DISTINCT p.agency_andar_number_id) AS agencies, SUM(t.early_years) AS early_years, SUM(t.middle_years) AS middle_years, SUM(t.seniors) AS seniors, SUM(t.parent_caregivers) AS parent_caregivers, SUM(t.families) AS families, SUM(t.meals_snacks) as meals_snacks, SUM(t.counselling_sessions) AS counselling_sessions, SUM(t.mentors_tutors) AS mentors_tutors, SUM(t.workshops) as workshops, SUM(t.volunteers) AS volunteers FROM uw_dashboard_program as p, uw_dashboard_totals as t WHERE"

		tQuery += " p.program_andar_number = t.program_andar_number_id AND"

		if len(programsReturned) != 0:
			tQuery += " ("
			for i in programsReturned:
				tQuery += " p.program_andar_number = '" + str(programsReturned[i]) + "' OR"
			tQuery = tQuery[:-2]
			tQuery += ") AND"
		tQuery += " TRUE"

		tResults = _my_custom_sql(tQuery)

		return {'results': firstResults, 'totals': tResults, 'query': query, 'tquery': tQuery, 'filters': filters, 'fund': filters['funding_year']}	
