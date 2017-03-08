import getpass as gp
import re, os

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

	print("Enter a password (max 4 characters)")
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

	cursor.prepare("INSERT INTO users VALUES (" \
		":id, :password, :name, :email, :city, :timezone)")
	cursor.execute(None, \
		{'id':maxID+1, 'password':password, 'name':name, 'email':email, \
		'city':city, 'timezone':timezone})

	# Review account before commit
	os.system("clear")
	print("Review your account")
	print("-----------------------------------------------------------"+'\n')
	print("Name:" + '\t'*3 + name)
	print("Email:" + '\t'*3 + email)
	print("City:" + '\t'*3 + city)
	print("Time zone:" + '\t'*2 + str(timezone))
	print("Your User ID is:" + '\t' + str(maxID+1))
	
	confirm = input('\n' + "Confirm? (y/n) ").strip().lower()
	while confirm not in ["yes", "y", "no", "n"]:
			confirm = input('\n' + "Confirm? (y/n) ").strip().lower()
	
	if (confirm == "yes") or (confirm == "y"):
		connection.commit()
		cursor.close()
		return maxID + 1
	elif (confirm == "no") or (confirm == "n"):
		cursor.close()
		return None
