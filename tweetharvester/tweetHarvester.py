import tweepy
from textblob import TextBlob
import re, string, csv, json


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


# ---------------------------------------------END METHODS--------------------------------------------------


search_term = "#Covid-19 OR Covid-19 OR Covid"
count = 100

# state names, list of strings
STATES = []

# filename to save
SAVE_LOCATION = "covid.csv"

for state in STATES:

    search_place = state + ", Australia"
    places = api.geo_search(query=search_place) 
    place_id = places[0].id

    query = search_term + " place:" + place_id #+ " -filter:retweets"

    tweets = tweepy.Cursor(api.search,
                            q = query,
                            lang = "en",
                            tweet_mode = 'extended',
                            # since = date_since,
                            # until = date_until,
                            # geocode = "-37.7715451,144.8536343, 1mi",
                            ).items(count)

    # save to csv file, with additional writting up
    write_to_csv(tweets, SAVE_LOCATION, search_place)
