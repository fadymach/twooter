import getpass
import os

def main(connection):
	input_valid = False
	while (not input_valid):
		os.system("clear")


		banner = open("banner.txt", 'r')
		bird = banner.read()
		banner.close()
		print(bird)

		print("Welcome to Twooter")
		

		choice = input("Login(l) or Register(r)? ")
		if choice.strip().lower() == 'l' or choice.strip().lower() == "login":
			username = login(connection)
			input_valid = True
		elif choice.strip().lower() == 'r' or choice.strip().lower() == "register":
			#Call register function here. 
			print("This is the register option, delete this line when added a proper function")
			input_valid = True
		elif choice.strip().lower() == "exit":
			quit()
		else:
			print("Please choose an option")
	return username


def login(connection):
	os.system("clear")
	LOGGEDIN = False 
	LOGINATTEMPT = 0


	#No validation needed for password. If password is wrong, no login allowed.
	cursor = connection.cursor()

	#Select the username and password rows from the users table
	#Will compare the entered information to see if vaid login exists
	cursor.execute("SELECT usr, pwd FROM users")
	rows = cursor.fetchall()
	
	username = getUsername()

	while(not LOGGEDIN and LOGINATTEMPT < 3):
		LOGINATTEMPT += 1
		os.system("clear")
		print("Attempt Number %d/3" %LOGINATTEMPT)
		password = getpass.getpass()
		credentials = (username, password)
		for row in rows:
			if(credentials == row):
				os.system("clear")
				#TODO
				print("Login Success -- Need to add functionality here")	
				LOGGEDIN = True
	#Must close the cursor here, but the connection is closed in main.py. If program doesn't end up in main.py, must close it in your file.
	cursor.close()
	if(not LOGGEDIN):
		os.system("clear")
		print("Username and/or Password Incorrect")
		exit()
	else:
		return username
	
 


def getUsername():
	USERVALID = False
	#Validate the input of username as an integer
	while(USERVALID == False):	
		try:
			user_input = input("Please enter your unique User ID: ")
			username = int(user_input)
		except ValueError:
			os.system("clear")
			print("Please enter an integer")
			continue
		else: 
			USERVALID = True
			break
	return username
