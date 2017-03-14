from django.db import connection, models

def my_custom_sql(query, is_dict):
	with connection.cursor() as cursor:
        	cursor.execute(query)
		if is_dict == 1:
	                results = dictfetchall(cursor)
		else:
			results = cursor.fetchall()
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
		query = "SELECT * FROM uw_dashboard_program AS p, uw_dashboard_target_population AS t, uw_dashboard_geo_focus_area AS gfa WHERE"

		query += " p.program_andar_number = t.program_andar_number_id AND p.program_andar_number = gfa.program_andar_number_id AND"

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
	
		if 'money_invested' in filters.keys():
			query += " ("
			for i in filters['money_invested']:
				if '+' in i:
					i = i[:-1]
					query += " p.funds > '" + str(i) + "' OR"
				elif '-' in i:
					nums = str(i).split('-')
					query += " (p.funds >= '" + str(nums[0]) + "' AND p.funds <= '" + str(nums[1]) + "') OR"
				else:
					query += " p.funds < '" + str(i) + "' OR"
			query = query[:-2]
			query += ") AND"

		query += " TRUE"

		firstResults = my_custom_sql(query, 1)
		
		programsReturned = [i['program_andar_number'] for i in firstResults]

		for program in programsReturned:
			peQuery = "SELECT specific_element FROM uw_dashboard_program_elements WHERE program_andar_number_id = '" + str(program) + "'"
			locQuery = "SELECT COUNT(id) AS total, postal_code FROM uw_dashboard_location WHERE program_andar_number_id = '" + str(program) + "'"
			deQuery = "SELECT donor_engagement FROM uw_dashboard_donor_engagement WHERE program_andar_number_id = '" str(program) + "'"
			programElem = (item for item in firstResults if item["program_andar_number"] == str(program)).next()
			programElem['specific_elements'] = my_custom_sql(peQuery, 0)
			programElem['locations'] = my_custom_sql(locQuery, 1)
			programElemt['donor_engagement'] = my_custom_sql(deQuery, 0)

		tQuery = "SELECT SUM(p.funds) AS invested, COUNT(p.program_andar_number) AS programs, COUNT(DISTINCT p.agency_andar_number_id) AS agencies, SUM(t.early_years) AS early_years, SUM(t.middle_years) AS middle_years, SUM(t.seniors) AS seniors, SUM(t.parent_caregivers) AS parent_caregivers, SUM(t.families) AS families, SUM(t.meals_snacks) as meals_snacks, SUM(t.counselling_sessions) AS counselling_sessions, SUM(t.mentors_tutors) AS mentors_tutors, SUM(t.workshops) as workshops, SUM(t.volunteers) AS volunteers FROM uw_dashboard_program as p, uw_dashboard_totals as t WHERE"

		tQuery += " p.program_andar_number = t.program_andar_number_id AND"

		if len(programsReturned) != 0:
			tQuery += " ("
			for i in programsReturned:
				tQuery += " p.program_andar_number = '" + str(i) + "' OR"
			tQuery = tQuery[:-2]
			tQuery += ") AND"
		tQuery += " TRUE"

		tResults = my_custom_sql(tQuery, 1)

		return {'results': firstResults, 'totals': tResults, 'query': query, 'tquery': tQuery, 'filters': filters}	
