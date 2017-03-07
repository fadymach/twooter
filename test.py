# This module is only used to test fucntions.
# To be deleted upon submission.


import cx_Oracle as cx
import getpass as gp
import os
import registration

def main():

	os.system("clear")

	print("Oracle connection:")
	print("-----------------------------------------------------------"+'\n')
	
	# Get Oracle credentials
	usr_oracle = input("Oracle username: ")
	pass_oracle = gp.getpass()
	# Connect to Oracle
	con = cx.connect(usr_oracle, pass_oracle, "gwynne.cs.ualberta.ca:1521/CRS")
	
	os.system("clear")
	
	registration.register(con)
	
	# Close cursor and connection
	con.close()

	clear = input("Clear screen? (y/n) ")
	if clear == "y":
		os.system('clear')


if __name__ == '__main__':
	main()