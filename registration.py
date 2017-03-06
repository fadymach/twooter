import cx_Oracle as cx
import getpass as gp
import os
import re

def registration(connection):

	def __init__(self):
		print('\n'+"Twooter User Registration")
		print("-------------------------------------------------------------")
		
		getUsr(connection)


def getUsr(connection):
	cursor = connection.cursor()

	name = input("Name: ")
	while len(name) > 20:
		name = input("Name must be less than 20 characters!"+'\n'+"Name: ")

	email = input("Email: ")
	while re.match(".*@.*\..*", email) == None:
		email = input("Invalid email format!"+'\n'+"Email: ")
	while len(email) > 15:
		email = input("Email must be less than 15 characters!"+'\n'+"Email: ")

	city = input("City: ")
	while len(city) > 12:
		city = input("City must be less than 12 characters!"+'\n'+"Email: ")

	timezone = float(input("Timezone: "))
	while (timezone < -12) or (timezone > 14):
		timezone = float(input("Invalid timezone!"+'\n'+"Timezone: "))

	print("Enter a password (Max 4 characters)")
	password = gp.getpass()
	while len(password) > 4:
		print("Password must be less than 4 characters!")
		password = getpass()

	# query to get max user id
	createUsr(connection)

def createUsr(connection):
	
