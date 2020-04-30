import json
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

# Load WW_trends and US_trends data into the the given variables respectively
WW_trends = json.loads(open('WWTrends.json').read())
US_trends = json.loads(open('USTrends.json').read()) 

print(WW_trends)
print(US_trends)

# Pretty-printing the results. First WW and then US trends.
print("WW trends:")
print(json.dumps(WW_trends, indent=1))

print("\n", "US trends:")
print(json.dumps(US_trends, indent=1))

# Extracting all the WW trend names from WW_trends
world_trends = set([trend['name'] for trend in WW_trends[0]['trends']])

# Extracting all the US trend names from US_trends
us_trends = set([trend['name'] for trend in US_trends[0]['trends']]) 

# Getting the intersection of the two sets of trends
common_trends = world_trends.intersection(us_trends)

# Inspecting the data
print(world_trends, "\n")
print(us_trends, "\n")
print (len(common_trends), "common trends:", common_trends)

# Loading the data
tweets = json.loads(open('WeLoveTheEarth.json').read())

# Inspecting some tweets
tweets[0:2]

# Extracting the text of all the tweets from the tweet object
texts = [tweet['text'] for tweet in tweets]

# Extracting screen names of users tweeting about #WeLoveTheEarth
names = [user_mention['screen_name'] for tweet in tweets for user_mention in tweet['entities']['user_mentions']]

# Extracting all the hashtags being used when talking about this topic
hashtags = [hashtag['text'] for tweet in tweets for hashtag in tweet['entities']['hashtags']]

# Inspecting the first 10 results
print (json.dumps(texts[0:10], indent=1),"\n")
print (json.dumps(names[0:10], indent=1),"\n")
print (json.dumps(hashtags[0:10], indent=1),"\n")

# Counting occcurrences/ getting frequency dist of all names and hashtags
for item in [names, hashtags]:
    c = Counter(item) 
    # Inspecting the 10 most common items in c
    print (c.most_common(10), "\n")
    
# Extracting useful information from retweets
retweets = [(tweet['retweet_count'],tweet['retweeted_status']['favorite_count'],tweet['retweeted_status']['user']['followers_count'],tweet['retweeted_status']['user']['screen_name'],tweet['text']) for tweet in tweets if 'retweeted_status' in tweet]

# Create a DataFrame and visualize the data in a pretty and insightful format
df = pd.DataFrame(retweets, columns=['Retweets','Favorites', 'Followers', 'ScreenName', 'Text']).groupby(['ScreenName','Text','Followers']).sum().sort_values(by=['Followers'],ascending=False)

df.style.background_gradient()

# Extracting language for each tweet and appending it to the list of languages
tweets_languages = []
for tweet in tweets: 
    tweets_languages.append(tweet['lang'])

# Plotting the distribution of languages
#%matplotlib inline
plt.hist(tweets_languages)