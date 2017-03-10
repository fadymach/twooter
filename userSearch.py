import os
import followers

###
#TODO need to add only 5 users at a time shown.
###

def search(usr, connection):
	message = ""
	os.system("clear")
	keywords = getKeywords()
	cursor = connection.cursor()
	nameQuery = buildNameQuery(keywords)
	cityQuery = buildCityQuery(keywords)
	if(nameQuery != "" and cityQuery != ""):
		names = cursor.execute(nameQuery).fetchall()
		names.sort(key = lambda x : len(x[1].strip()))
		cities = cursor.execute(cityQuery).fetchall()
		cities.sort(key = lambda t: len(t[2].strip()))

		people = names + cities

		message = followers.followers(usr, connection, people)
	return message



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




def getKeywords():
	usrInput = input("Enter space-separated keyword(s) to search for:" + '\n')
	keywords = usrInput.lower().strip().split()
	return keywords
