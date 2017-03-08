import re
import time 
import cx_Oracle
import os 

def create(connection, usr):
	cursor = connection.cursor()

	tid = getTweets(connection)

	writer = usr
	tdate = time.strftime("%d-%b-%Y")
	text = input("Your Twoot: ")

	INCLUDESHASHTAGS = False
	tags = checkforHashtags(text)
	if(tags != []):
		INCLUDESHASHTAGS = True
		
		

	INTFLAG = False
	INPUTVALID = False
	while(not INPUTVALID):
		reply = input("Is this twoot a reply to someone? (yes, no) ")
		os.system("clear")
		if reply.strip().lower() == 'y' or reply.strip().lower() == "yes":
			while(not INTFLAG):
				try: 
					replyto = input("Reply to which tweet? ")
					test = int(replyto)
				except ValueError:
					os.system("clear")
					print("Please enter an integer")
					continue
				else:
					INTFLAG = True
					break
			INPUTVALID = True
		elif reply.strip().lower() == 'n' or reply.strip().lower() == "no":
			replyto = None
			INPUTVALID = True
		elif reply.strip().lower() == "exit":
			print("Twoot was not created. Exiting")
			quit()
		else:
			print("Please choose an option")

	query = "INSERT INTO tweets VALUES (:1, :2, :3, :4, :5)"


	#Does this need to show the list of tweets that a person can reply to? Not specified. I'm not sure.
	try: 
		cursor.execute(query, (tid, writer, tdate, text, replyto))
	except cx_Oracle.IntegrityError:
		print("Twoot was not created, sorry. Try again")
	else:
		print("Twoot was created!")
		if(INCLUDESHASHTAGS):
			for each in tags:
				tag = addToHashtags(each, connection)
				if (tag == None):
					addToMentions(each, tid, connection)
				else:
					addToMentions(tag, tid, connection)
	finally:
		connection.commit()
		cursor.close()


def getTweets(connection):
	#This function gets the largest number from the tweet ids. It will then add one to that number
	# and return it so that the new twoot can have a unique id
	get_query = "SELECT max(tid) from tweets"
	get_cursor = connection.cursor()
	rows = get_cursor.execute(get_query).fetchall()
	temp = rows[0][0]
	get_cursor.close()
	return (temp + 1)


def checkforHashtags(text):
	hashtags = re.findall("#(\w+)", text)
	return hashtags


def addToMentions(tag, tid, connection):
	
	add_query = "INSERT INTO mentions VALUES (:tid, :tag)"
	add_cursor = connection.cursor()
	add_cursor.execute(add_query, {'tid' : tid, 'tag' : tag})
	connection.commit()
	add_cursor.close()

def addToHashtags(tag, connection):
	get_tags_query = "SELECT * FROM hashtags"
	add_tags_query = "INSERT INTO hashtags VALUES (:tag)"
	tags_cursor = connection.cursor()
	tagList = tags_cursor.execute(get_tags_query).fetchall()

	for each in tagList:
		if tag == each[0]:
			value = tag
		else:
			#TODO DOESNT WORK 
			tags_cursor.execute(add_tags_query, {'tag': tag})
			value = None

	connection.commit()
	tags_cursor.close()
	return value 