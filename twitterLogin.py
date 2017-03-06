def main():
	input_valid = False
	while (not input_valid):
		choice = input("Login(l) or Register(r)? ")
		if choice.strip().lower() == 'l' or choice.strip().lower() == "login":
			print("login")
			input_valid = True
		elif choice.strip().lower() == 'r' or choice.strip().lower() == "register":
			#Call register function here. 
			print("reg")
			input_valid = True
		else:
			print("Please choose an option")


def login():
	pass




