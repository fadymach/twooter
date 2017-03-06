import cx_Oracle
import getpass
import twitterLogin
import os

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
	user = input("Enter database username: ")
	password = getpass.getpass('Enter database password: ')
	(USERNAME, PASSWORD) = getCredentials()
	connection = createConnection(USERNAME, PASSWORD)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM movies")	
	for row in cursor:	
		print(row[0])
	cursor.close()
	connection.close()

def debugMain():
	(USERNAME, PASSWORD) = getCredentials()
	connection = createConnection(USERNAME, PASSWORD)
	cursor = connection.cursor()
	cursor.execute("SELECT * FROM users")	
	for row in cursor:	
		print(row[0], row[1])
	twitterLogin.main()
	cursor.close()
	connection.close()


# main()
debugMain()