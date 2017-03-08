from django.db import connection, models

def my_custom_sql(query):
	with connection.cursor() as cursor:
		cursor.execute(query)
		results = cursor.fetchall()
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
		query = "SELECT * FROM Program AS p, Program_Elements AS pe, Target_Population AS t, Geo_Focus_Area AS gfa, Donor_Engagement AS de WHERE"

		joinTables = " p.program_andar_number = pe.program_andar_number AND p.program_andar_number = t.program_andar_number AND p.program_andar_number = gfa.program_andar_number AND p.program_andar_number = de.program_andar_number AND"

		if 'funding_year' in filters.keys():
			query += " ("
			for i in range(len(filters['funding_year'])):
				query += " p.grant_start_date BETWEEN '" + str(filters['funding_year'][i]) + "-01-01' AND '" + str(filters['funding_year'][i]) + "'-12-31' OR"
			query = query[:-2]
			query += " AND"
	
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

		firstResults = my_custom_sql(query)
		
		programsReturned = [i[0] for i in firstResults]

		tQuery = "SELECT SUM(p.funds) AS invested, COUNT(p.program_andar_number) AS programs, COUNT(DISTINCT p.agency_andar_number) AS agencies, SUM(t.early_years) AS early_years, SUM(t.middle_years) AS middle_years, SUM(t.seniors) AS seniors, SUM(t.parent_caregivers) AS parent_caregivers, SUM(t.families) AS families, SUM(t.meals_snacks) as meals_snacks, SUM(t.counselling_sessions) AS counselling_sessions, SUM(t.mentors_tutors) AS mentors_tutors, SUM(t.workshops) as workshops, SUM(t.volunteers) AS volunteers FROM Program as p, Totals as t WHERE"

		tJoinQuery = " p.program_andar_number = t.program_andar_number AND"

		tPrograms = " ("
		for i in programsReturned:
			tPrograms += " p.program_andar_number = '" + str(programsReturned[i]) + "' OR"
		tPrograms = tPrograms[:-2]
		tPrograms += ")"

		tFinalQuery = tQuery + tJoinQuery + tPrograms

		tResults = my_custom_sql(tFinalQuery)
