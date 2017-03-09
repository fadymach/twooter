import os

def followers(usr, connection):
	#This query selects the id and name of the users that follows the input of :usr
	query = "SELECT u.usr, u.name FROM FOLLOWS f, users u WHERE f.flwer = u.usr and FLWEE = :usr"
	cursor = connection.cursor()
	rows = cursor.execute(query, {'usr': usr}).fetchall()
	printList(rows)
	VALIDINPUT = False
	while (not VALIDINPUT):
		user_input = input(":" )
		if(user_input == "exit"):
			exit()
		try:
			selection = int(user_input)
		except ValueError:
			os.system("clear")
			printList(rows)
			print("Please enter an integer")
			continue 
		else: 
			if(selection > len(rows) or selection < 1):
				os.system("clear")
				printList(rows)
				print("Make a valid selection, please")
				continue
			else:
				VALIDINPUT = True
				print(rows[selection - 1])
				break

def printList(rows):
	print("Which of your follows would you like to see more information about? ")
	for i in range(0, len(rows)):
		print("(%d) %s" %(i+1, rows[i][1]))
	print("    exit")