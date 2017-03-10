import time
import os
import cx_Oracle
import textwrap

def followers(usr, connection, rows = None):
	os.system("clear")
	message = ""
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
			break
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
				message = seeMore(rows[selection - 1], usr, connection)
				break
	return message

#Prints a formated list of the followers with indexes 
def printList(rows):
	print("Which of your follows would you like to see more information about? ")
	for i in range(0, len(rows)):
		print("(%d) %s" %(i+1, rows[i][1]))
	print("    exit")


def seeMore(person, usr, connection):
	message = "" 
	name = person[1].strip()
	info = {'writer':person[0]}
	info2 = {'writer':person[0], 'name':name}
	uid = int(person[0])
	data_cursor = connection.cursor()
	num_tweet_query = "SELECT COUNT(tid) FROM TWEETS WHERE WRITER = :writer"
	num_follows_query = "SELECT COUNT(flwee) FROM FOLLOWS WHERE FLWER = :writer"
	num_followers_query = "SELECT COUNT(flwer) FROM FOLLOWS WHERE FLWEE = :writer"


	num_tweet = data_cursor.execute(num_tweet_query, info).fetchone()[0]
	num_follows = data_cursor.execute(num_follows_query, info).fetchone()[0]
	num_followers = data_cursor.execute(num_followers_query, info).fetchone()[0]

	usr_info = [name, num_tweet, num_follows, num_followers]

	tweets_query = "SELECT tid, :name as author, tdate, text, NULL as replyto, 0 as rt FROM TWEETS WHERE WRITER = :writer ORDER BY tdate"
	tweets = data_cursor.execute(tweets_query, info2)
	tweetsList = tweets.fetchmany(numRows = 3)

	display(tweetsList, 3, usr_info)

	input_valid = False
	while (not input_valid):
		choice = input("Selection:").lower().strip()
		if(choice == "next"):
			tweetsList = tweets.fetchmany(numRows = 3)
			display(tweetsList, 3, usr_info)
			input_valid = True
		elif(choice == "top"):
			pass
		elif(choice == "follow"):
			message = followPerson(usr, info.get("id"), connection)
			input_valid = True
		elif(choice == "back"):
		else:
			print("Please enter a valid choice")
	return message 


def followPerson(usr, id, connection):
	follow_query = "INSERT INTO FOLLOWS VALUES (:usr, :id, :start_date)"
	start_date = time.strftime("%d-%b-%Y")
	add_cursor = connection.cursor()
	message = ""
	try: 
		add_cursor.execute(follow_query, {'id':id, 'usr':usr, 'start_date':start_date})
		connection.commit()
		message = "Followed!"
	except cx_Oracle.IntegrityError:
		message = "You're already following"
	return message

def display(twootdata, n, usr_info, showTID=False):
	# twootdata = list of tuples formatted as (tid, author, date, text, replyto, and rt)
	#										   int	string	date  string string		 int (1 or 0)
	# n = number of items per page
	os.system("clear")
	#usr_info = [name, num_tweet, num_follows, num_followers]
	name = usr_info[0]
	num_tweet = usr_info[1]
	num_follows = usr_info[2]
	num_followers = usr_info[3]
	print("%s's Information Page:" %name)
	print("Number of twoots written: %d" %num_tweet)
	print("Number of people being followed by %s: %d" %(name, num_follows))
	print("Number of people following %s: %d" %(name, num_followers))
	print("Most recent twoots: ")

	for twoot in twootdata:
		print('|' + "-"*55)
		print('|' + twoot[1].strip(), end=' ')
		if twoot[5] == '1': # if it is a retwoot
			print('retwooted:')
		elif twoot[4] != None:
			print('replied to ' + str(twoot[4]).strip() + ':')
		else:
			print('twooted:')
		print('|' + '\n|'.join(textwrap.wrap(twoot[3], 50)))
		print('|' + '\t'*4, end='')
		if showTID:
			print('\t\tTID:'+str(twoot[0]))
		else:
			print('on ' + twoot[2].strftime('%Y-%m-%d'), end='') #date
			print(' at ' + twoot[2].strftime('%I:%M%p'))

	print('|' + "-"*55)
	print('Tw'+'o'*50+'ter!')
	if showTID!=True:
		print("Navigation\n"\
			"next:\tDisplay "+str(n)+" more Twoots.\n"\
			"top: \tReturn to top of feed.\n"\
			"follow:\tFollow " + twoot[1] + " on Twooter."
			"back:\tReturn to previous page.")