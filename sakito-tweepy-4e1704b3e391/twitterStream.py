import sys
import tweepy
import json
import MySQLdb as mdb
consumer_key="oNeZSSGb1bvZD156W3Cv9A"
consumer_secret="UApZt4Q4rufTsDmwaCfvQzDvhzF1nBOHmyB2UHbRxA"
access_key = "142917712-mgmfkAmPf9e5WQfYSsQfn0eCqhIAmDyorQNUYIBF"
access_secret = "IaMmeioBZNnEgllG4IHPd1evjaYzhRzhRq4Jv33v0" 

con = mdb.connect('localhost' , 'root' , 'admin' , 'happiness_index');
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.text

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream
    
    def on_data(self, data):
        print 'start'
        tweets = json.loads(data)
        print tweets
        print '----------------------------------------------'
        with con:
            cur =con.cursor()
            cur.execute("INSERT INTO Tweets(USER_ID , USER_NAME , TWEET_STRING , SCREEN_NAME) VALUES (%s , %s , %s , %s)" , (tweets['id'] , tweets['user']['name'].encode('utf-8') , tweets['text'].encode('utf-8') , tweets['user']['screen_name'].encode('utf-8')))
        print tweets['text']
        print tweets['id']
        print tweets['user']['screen_name']
        print tweets['user']['name']
        print 'success'

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['Kejriwal'])
