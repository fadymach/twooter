def main(connection):
	input_valid = False
	while (not input_valid):
		print("Welcome to Twooter")
		choice = input("Login(l) or Register(r)? ")
		if choice.strip().lower() == 'l' or choice.strip().lower() == "login":
			login(connection)
			input_valid = True
		elif choice.strip().lower() == 'r' or choice.strip().lower() == "register":
			#Call register function here. 
			print("This is the register option, delete this line when added a proper function")
			input_valid = True
		else:
			print("Please choose an option")


def login(connection):
	cursor = connection.cursor()
	cursor.execute("SELECT usr, pwd FROM users")
	rows = cursor.fetchall()
	print(rows)
