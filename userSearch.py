import os
import followers

def search(usr, connection):
	message = ''
	while(True):
		keywords = ""
		while keywords == "":
			keywords = getKeywords(message)
		cursor = connection.cursor()
		nameQuery = buildNameQuery(keywords)
		cityQuery = buildCityQuery(keywords)
		if (nameQuery=="" or cityQuery==""):
			continue

		names = cursor.execute(nameQuery).fetchall()
		names.sort(key = lambda x : len(x[1].strip()))
		cities = cursor.execute(cityQuery).fetchall()
		cities.sort(key = lambda t: len(t[2].strip()))

		people = names + cities
		if people==[]:
			message = "No results found."
			continue

		followers.followers(usr, connection, people, 5)
		return



def buildNameQuery(keywords):
	if len(keywords) > 0:
		whereClause1 = "WHERE ((LOWER(u.name) LIKE "
		i = 0
		for word in keywords:
			if i == 0:
				whereClause1 += "'%"+word+"%')"
				i += 1
			else:
				whereClause1 += " OR (LOWER(u.name) LIKE '%"+word+"%')"
		whereClause1 += ")"
		query = "SELECT u.usr, u.name FROM users u " +whereClause1
	else:
		query = ""
	return query


def buildCityQuery(keywords):
	if len(keywords) > 0:
		whereClause1 = "WHERE ((LOWER(u.city) LIKE "
		i = 0
		for word in keywords:
			if i == 0:
				whereClause1 += "'%"+word+"%')) MINUS (SELECT u.usr, u.name, u.city from users u WHERE ((LOWER(u.name) LIKE '%"+word+"%')))"
				i += 1

		query = "SELECT u.usr, u.name, u.city FROM users u " +whereClause1
	else:
		query = ""
	return query




def getKeywords(message = ''):
	os.system("clear")
	print(message)
	usrInput = input("Enter space-separated keyword(s) to search for:" + '\n')
	keywords = usrInput.lower().strip().split()
	return keywords
