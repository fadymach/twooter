import cx_Oracle as cx
import textwrap, os
import compose

def info(usr, connection, tid):
    try:
        tid = int(tid)
    except Exception:
        return -1

    tid_q = "SELECT tid FROM tweets where tid = :tid"
    query = "SELECT rtcnt, rpcnt, name, tdate, text FROM tweets, users, " \
            "(select count(*) as rtcnt from retweets where tid = :tid), " \
            "(select count(*) as rpcnt from tweets " \
            "where replyto is not null and replyto = :tid) " \
            "WHERE tid = :tid AND writer = usr"

    cursor = connection.cursor()
    cursor.execute(tid_q, {'tid':tid})
    exists = cursor.fetchall()
    if exists==[]:
        return -1
    
    cursor.execute(query, {'tid':tid})
    data = cursor.fetchall()[0]
    # data has one entry containing (rtcnt, rpcnt, writer, tdate, and text)
    #                                   0     1      2       3          4
    sys_msg = ""
    while True:
        display(data)
        print(sys_msg)
        sys_msg = ""

        userin = input("Selection: ").lower()

        if userin=='rep':
            compose.create(usr, connection, tid)
            sys_msg = "Reply posted."
        elif userin=='retw':
            sys_msg = "FUNCTION NOT CURRENTLY AVAILABLE"
        elif userin=='back':
            return 0
        else:
            sys_msg = "INVALID INPUT: Try again."


def display(data):
    os.system("clear")
    print('-'*56)
    print('\n'.join(textwrap.wrap(data[4], 56)))
    bottom = "Written by " + data[2].strip() + " on " + data[3].strftime('%Y-%m-%d at %I:%M%p')
    print("{:>56}".format(bottom))
    print("{:>56}".format("Retweeted "+str(data[0])+" times, "+str(data[1])+" replies."))
    print('-'*56, end='\n\n')
    print("Actions:\nrep: \tReply to this Twoot.\nretw:\tRetwoot this.\n" \
        "back:\tReturn to the previous page.")
