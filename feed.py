# initial feed; pages of 5 tweets, option of more info.
import cx_Oracle as cx

def feed(usr, connection):

	test = "SELECT tid, writer, tdate FROM follows f, (select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text from tweets t, retweets r where t.tid = r.tid UNION select tid, writer, tdate, text from tweets) WHERE writer = f.flwee AND f.flwer = :usr"
	query = "SELECT tid, u.name AS author, tdate, text, replyto " \
			"FROM follows f, users u, " \
				"(select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text, t.replyto as replyto " \
				 "from tweets t, retweets r " \
				 "where t.tid = r.tid " \
			"UNION " \
				"select tid, writer, tdate, text, replyto from tweets) " \
				 "WHERE writer = f.flwee AND f.flwer = :usr AND u.usr = writer "

	

	cursor = connection.cursor()
	cursor.execute(query, {'usr':usr})

	print(cursor.fetchmany(numRows = 5))	


	# for i in range(len(results)):
	# if results[i][3] != None:
	# 	print("Reply to: " + str(results[i][3])) # Reply to
	# print("---------------------------------------------------")
	# print(str(results[i][0]) + '\t'*2 + str(results[i][1])) # User and date
	# print(textwrap.fill(results[i][2], 50)) # Text
	# print('\n')
	# i += 1

	print("-----------------------------------------------------")
	print("Navigation")