import time
import os
import cx_Oracle

def followers(usr, connection, rows = None):
	#This query selects the id and name of the users that follows the input of :usr
	query = "SELECT u.usr, u.name FROM FOLLOWS f, users u WHERE f.flwer = u.usr and FLWEE = :usr"
	cursor = connection.cursor()
	if(rows == None):
		rows = cursor.execute(query, {'usr': usr}).fetchall()
	printList(rows)
	VALIDINPUT = False
	while (not VALIDINPUT):
		user_input = input(":" )
		if(user_input == "exit"):
			exit()
		try:
			selection = int(user_input)
		except ValueError:
			os.system("clear")
			printList(rows)
			print("Please enter an integer")
			continue 
		else: 
			if(selection > len(rows) or selection < 1):
				os.system("clear")
				if(searchFlag == True):
					printList(rows)
				else:
					printList(rows)
				print("Make a valid selection, please")
				continue
			else:
				VALIDINPUT = True
				seeMore(rows[selection - 1], usr, connection)
				break

#Prints a formated list of the followers with indexes 
def printList(rows):
	print("Which of your follows would you like to see more information about? ")
	for i in range(0, len(rows)):
		print("(%d) %s" %(i+1, rows[i][1]))
	print("    exit")


def seeMore(person, usr, connection):
	index = 1 
	name = person[1].strip()
	info = {'id':person[0]}
	data_cursor = connection.cursor()
	num_tweet_query = "SELECT COUNT(tid) FROM TWEETS WHERE WRITER = :id"
	num_follows_query = "SELECT COUNT(flwee) FROM FOLLOWS WHERE FLWER = :id"
	num_followers_query = "SELECT COUNT(flwer) FROM FOLLOWS WHERE FLWEE = :id"


	num_tweet = data_cursor.execute(num_tweet_query, info).fetchone()[0]
	num_follows = data_cursor.execute(num_follows_query, info).fetchone()[0]
	num_followers = data_cursor.execute(num_followers_query, info).fetchone()[0]

	printData(name, num_tweet, num_follows, num_followers, info, data_cursor, index)

	print("-- Follow %s (f)" %name)
	print("-- Exit")
	input_valid = False
	while (not input_valid):
		choice = input(":")
		if(choice.lower().strip() == 'y' or choice.lower().strip() == "yes"):
			printData(name, num_tweet, num_follows, num_followers, info, data_cursor, index)
			input_valid = True
		elif(choice.lower().strip() == 'f' or choice.lower().strip() == "follow"):
			followPerson(usr, info.get("id"), connection)
			pass
			input_valid = True
		elif(choice.lower().strip() == "exit"):
			exit()
		else:
			print("Please enter a valid choice")


def printData(name, num_tweet, num_follows, num_followers, info, data_cursor, index):
	os.system("clear")
	print("%s's Information Page:" %name)
	print("Number of twoots written: %d" %num_tweet)
	print("Number of people being followed by %s: %d" %(name, num_follows))
	print("Number of people following %s: %d" %(name, num_followers))
	print("Most recent twoots: ")

	tweets_query = "SELECT text, ROW_NUMBER() over (ORDER BY tdate) FROM TWEETS WHERE WRITER = :id"
	counter = 0
	tweets = data_cursor.execute(tweets_query, info)
	rows = tweets.fetchone()
	tweetsList = []
	while rows:
		tweetsList.append(rows)
		counter += 1
		print(rows)
		rows = tweets.fetchone()


	if (len(tweetsList) > 2):
		print("See more Twoots? (y)")


def followPerson(usr, id, connection):
	follow_query = "INSERT INTO FOLLOWS VALUES (:usr, :id, :start_date)"
	start_date = time.strftime("%d-%b-%Y")
	add_cursor = connection.cursor()
	try: 
		add_cursor.execute(follow_query, {'id':id, 'usr':usr, 'start_date':start_date})
		connection.commit()
	except cx_Oracle.IntegrityError:
		print("You're already following")
		