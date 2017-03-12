# initial feed; pages of 5 tweets, option of more info.
import cx_Oracle as cx
import textwrap, os
import searchTwoots, compose, followers, twootInfo, userSearch, lists

def feed(usr, connection):
	showTID = False

	query = "SELECT tid, u.name AS author, tdate, text, repname AS replyto, rt " \
			"FROM users u, (select flwer, flwee from follows union select :usr as flwer, :usr as flwee from dual), " \
				"(select t.tid as tid, r.usr as writer, r.rdate as tdate, t.text as text, t.replyto as replyto, '1' as rt " \
				 "from tweets t, retweets r " \
				 "where t.tid = r.tid " \
			"UNION " \
				"select tid, writer, tdate, text, replyto, '0' as rt from tweets) " \
				"LEFT OUTER JOIN (select tid as reptid, name as repname from tweets, users where writer = usr) ON replyto = reptid " \
			"WHERE writer = flwee AND flwer = :usr AND u.usr = writer " \
			"ORDER BY tdate DESC"

	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})
	system_message = ""

	twootdata = cursor.fetchmany(numRows = 5)
	while True:
		display(twootdata, 5, showTID)
		print('\n'+system_message)
		system_message = ""

		userin = input("Selection: ").lower().strip()
		if userin=='new':
			# create new twoot
			compose.create(usr, connection)
			# refresh feed data
			cursor.execute(query, {'usr':usr})
			twootdata = cursor.fetchmany(numRows = 5)
		elif userin=='info':
			while True:
				info_result = 0
				# shot TIDs
				display(twootdata, 5, True)
				print(system_message)
				system_message=""
				# get TID from user
				info_select = input("Enter TID of the Twoot you want to expand: ")
				if info_select=='c':
					break
				# attempt to get info
				info_result = twootInfo.info(usr, connection, info_select)
				if info_result==-1:
					system_message = "Twoot does not exist. Enter c to cancel."
				elif info_result==0:
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
				userSearch.search(usr, connection)
			elif searchin=='t':
				searchTwoots.searchTwoots(usr, connection)
				# refresh feed data
				cursor.execute(query, {'usr':usr})
				twootdata = cursor.fetchmany(numRows = 5)
			elif searchin=='c':
				system_message += "Search Canceled"
			else:
				system_message = "INVALID INPUT: Search Canceled"
		elif userin=='sheep':
			followers.followers(usr, connection)
		elif userin=='list':
			lists.manageLists(usr, connection)
		elif userin=='exit':
			cursor.close()
			return
		else:
			system_message = "INVALID SELECTION: see Navigation above."

	# each twoot consists of tid, author, date, text, replyto, and rt
	#						  0		1		2	  3		4			5

def display(twootdata, n, showTID=False):
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
		print('|' + '\t'*4, end='')
		if showTID:
			print('\t\tTID:'+str(twoot[0]))
		else:
			print('on ' + twoot[2].strftime('%Y-%m-%d'), end='') #date
			print(' at ' + twoot[2].strftime('%I:%M%p'))

	print('|' + "-"*55 + '\n')
	print('#'*56)
	if showTID!=True:
		print("Navigation\n"\
			"new: \tCompose a new Twoot.\n"\
			"info:\tGet statistics about or reply to a specific tweet.\n"
			"next:\tDisplay "+str(n)+" more Twoots.\n"\
			"top: \tReturn to top of feed.\n"\
			"search:\tSearch for users or individual twoots.\n"\
			"sheep:\tDisplay a list of your devoted followers.\n"\
			"list:\tOpen list manager.\n"
			"exit:\tClose Twooter.")
