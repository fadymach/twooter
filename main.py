import cx_Oracle
import getpass
import logReg
import os
import compose
import feed

#Reads username and password from file. Format it with username and password on their own line
def getCredentials():
	file = open("credentials.txt", "r")
	info = file.readlines()
	USERNAME = info[0].strip()	
	PASSWORD = info[1].strip()
	return USERNAME, PASSWORD

def createConnection(USERNAME, PASSWORD):
	connection = cx_Oracle.connect(USERNAME, PASSWORD, "gwynne.cs.ualberta.ca:1521/CRS")
	return connection


def main():
	USERNAME = input("Enter database username: ")
	PASSWORD = getpass.getpass('Enter database password: ')
	connection = createConnection(USERNAME, PASSWORD)
	try:
		connection.ping()
	except cx_Oracle.DatabaseError:
		print(cx_Oracle.DatabaseError.message)
	else:
		os.system("clear")
		usr = logReg.main(connection)
		feed(usr, connection)
	finally:
		connection.close()
		cursor.close()



def debugMain():
	(USERNAME, PASSWORD) = getCredentials()
	connection = createConnection(USERNAME, PASSWORD)
	try:
		connection.ping()
	except cx_Oracle.DatabaseError:
		print(cx_Oracle.DatabaseError.message)
	else:
		os.system("clear")
		usr = logReg.main(connection)
		compose.create(connection, usr)
	finally:
		print("Program ended up in main.py -- The connection is closed properly")
		connection.close()


# main()
debugMain()
