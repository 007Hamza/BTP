import sys
import tweepy/tweepy
import json

consumer_key="oNeZSSGb1bvZD156W3Cv9A"
consumer_secret="UApZt4Q4rufTsDmwaCfvQzDvhzF1nBOHmyB2UHbRxA"
access_key = "142917712-mgmfkAmPf9e5WQfYSsQfn0eCqhIAmDyorQNUYIBF"
access_secret = "IaMmeioBZNnEgllG4IHPd1evjaYzhRzhRq4Jv33v0" 


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
        for key in tweets.keys():
            if key=='text':
                print tweets[key]
        print 'success'

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['happy'])
