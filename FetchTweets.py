import twitter
import nltk
import csv

CONSUMER_KEY = 'LAvx9GweIfGkSndmhgpw08EAr'
CONSUMER_SECRET = 'sYHWlWh7uwhdV502vE9HU0YKKEidx51yEcmff0y4MxXEW8fG0S'
ACCESS_TOKEN = '2831320634-PxWMpKUZNxCT111mjauvfJohOi1J8K7SOUWHjEC'
ACCESS_TOKEN_SECRET = '0gCzmpgw0sbIIWzusTfnhyz3GtosCiqy20GLTUePG5S0r'


# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

# Load list of stop words
stopwords = nltk.corpus.stopwords.words('english')

tweets = api.GetSearch(raw_query="q=hillary%20OR%20clinton%20OR%20donald%20OR%20trump%20%23election2016%20lang%3Aen&result_type=recent&count=100&exclude=retweets&exclude=replies")
with open('tweets.csv', 'wb') as csvfile:
    tweetWriter = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting=csv.QUOTE_MINIMAL)
    tweetWriter.writerow(["created_at", "tweet", "favorite_count", "retweet_count", "user_id", "user_followers_count", "user_friends_count", "user_location"])
    for tweet in tweets:
        tweetText = tweet.text.strip() #strip newlines
        tweetText = tweetText.replace(',', '') #strip commas so doesn't interfere with CSV delimiter
        userLocation = tweet.user.location.replace(',', '')
        print tweet
        # print str(count) + " " + tweetText
        tweetWriter.writerow([tweet.created_at.encode('utf-8'), tweetText.encode('utf-8'), tweet.favorite_count, tweet.retweet_count, tweet.user.id, tweet.user.followers_count, tweet.user.friends_count, userLocation.encode('utf-8')])

