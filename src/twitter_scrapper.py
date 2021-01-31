from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import pandas as pd
import os
import time

# Authenticating Twitter API
# Obtain your Twitter credentials from your twitter developer account

consumer_key = 'Your API Key'
consumer_secret = 'Your API Seceret Key'
access_key = 'Access Token Key'
access_secret = 'Access Token Seceret Key'

# Pass your twitter credentials to tweepy via its OAuthHandler

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

## Automating Scraping
# Calls API every 15 minutes to prevent overcalling


def scraptweets(search_words, date_since, numTweets, numRuns):

    # Define a pandas dataframe to store the date:
    db_tweets = pd.DataFrame(columns = ['username', 'acctdesc', 'location', 'following',
                                        'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                        'retweetcount', 'text', 'hashtags']
                                )
    # Define a for-loop to generate tweets at regular intervals
    for i in range(0, numRuns):
        # We will time how long it takes to scrape tweets for each run:
        start_run = time.time()
        
        # Collect tweets using the Cursor object
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode='extended').items(numTweets)

        # Store these tweets into a python list
        tweet_list = [tweet for tweet in tweets]


        # Begin scraping the tweets individually:
        noTweets = 0

        for tweet in tweet_list:

            # Pull the values
            username = tweet.user.screen_name
            acctdesc = tweet.user.description
            location = tweet.user.location
            following = tweet.user.friends_count
            followers = tweet.user.followers_count
            totaltweets = tweet.user.statuses_count
            usercreatedts = tweet.user.created_at
            tweetcreatedts = tweet.created_at
            retweetcount = tweet.retweet_count
            hashtags = tweet.entities['hashtags']

            try:
                text = tweet.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                text = tweet.full_text

            # Add the 11 variables to the empty list - ith_tweet:
            ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                         usercreatedts, tweetcreatedts, retweetcount, text, hashtags]

            # Append to dataframe - db_tweets
            db_tweets.loc[len(db_tweets)] = ith_tweet

            # increase counter - noTweets  
            noTweets += 1
        
        # Run ended:
        end_run = time.time()
        duration_run = round(end_run-start_run, 2)
        
        print('no. of tweets scraped for run {} is {}'.format(i, noTweets))
        print('time take for {} run to complete is {}'.format(i, duration_run))
        
        time.sleep(900) #15 minute sleep time

        
    # Once all runs have completed, save them to a single csv file:    
    # Obtain timestamp in a readable format:
    from datetime import datetime
    to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')

    # Define working path and filename
    path = os.getcwd()
    filename = path + '/data/' + to_csv_timestamp + '_covid_tweets.csv'

    # Store dataframe in csv with creation date timestamp
    db_tweets.to_csv(filename, index = False)
    
    print('Scraping has completed!')
# Initialise these variables:
search_words = "#COVID or #covid"
date_since = "2021-01-15"
numTweets = 2500
numRuns = 6
# Call the function scraptweets
scraptweets(search_words, date_since, numTweets, numRuns)