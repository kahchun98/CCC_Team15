import tweepy
from textblob import TextBlob
import re, string, csv

from mpi4py import MPI

#-------------------------------------------Twitter API Authentication-----------------------------------------

# Authenticate to Twitter
CONSUMER_KEY = "qDsLm9vWLuajh3tDvAV4PAoMF"
CONSUMER_SECRET = "KuTsYvgapkUAVZ0Ry8B4oJ81Z3hywbxDz6hiz4MH8GX9EsNapN"
ACCESS_TOKEN = "1062507160586743808-LnHkPAbLFWa6zySowOjLonzEcK9h98"
ACCESS_TOKEN_SECRET = "g2EiplJWc6goKvzVgE8PhoIEJVTKd5p9vAPcLB60uOC45"

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

def write_to_csv(tweets_iterator, filename, location):
    with open(filename, 'a+', newline='') as f:
        f_writer = csv.writer(f)
        # f_writer.writerow(['Tweet ID', 'Polarity', 'Location'])
        for tweet in tweets_iterator:
            blob = TextBlob(clean(tweet.full_text))
            polarity = blob.sentiment.polarity
            f_writer.writerow([tweet.id, polarity, location])

# ---------------------------------------------END METHODS--------------------------------------------------


# -------------------------------------------MAIN----------------------------------------

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()


if rank == 0:
    SUBURBS = ["Brunswick", "Abbotsford"]
if rank == 1:
    SUBURBS = ["Boronia", "Ferntree Gully"]

search_term = "#F1"
count = 5

SAVE_LOCATION = "test.csv"

# not working
# date_since = "2018-01-01"
# date_until = "2021-05-01"


for suburb in SUBURBS:
    # search_place = suburbs
    search_place =  suburb + ", Melbourne, Australia"
    places = api.geo_search(query=search_place) 
    place_id = places[0].id

    query = search_term + " place:" + place_id #+ " -filter:retweets"

    tweets = tweepy.Cursor(api.search,
                            q = query,
                            lang = "en",
                            tweet_mode = 'extended',
                            # since = date_since,
                            # until = date_until,
                            ).items(count)

    write_to_csv(tweets, SAVE_LOCATION, search_place)
