import tweepy
from textblob import TextBlob
import re, string, csv, json

import os
import couchdb

#------------------------------------------- ENVIRONMENT DEFINITION -----------------------------------------

# State names, list of strings
STATES = str(os.environ['STATELIST']).split(',')

COUCHDB_IP = os.environ['COUCHDB_IP']
COUCHDB_PORT = os.environ['COUCHDB_PORT']
DB_NAME = os.environ['DATABASE_NAME']

#------------------------------------------------ END DEFINITION --------------------------------------------

# Connect to CouchDB server
couch = couchdb.Server(COUCHDB_IP + ':' + COUCHDB_PORT)

# Connect to Database
db = couch[DB_NAME]

search_term = "#Covid-19 OR Covid-19 OR Covid"
count = 100

# state names, list of strings
# STATES = ["Queensland"]

# filename to save
# SAVE_LOCATION = "covid.csv"
# SAVE_LOCATION = "covid.json"


#-------------------------------------------Twitter API Authentication-----------------------------------------

# Authenticate to Twitter
from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

# Verify Authentication
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

#------------------------------------------------END Authentication---------------------------------------------


# ------------------------------------------------METHODS--------------------------------------------------

def clean(tweet):
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',tweet) # Get rid of www.* or https?://*
    tweet = re.sub('@[^\s]+','',tweet) # Get rid of @username
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet) # Get rid of #
    tweet = re.sub(r'[^\x00-\x7F]+','', tweet) # Get rid of consecutive non-ASCII characters
    tweet = re.sub('[\s]+', ' ', tweet) # Remove additional white spaces
    tweet = tweet.strip('\'"')
    return tweet

def write_to_csv(tweets_iterator, filename, place):
    # 'a+' for additional writing up, 'w+' for overwriting everything
    with open(filename, 'a+', newline='') as f:
        f_writer = csv.writer(f)
        # f_writer.writerow(['Tweet ID', 'Polarity', 'Location'])
        for tweet in tweets_iterator:
            blob = TextBlob(clean(tweet.full_text))
            polarity = blob.sentiment.polarity
            f_writer.writerow([tweet.id, polarity, place])

def write_to_json(tweets_iterator, filename, state):
    record = {}
    record[state] = {}
    for tweet in tweets_iterator:
        blob = TextBlob(clean(tweet.full_text))
        polarity = blob.sentiment.polarity
        record[state][tweet.id] = polarity
    with open(filename, 'a+') as f:
        j_str = json.dumps(record)
        f.write(j_str)

def write_to_couchdb(tweets_iterator, state):
    for tweet in tweets_iterator:
        blob = TextBlob(clean(tweet.full_text))
        polarity = blob.sentiment.polarity
        record = {'semantic':polarity, 'state': state}
        db[tweet.id] = record


# ---------------------------------------------END METHODS--------------------------------------------------


for state in STATES:

    search_place = state + ", Australia"
    places = api.geo_search(query=search_place) 
    place_id = places[0].id

    query = search_term #+ " place:" + place_id #+ " -filter:retweets"
    print(state, place_id)
    tweets = tweepy.Cursor(api.search,
                            q = query,
                            lang = "en",
                            tweet_mode = 'extended',
                            # since = date_since,
                            # until = date_until,
                            # geocode = "-37.7715451,144.8536343, 1mi",
                            ).items(count)
    # save to csv file, with additional writting up
    # write_to_csv(tweets, SAVE_LOCATION, state)
    # write_to_json(tweets, SAVE_LOCATION, state)
    write_to_couchdb(tweets, state)

