import os

def menu():
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

	for command in commands:
		print(command[0] + '\t'*2 + command[1])
	print("---------------------------------")



if __name__ == '__main__':
	menu()
