import cx_Oracle as cx
import getpass as gp
import os
import re

def registration(connection):

	def __init__(self):
		print('\n'+"User Registration"+'\n')
		print("-------------------------------------------------------------")
		
		getUsr(connection)


def getUsr(connection):
	curs = connection.cursor()

	name = input("Name: ")
	while len(name) > 20:
		name = input("Name must be less than 20 characters!"+'\n'+"Name: ")

	email = input("Email: ")
	while re.match(".*@.*\..*", email) == None:
		email = input("Invalid email format!"+'\n'+"Email: ")
