-- HOMEPAGE:        all tweets and retweets from followed users; ordered descending by date
SELECT tid, writer, tdate
FROM
	follows f, 
	(--selection of all tweets and retweets
	select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text
	from tweets t, retweets r
	where t.tid = r.tid
		UNION
	select tid, writer, tdate, text from tweets
	)
WHERE writer = flwee AND flwer = 122;
--replace 122 with id of user currently logged in

-- HOMEPAGE STATS:	can select tweet for stats: no. retweets, no. replies
--eg 19 --> 21, 4
SELECT rtcnt as "# of retweets", rpcnt as "# of replies"
FROM (SELECT COUNT(*) as rtcnt
		FROM retweets
		WHERE tid = 19
	), 
	(SELECT COUNT(*) as rpcnt
		FROM tweets
		WHERE replyto IS NOT NULL AND replyto = 19
	);
-- replace 19 with tweet id


-- TWOOT SEARCH:    all tweets with keyword k as a hashtag or including k; order by date descending


-- USER SEARCH:     first, users whose names match keyword k, ordered by name len ascending
--                  then, users whose cities match k, ordered by city len ascending


-- COMPOSE TWOOT:   save words preceded by a # in hashtags and mentions
--  this will largely be on the python side


-- LIST FOLLOWERS:	list of all users who follow current user.
SELECT flwer FROM follows WHERE flwee=0;
--replace 0 with current user

-- USER DETAILS:	no. tweets, no. followed, no. followers, 3 latest tweets
-- accessed from USER SEARCH and LIST FOLLOWERS
SELECT *
FROM (
	SELECT COUNT(*) AS "# of twoots"
	FROM tweets WHERE writer = 0
	), 
	(
	SELECT COUNT(*) AS "Followed"
	FROM follows WHERE flwer = 0
	), 
	(
	SELECT COUNT(*) AS "Followers"
	FROM follows WHERE flwee = 0
	);

SELECT tdate as "Date", text as "Twoot"
FROM (--selection of all tweets and retweets
	select t.tid as tid, r.usr as writer, t.tdate as tdate, t.text as text
	from tweets t, retweets r
	where t.tid = r.tid
		UNION
	select tid, writer, tdate, text from tweets
	)
WHERE writer = 0;
--replace 0s with id of user you want details of

-- VIEW LISTING OF CURRENT USER'S LISTS
SELECT lname AS "List" FROM lists WHERE owner = 0;
-- replace 0 with current user

-- SEE LISTS CURRENT USER IS ON
SELECT DISTINCT lname AS "List"
FROM includes i
WHERE i.member = 0;
-- replace 0 with current user

-- CREATE AND EDIT LISTS
-- mostly python
