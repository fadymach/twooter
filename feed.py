# initial feed; pages of 5 tweets, option of more info.
import cx_Oracle as cx
import textwrap, os
import searchTwoots, compose

def feed(usr, connection):

	test = "SELECT tid, writer, tdate FROM follows f, (select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text from tweets t, retweets r where t.tid = r.tid UNION select tid, writer, tdate, text from tweets) WHERE writer = f.flwee AND f.flwer = :usr"
	query = "SELECT tid, u.name AS author, tdate, text, u1.name AS replyto, rt " \
			"FROM users u, (select flwer, flwee from follows union select :usr as flwer, :usr as flwee from dual), " \
				"(select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text, t.replyto as replyto, '1' as rt " \
				 "from tweets t, retweets r " \
				 "where t.tid = r.tid " \
			"UNION " \
				"select tid, writer, tdate, text, replyto, '0' as rt from tweets) " \
				"LEFT OUTER JOIN users u1 ON replyto = u1.usr " \
				 "WHERE writer = flwee AND flwer = :usr AND u.usr = writer " \
			"ORDER BY tdate DESC"

	

	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	system_message = ""

	twootdata = cursor.fetchmany(numRows = 5)
	while True:
		display(twootdata, 5)
		print('\n'+system_message)
		system_message = ""

		userin = input("Selection: ").lower()
		if userin=='new':
			# create new twoot
			compose.create(usr, connection)
			# refresh feed data
			cursor.execute(query, {'usr':usr})
			twootdata = cursor.fetchmany(numRows = 5)
		elif userin=='next':
			newdata = cursor.fetchmany(numRows = 5)
			if newdata == []:
				display(twootdata, 5)
				system_message = "No more twoots to display."
			else:
				twootdata = newdata
		elif userin=='top':
			cursor.execute(query, {'usr':usr})
			twootdata = cursor.fetchmany(numRows = 5)
		elif userin=='search':
			searchin = input("Search for users (u) or tweets (t)? (c to cancel)").lower()
			if searchin=='u':
				system_message = "user "
			elif searchin=='t':
				searchTwoots.searchTwoots(connection)
			elif searchin=='c':
				pass
			else:
				system_message = "INVALID INPUT: "
			system_message += "Search Canceled"

		elif userin=='exit':
			cursor.close()
			return
		else:
			display(twootdata, 5)
			system_message = "INVALID SELECTION: see Navigation above."


	#twootdata = cursor.fetchmany(numRows = 5)
	#display(twootdata, 5)

	# each twoot consists of tid, author, date, text, replyto, and rt
	#						  0		1		2	  3		4			5

def display(twootdata, n):
	# twootdata = list of tuples formatted as (tid, author, date, text, replyto, and rt)
	#										   int	string	date  string string		 int (1 or 0)
	# n = number of items per page
	os.system("clear")

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
		print('|' + '\t'*4 + 'on ' + twoot[2].strftime('%Y-%m-%d'), end='') #date
		print(' at ' + twoot[2].strftime('%I:%M%p'))

	print('|' + "-"*55)
	print('/'*56)
	print("Navigation\n"\
		"new: \tCompose a new Twoot.\n"
		"next:\tDisplay "+str(n)+" more Twoots.\n"\
		"top: \tReturn to top of feed.\n"\
		"search:\tSearch for users or individual twoots.\n"
		"exit:\tClose Twooter.")