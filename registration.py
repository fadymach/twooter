import getpass as gp
import re

def register(connection):
	os.system("clear")
	print('\n'+"Twooter User Registration")
	print("-------------------------------------------------------------")

	getUsr(connection)


def getUsr(connection):
	cursor = connection.cursor()

	# Get new user info
	name = input("Name: ")
	while len(name) > 20:
		name = input("Name must be less than 20 characters!"+'\n'+"Name: ")

	email = input("Email: ")
	while re.match(".*@.*\..*", email) == None:
		email = input("Invalid email format!"+'\n'+"Email: ")
	while len(email) > 15:
		email = input("Email must be less than 15 characters!"+'\n'+"Email: ")

	city = input("City: ")
	while len(city) > 12:
		city = input("City must be less than 12 characters!"+'\n'+"Email: ")

	timezone = float(input("Timezone: "))
	while (timezone < -12) or (timezone > 14):
		timezone = float(input("Invalid timezone!"+'\n'+"Timezone: "))

	print("Enter a password (Max 4 characters)")
	password = gp.getpass()
	while len(password) > 4:
		print("Password must be less than 4 characters!")
		password = getpass()

	# Query maximum user ID
	maxID_query = "SELECT MAX(usr) FROM users"
	maxID_result = cursor.execute(maxID_query)
	maxID = cursor.fetchone()[0]
	cursor.close()

	createUsr(connection, name, email, city, timezone, password, maxID)


def createUsr(connection, name, email, city, timezone, password, maxID):
	# Executes SQL statement to insert new user
	cursor = connection.cursor()

	insert_statement = "INSERT INTO users " \
		"VALUES (" +str(maxID+1)+ "," +password+ "," +name+ "," +email+ "," \
		+city+ "," +str(timezone)+ ")"

	cursor.execute(insert_statement)

	# Review account before commit
	os.system("clear")
	print("Review your account")
	print("-----------------------------------------------------------"+'\n')
	print("Name:" + '\t' + name)
	print("Email:" + '\t' + email)
	print("City:" + '\t' + city)
	print("Time zone:" + '\t' + str(timezone))
	print("Your User ID is:" + '\t' + str(maxID+1))
	
	confirm = lower(input("Confirm? (y/n) "))
	while (confirm != "yes") or (confirm != "y") \
		or (confirm != "no") or (confirm != "n"):
			confirm = lower(input("Confirm? (y/n) "))
	
	if (confirm == "yes") or (confirm == "y"):
		cursor.commit()
		# CALL HOME SCREEN
	elif (confirm == "no") or (confirm == "n"):
		cursor.rollback()
		# RETURN TO LOGIN SCREEN






















