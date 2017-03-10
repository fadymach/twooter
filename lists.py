import os
import cx_Oracle as cx

def manageLists(usr, connection):
	printScreen()

def getMyLists(usr, connection):
	query = ("SELECT lname FROM lists WHERE owner = :usr")
	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr}
	return cursor.fetchall()

def printScreen():
	os.system("clear")
	print("Lists\n" + '-'*56)
