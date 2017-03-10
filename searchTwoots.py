import cx_Oracle as cx
import os, re, textwrap
import twootInfo

def searchTwoots(usr, connection):
	msg = ""
	# Allows a user to search for twoots
	printHeader()
	keywords, hashtags = getKeywords()
	cursor = executeQuery(connection, keywords, hashtags)
	
	results = cursor.fetchmany(numRows=5)
	
	# Get user input
	allowedTID = getTID(results) # IDs user is allowed to input
	allowedCMD = ("back", "more", "sel")
	while True:
		printResults(results)
		print(msg)
		cmd = input("Selection: ").lower()
		while cmd not in allowedCMD:
			cmd = input("Invalid selection! Selection: ")
	
		if cmd == "back":
			break
		elif cmd == "more":
			newresults = cursor.fetchmany(numRows=5)
			if newresults != []:
				results = newresults
			else:
				msg = "No more results to show."
		elif cmd == "sel":
			allowedTID = getTID(results)
			tid = int(input("Enter twoot ID (TID): "))
			while tid not in allowedTID:
				tid = int(input("Enter a valid ID!: "))
			twootInfo.info(usr, connection, tid)


def executeQuery(connection, keywords, hashtags):
	
	# Build first WHERE clause and query
	if len(keywords) > 0:
		whereClause1 = "WHERE ((LOWER(t1.text) LIKE "
		i = 0
		for word in keywords:
			if i == 0:
				whereClause1 += "'%"+word+"%')"
				i += 1
			else:
				whereClause1 += " OR (LOWER(text) LIKE '%"+word+"%')"
		whereClause1 += ") AND (t1.writer = u1.usr) "

	query1 = "SELECT u1.name, t1.tdate, t1.text, t1.tid " \
			"FROM users u1, tweets t1 " +whereClause1

	# Build second WHERE clause and query
	if len(hashtags) > 0:
		whereClause2 = "WHERE m.term IN ("
		i = 0
		for word in hashtags:
			i += 1
			if i != len(hashtags):
				whereClause2 += "'"+word+"',"
			else:
				whereClause2 += "'"+word+"') "
		whereClause2 += "AND (m.tid = t2.tid) AND (t2.writer = u2.usr)"

		query2 = "SELECT u2.name, t2.tdate, t2.text, t2.tid " \
				"FROM users u2, tweets t2, mentions m " +whereClause2


	# Combine queries if there are both keywords and hashtags
	if (len(keywords) > 0) and (len(hashtags) > 0):
		queryUnion = "("+query1+") UNION ("+query2+")"
	elif (len(keywords) > 0) and (len(hashtags) == 0):
		queryUnion = query1
	elif (len(keywords) == 0) and (len(hashtags) > 0):
		queryUnion = query2

	# Add ORDER BY clause
	queryComplete = "SELECT * FROM ("+queryUnion+") ORDER BY 2 DESC"


	# Execute query
	cursor = connection.cursor()
	cursor.execute(queryComplete)

	return cursor
	

def getKeywords():
	usrInput = input("Enter space-separated keyword(s) to search for:" + '\n')
	keywords = usrInput.lower().strip().split()
	hashtags = []
	
	for word in keywords:
		if re.match("#.*", word) != None:
			hashtags.append(word[1:])
	return keywords, hashtags

def getTID(results):
	# Get CMDs that user is allowed to use
	tids = []
	for result in results:
		tids.append(result[3])
	return tids

def printResults(results):
	printHeader()
	if results == []:
		print("No twoots found.\n\nActions:\nback:\tReturn to feed.")
		return
	for twoot in results:
		print(str(twoot[0]) + " wrote:\t\t" \
			+ str(twoot[1]))# user and date
		print(textwrap.fill(twoot[2], 50)) # Text
		print('\t'*6 + "TID:" + str(twoot[3])) #TID
		print("-"*56)

	print("Actions:\nback: \tReturn to feed.\nmore:\tShow more twoots.\n" \
        "sel:\tSelect twoot.\n")

def printHeader():
	os.system("clear")
	print("Twoot Search")
	print("-"*56)
