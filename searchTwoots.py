import cx_Oracle as cx
import os
import textwrap

def searchTwoots(connection):
	# Allows a user to search for twoots
	printScreen()
	keywords = getKeywords()
	results = executeQuery(connection, keywords)

	printScreen()

	for i in range(len(results)):
		if results[i][3] != None:
			print("Reply to: " + str(results[i][3])) # Reply to
		print("---------------------------------------------------")
		print(str(results[i][0]) + '\t'*2 + str(results[i][1])) # User and date
		print(textwrap.fill(results[i][2], 50)) # Text
		print('\n')
		i += 1




def executeQuery(connection, keywords):
	# Create string for query WHERE clause
	whereClause = "WHERE ((LOWER(text) LIKE "
	countWords = len(keywords)

	# Build WHERE clause
	i = 0
	for word in keywords:
		if i == 0:
			print(word)
			whereClause += "'%"+word+"%')"
			i += 1
		else:
			whereClause += " OR (LOWER(text) LIKE '%"+word+"%')"
	whereClause += ") AND (t.writer = u1.usr) "

	# Create and execute query
	query = "SELECT u1.name, t.tdate, t.text, u2.name " \
			"FROM users u1, tweets t " \
			"LEFT OUTER JOIN users u2 ON t.replyto = u2.usr " + whereClause
	

	print(query)
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	cursor.close()

	return results
	

def getKeywords():
	usrInput = input("Enter space-separated keyword(s) to search for:" + '\n')
	return usrInput.lower().strip().split()

def printScreen():
	os.system("clear")
	print("Search Twoots")
	print("-------------------------------------------------------------" + '\n')
