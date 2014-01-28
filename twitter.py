from twython import Twython, TwythonError
import string 

# This is my search term in twitter

query = "elonmusk"


# Obtain the consumer key and consumer secret from https://dev.twitter.com/apps 
# and register for an application

APP_KEY = 'jYTi5z6873q4t9g9RB3r9Q'
APP_SECRET = 'PgzA3ntCtdd0wH6BQ3qqZMjMUkAlXn1A8sn2TKoU4'

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens()


# Define a function called search(query), which takes in a query term
# Abstract the twitter search into a function
# Search(query) returns a list of tweets

def search(query):
    tweet_list = []
    try:
        search_results = twitter.search(q=query)
    except TwythonError as e:
        print e

    for tweet in search_results['statuses']:
        tweet_list.append(tweet['text'].encode('utf-8'))
    return tweet_list

# Define a function called read_score(sfile), which takes in the name of a file
# contains a list of sentiment scores
# Each line in the file contains a word or phrase followed by a score
# read_scores returns a dictionary of key-value pairs where key is the sentiment
# word and key is the sentiment score

def read_scores(sfile):
    score_dict={}
    open_file = open(sfile,'r')
    for line in open_file:
        line = line.strip()
        word, score = line.split('\t',1)
        score_dict[word]=int(score)
        # print word, score
    return score_dict


# This is the file which contains sentiment word and score
afinn = read_scores('AFINN-111.txt')


# Define a function called sentiment(str), which takes in a string
# sentiment(str) returns the total sentiment score of the string

def sentiment(s,sentiment_score=afinn):
    tot_score = 0
    for c in string.punctuation:
        s = s.replace(c,"")
    for word in s.split():
        if word.lower() in sentiment_score.keys():
            print word, sentiment_score[word.lower()]
            tot_score += sentiment_score[word.lower()]
    return tot_score


# Define a function called total_sentiment, which takes a list of tweets
# total_sentiment(lst) returns the total sentiment score of all tweets in the list

def total_sentiment(lst):
    score = 0    
    for str in lst:
        score += sentiment(str)
    return score

# Return a list of tweets using a query term

tweets_list = search(query)


# Print the item in tweets_list

for t in tweets_list:
    print t

# Check the maximum length of any tweet in the query, it should typically be less than 143

#tweet_lengths = [len(tweet) for tweet in search(query)]
#print max(tweet_lengths)

# Test: calculate the total sentiment of a twitter search query
tot = total_sentiment(tweets_list)
print "Total sentiment of %s is: %s" % (query, tot)
