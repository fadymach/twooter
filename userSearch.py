import os
import followers

###
#TODO need to add only 5 users at a time shown.
###

def search(usr, connection):
	keywords = getKeywords()
	cursor = connection.cursor()
	query = buildQuery(keywords)
	rows = cursor.execute(query).fetchall()
	rows.sort(key = lambda x : len(x[1].strip()))
	followers.followers(usr, connection, rows)



def buildQuery(keywords):
	if len(keywords) > 0:
			whereClause1 = "WHERE ((LOWER(u.name) LIKE "
			i = 0
			for word in keywords:
				if i == 0:
					whereClause1 += "'%"+word+"%')"
					i += 1
				else:
					whereClause1 += " OR (LOWER(name) LIKE '%"+word+"%')"
			whereClause1 += ")"

	query = "SELECT u.usr, u.name FROM users u " +whereClause1
	return query


def getKeywords():
	usrInput = input("Enter space-separated keyword(s) to search for:" + '\n')
	keywords = usrInput.lower().strip().split()
	return keywords
