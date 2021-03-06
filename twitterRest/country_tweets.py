# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import MySQLdb as mdb

REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"

CONSUMER_KEY = "oNeZSSGb1bvZD156W3Cv9A" 
CONSUMER_SECRET = "UApZt4Q4rufTsDmwaCfvQzDvhzF1nBOHmyB2UHbRxA" 

OAUTH_TOKEN = "142917712-mgmfkAmPf9e5WQfYSsQfn0eCqhIAmDyorQNUYIBF"
OAUTH_TOKEN_SECRET = "IaMmeioBZNnEgllG4IHPd1evjaYzhRzhRq4Jv33v0"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

if __name__ == "__main__":
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = get_oauth() 
        con = mdb.connect('localhost' , 'root' , 'admin' , 'happiness_index')
        cur = con.cursor()
        cur.execute("SELECT * from geo_tweets")
        con.commit()
        numrows = int(cur.rowcount)
        cur1 = con.cursor()
        for x in range(0 , numrows):
            row = cur.fetchone()
            latitude = row[3]
            longitude = row[2]
            r = requests.get(url="https://api.twitter.com/1.1/geo/reverse_geocode.json?lat="+str(latitude)+"&long="+str(longitude), auth=oauth)
            result = r.json()
            country = result['result']['places'][1]['contained_within'][0]['country_code'] 
            cur1.execute("update geo_tweets SET place = %s WHERE id = %s" , (country , row[0]))
            print "success " + str(row[0]) + "\n"

