SELECT rtcnt, rpcnt, writer, tdate, text
FROM tweets, (SELECT COUNT(*) as rtcnt
		FROM retweets
		WHERE tid = 19
	), 
	(SELECT COUNT(*) as rpcnt
		FROM tweets
		WHERE replyto IS NOT NULL AND replyto = 19
	) WHERE tid = 19;
