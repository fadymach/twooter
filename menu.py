import os

def menu(connection):
	# Display menu and take user input
	printScreen()

	cmd = input('\n' + '\t' + "       COMMAND: ").strip().lower()

	while cmd not in ["fe","fo","ct","st","su","ml","exit"]:
		os.system("clear")
		printScreen()
		cmd = input('\n' + " ENTER A VALID COMMAND: ").strip().lower()

	if cmd == "fe":
		pass
		# CALL FEED
	elif cmd == "fo":
		pass
		# CALL FOLLOWERS
	elif cmd == "ct":
		pass
		# CALL COMPOSE TWOOT
	elif cmd == "st":
		pass
		# CALL SEARCH TWOOT
	elif cmd == "su":
		pass
		# CALL SEARCH USERS
	elif cmd == "ml":
		pass
		# CALL MANAGE LISTS
	elif cmd == "exit":
		connection.close()
		os.system("clear")
		print("Logged out")


def printScreen():
	os.system("clear")

	print("Main Menu" + '\n')
	print("---------------------------------")
	print("GO TO:" + '\t'*3 + "COMMAND:")
	print("---------------------------------")

	commands = [("Feed         ","FE"), \
				("Followers    ","FO"), \
				("Compose Twoot","CT"), \
				("Search Twoots","ST"), \
				("Search Users ","SU"), \
				("Manage Lists ","ML"), \
				("Logout       ","EXIT")]

	for i in commands:
		print(i[0] + '\t'*2 + i[1])
	print("---------------------------------")

if __name__ == '__main__':
	menu()
