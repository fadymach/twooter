import os, time
import cx_Oracle as cx

def manageLists(usr, connection):
	allowedCMD = ["back","my","on","create","del"]
	descriptions = ["Return to feed","Show my lists","Show lists I am on", \
		"Create new list","Delete list"]

	while True:
		printHeader("Lists")
		cmd = getInput(allowedCMD, descriptions)

		if cmd == "back":
			break
		elif cmd == "my":
			printMyLists(usr, connection)
		elif cmd == "on":
			printOnLists(usr, connection)
		elif cmd == "create":
			createList(usr, connection)
		elif cmd == "del":
			deleteList(usr, connection)

def createList(usr, connection):
	printHeader("Create List")
	lname = input("Enter unique list name: ").lower().strip()
	while len(lname) > 12:
		lname = input("Name must be less than 12 characters! Name: ").lower().split()

	query = "INSERT INTO lists VALUES ('"+lname+"', "+str(usr)+")"
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		connection.commit()
	except cx.IntegrityError:
		print("List name is already taken! Returning back to menu...")
		time.sleep(4)
	
	cursor.close()


def printOnLists(usr, connection):
	# Prints the lists that a user is on
	allowedLists = []
	queryOutput = getOnLists(usr, connection)

	allowedCMD = ["back", "sel"]
	descriptions = ["Return to lists menu", "Select a list"]
	while True:
		printHeader("Lists that I am on")
		for list in queryOutput:
			print(list[0].strip())
			allowedLists.append(list[0].strip())
		
		cmd = getInput(allowedCMD, descriptions)
		if cmd == "back":
			break
		elif cmd == "sel":
			selectNoEditList(connection, allowedLists)
			
			
def selectNoEditList(connection, allowedLists):
	# Show users in a list, w/o options to add/delete members
	list = input("Enter a list name: ").strip().lower()
	while list not in allowedLists:
		list = input("Enter valid list name!: ").strip().lower()
		if list == "back" and "back" not in allowedLists:
			return
	
	results = selectListQuery(connection, list)
	printAList(results)

	allowedCMD = ["back"]
	descriptions = ["Return to lists"]
	while True:
		cmd = getInput(allowedCMD, descriptions)
		if cmd == "back":
			break


def printMyLists(usr, connection):
	# Prints user's lists, and gives option to select list for further action
	printHeader("My Lists")
	
	queryOutput = getMyLists(usr, connection)
	myLists = []
	for list in queryOutput:
		print(list[0].strip())
		myLists.append(list[0].strip()) # Keep proper list to check selection
	
	allowedCMD = ["back","sel"]
	descriptions = ["Return to lists menu","Select a list"]
	cmd = getInput(allowedCMD, descriptions)

	if cmd == "sel":
		selectList(connection, myLists)


def selectList(connection, allowedLists):
	# Displays all users in a list and gives the option to add/delete members
	list = input("Enter list name: ").strip().lower()
	while list not in allowedLists:
		list = input("Enter valid list name!: ").strip().lower()
		if list == "back" and "back" not in allowedLists:
			return

	# Create and execute query
	results = selectListQuery(connection, list)

	# Display results and get user input
	allowedCMD = ["back","add","del"]
	descriptions = ["Return to lists", "Add member", "Remove member"]
	while True:
		printHeader("List: " + list)
		printAList(results)
		cmd = getInput(allowedCMD, descriptions)

		if cmd == "back":
			break
		elif cmd == "add":
			addToList(connection, list)
			results = selectListQuery(connection, list) # Update list to print
		elif cmd == "del":
			delFromList(connection, list)
			results = selectListQuery(connection, list) # Update list to print


def addToList(connection, list):
	isInt = False
	while not isInt:
		try:
			usrToAdd = input("User ID of user to add: ")
			usrToAdd = int(usrToAdd)
			isInt = True
		except ValueError:
			print("User ID must be integer!")

	query = "INSERT INTO includes VALUES ('"+list+"', "+str(usrToAdd)+")"
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		cursor.close()
		connection.commit()
	except cx.IntegrityError:
		print("User does not exist!")
		time.sleep(3)


def delFromList(connection, list):
	isInt = False
	while not isInt:
		try:
			usrToDel = input("User ID of user to delete: ")
			usrToDel = int(usrToDel)
			isInt = True
		except ValueError:
			print("User ID must be integer!")

	query = "DELETE FROM includes " \
			"WHERE lname = '"+list+"' AND member = "+str(usrToDel)
	cursor = connection.cursor()
	cursor.execute(query)
	cursor.close()
	connection.commit()


def printAList(results):
	# Prints users in a list
	print("USER ID" +'\t'*2+ "NAME")
	for row in results:
		print("%7d\t\t %s" % (row[0], row[1]))


# GetLists functions -----------------------------------------------------------
def getMyLists(usr, connection):
	# Get lists that a user owns
	query = "SELECT lname FROM lists WHERE owner = :usr"
	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	results = cursor.fetchall()
	cursor.close()
	return results

def getOnLists(usr, connection):
	# Get lists that a user is on
	query = "SELECT lname FROM includes WHERE member = :usr"
	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	results = cursor.fetchall()
	cursor.close()
	return results

def selectListQuery(connection, list):
	# Query used in selectList function.
	query = "SELECT i.member, u.name FROM includes i, users u " \
			"WHERE i.member = u.usr AND LOWER(i.lname) = '"+list+"'"
	cursor = connection.cursor()
	cursor.execute(query)
	results = cursor.fetchall()
	cursor.close()
	return results


# Administrative functions -----------------------------------------------------
def printHeader(title):
	os.system("clear")
	print(title + '\n' + '-'*56 +'\n')

def getInput(allowedCMD, descriptions):
	# Given commands and their descriptions, get input from user
	menu = "\nActions:\n"
	for i in range(len(allowedCMD)):
		menu += allowedCMD[i] + ":\t" + descriptions[i] + ".\n"
	print(menu)
	
	cmd = input("Selection: ").strip().lower()
	while cmd not in allowedCMD:
		cmd = input("Invalid selection! Selection: ").strip().lower()
	return cmd
