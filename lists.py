import os
import cx_Oracle as cx

def manageLists(usr, connection):
	printManageScreen()
	allowedCMD = ["back","my","on","create","del"]
	
	while True:
		cmd = input("Selection: ").lower()
		while cmd not in allowedCMD:
			cmd = input("Invalid selection! Selection: ")

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
	
	myLists = getMyLists(usr, connection)
	onLists = getOnLists(usr, connection)


def printMyLists(usr, connection):
	# Prints user's lists, and gives option to select list for further action
	printHeader("My Lists")
	queryOutput = getMyLists(usr, connection)
	myLists = []
	for list in queryOutput:
		print(list[0].strip())
		myLists.append(list[0].strip()) # Keep proper list to check selection.
	print("\nActions:\nback: \tReturn to menu.\nsel:\tSelect a list.\n")

	cmd = input("Selection: ").lower()
	while cmd not in ("back","sel"):
		cmd = input("Invalid selection! Selection: ")

	if cmd == "sel":
		selectList(connection, myLists)


def selectList(connection, allowedLists):
	# Displays all users in a list and gives the option to add/delete members
	list = input("Enter list name: ").lower()
	while list not in allowedLists:
		list = input("Enter valid list name!: ").lower()

	printHeader("List: " + list)

	query = "SELECT i.member, u.name FROM includes i, users u " \
			"WHERE i.member = u.usr AND i.lname = :list"
	cursor = connection.cursor()
	results = cursor.execute(query, {'list':list})

	printAList(results)
	# Get input from user with option to add/delete members

	cursor.close()

def printAList(results):
	# Prints users in a list
	print("USER ID" +'\t'+ "NAME")
	for row in results: # FIX THIS
		print("%7d\t" +results[1] % (results[0]))


def getMyLists(usr, connection):
	query = "SELECT lname FROM lists WHERE owner = :usr"
	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	results = cursor.fetchall()
	cursor.close()
	return results


def getOnLists(usr, connection):
	query = "SELECT lname FROM includes WHERE member = :usr"
	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	results = cursor.fetchall()
	cursor.close()
	return results


def printHeader(title):
	os.system("clear")
	print(title + '\n' + '-'*56 +'\n')


def printManageScreen():
	printHeader("Lists")
	print("Actions:\nback: \tReturn to feed.\nmy:\tShow my lists.\n" \
        "on:\tShow lists I am on.\ncreate:\tCreate new list.\n" \
		"del:\tDelete list.\n")
