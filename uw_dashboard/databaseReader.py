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

	def readData():
		filters = self.filters
		query = "SELECT * FROM Program AS p, Program_Elements AS pe, Target_Population AS t, Geo_Focus_Area AS gfa, Donor_Engagement AS de WHERE"

		joinTables = " p.program_andar_number = pe.program_andar_number AND p.program_andar_number = t.program_andar_number AND p.program_andar_number = gfa.program_andar_number AND p.program_andar_number = de.program_andar_number AND"

		if 'year' in filters.keys():
			filterYear = " ("
			for i in range(len(filters['year'])):
				filterYear += " p.grant_start_date BETWEEN '" + str(filters['year'][i]) + "-01-01' AND '" + str(filters['year'][i]) + "'-12-31' OR"
			filterYear = filterYear[:-2]
			filterYear += " AND"
	
		if 'focus_area' in filters.keys():
			focusArea = " ("
			for i in range(len(filters['focus_area'])):
				focusArea += " p.focus_area = '" + str(filters['focus_area'][i]) + "' OR"
			focusArea = focusArea[:-2]
			focusArea += " ) AND"

		if 'target_population' in filters.keys():
			targetPop = " ("
			for i in range(len(filters['target_population'])):
				targetPop += " t.target_population = '" + str(filters['target_population'][i]) + "' OR"
			targetPop = targetPop[:-2]
			targetPop += ") AND"

		if 'program_elements' in filters.keys():
			programElements = " ("
			for i in range(len(filters['program_elements'])):
				programElements += " pe.specific_element = '" + str(filters['program_elements'][i]) + "' OR"
			programElements = programElements[:-2]
			programElements += ") AND"

		if 'gfa' in filters.keys():
			gfa = " ("
			for i in range(len(filters['gfa'])):
				gfa += " gfa.city = '" + str(filters['gfa'][i]) + "' OR"
			gfa = gfa[:-2]
			gfa += ") AND"

		if 'city' in filters.keys():
			cityGrouping = " ("
			for i in range(len(filters['city'])):
	                        cityGrouping += " gfa.city_grouping = '" + str(filters['city'][i]) + "' OR"
	                cityGrouping = cityGrouping[:-2]
	                cityGrouping += ") AND"	
	
		if 'donor' in filters.keys():
			donorEngagement = " ("
			for i in range(len(filters['donor'])):
				donorEngagement += " de.donor_engagement = '" + str(filters['donor'][i]) + "' OR"
			donorEngagement = donorEngagement[:-2]
			donorEngagement += ") AND"

		if 'invested' in filters.keys():
			investment = " ("
			for i in range(len(filters['invested'])):
				investment += " p.funds = '" + str(filters['invested'][i]) + "' OR"
			investment = investment[:-2]
			investment += ")"

		finalQuery = query + joinTables + filterYear + focusArea + targetPop + programElements + gfa + cityGrouping + donorEngagement + investment

		firstResults = my_custom_sql(finalQuery)
		
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
