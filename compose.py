import re
import time 
import cx_Oracle
import os 

def create(usr, connection, replyto = None):
	cursor = connection.cursor()

	tid = getTid(connection)

	writer = usr
	tdate = time.strftime("%d-%b-%Y")
	text = input("Your Twoot: ")

	
	tags = checkforHashtags(text)
	if(tags != []):
		INCLUDESHASHTAGS = True
	else:
		INCLUDESHASHTAGS = False
		

	query = "INSERT INTO tweets VALUES (:1, :2, :3, :4, :5)"
	#Does this need to show the list of tweets that a person can reply to? Not specified. I'm not sure.
	try: 
		cursor.execute(query, (tid, writer, tdate, text, replyto))
	except cx_Oracle.IntegrityError:
		print("Twoot was not created, sorry. Try again")
	else:
		print("Twoot was created!")
		connection.commit()
		if(INCLUDESHASHTAGS):
			for each in tags:
				tag = addToHashtags(each, tid, connection)
				if (tag == None):
					# addToMentions(each, tid, connection)
					pass
				else:
					# addToMentions(tag, tid, connection)
					pass
	finally:
		connection.commit()
		cursor.close()


def getTid(connection):
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


def addToHashtags(tag, tid, connection):
	get_tags_query = "SELECT * FROM hashtags"
	tags_cursor = connection.cursor()
	tagsList = tags_cursor.execute(get_tags_query)
	tagsList = tagsList.fetchall()
	#if tag not in db, add tag to db
	newHashtag = True
	for each in tagsList:
		if each[0].strip() == tag:
			newHashtag = False
			break
	if newHashtag:
		add_tags_query = "INSERT INTO hashtags VALUES (:tag)"
		tags_cursor.execute(add_tags_query, {'tag': tag})
		connection.commit()

	#add tag to mentions
	addToMentions(tag, tid, connection)
	connection.commit()


def addToMentions(tag, tid, connection):
	mention_query = "INSERT INTO mentions VALUES (:tid, :tag)"
	mention_cursor = connection.cursor()
	mention_cursor.execute(mention_query, {'tid': tid, 'tag': tag})
	connection.commit()
	mention_cursor.close()