
import tweepy
from textblob import TextBlob

# Step 1 - Authenticate
consumer_key = '3jvQrG5lIcvSvH2r5049Ft7cC'
consumer_secret = 'fMaVbZTbyh6E9OHHauGX3gGnA5bldZDqFRSwr3Bmjfjl0Qu6vp'

access_token = '2940741810-8KQcn8I5m2pxYapAgtotGVs64ZEHGlNPAXTuaPR'
access_token_secret = 'OKp2stysqmPsofoYVV4JTgt7Bm1jtpEJ8u4kQoKru5YaC'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Step 3 - Retrieve Tweets
public_tweets = api.search('Modi')


for tweet in public_tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    print("")