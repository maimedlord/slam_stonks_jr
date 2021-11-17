# api.py


from time import sleep
import pandas as pd
from pytrends.request import TrendReq
import tweepy
import nltk
from nltk.corpus import stopwords
from textblob import Word, TextBlob
import re


# Accepts a ticker dictionary that has hours per day and a corresponding value.
# These hour values are averaged for the day and returned in a dictionary.
def averager(ticker_dictionary):
    dictionary_to_return = {}  # loads nested_dictionary_return when full and empties for next ticker
    popping_from_ticker = ticker_dictionary.popitem()  # pops a tuple from into the var
    current_date = popping_from_ticker[0].strftime("%Y-%m-%d")  # string
    counter = popping_from_ticker[1]  # int
    counter_for_avg = 1
    while len(ticker_dictionary) > 0:
        popping_from_ticker = ticker_dictionary.popitem()
        temp_current_date = popping_from_ticker[0].strftime("%Y-%m-%d")
        if temp_current_date == current_date:
            counter_for_avg += 1
            counter += popping_from_ticker[1]
        if temp_current_date != current_date:
            dictionary_to_return.update({current_date: counter / counter_for_avg})
            current_date = temp_current_date
            counter = popping_from_ticker[1]
            counter_for_avg = 1
        if len(ticker_dictionary) == 0:
            dictionary_to_return.update({current_date: counter / counter_for_avg})

    return dictionary_to_return
# End of averager

# pytrends, pandas (dataframe, timeframe)
# Returns a nested dictionary containing data needed for
# comparing the relative frequency of tickers compared to each other.
# Very helpful: https://towardsdatascience.com/telling-stories-with-google-trends-using-pytrends-in-python-a11e5b8a177
def pytrend_normalized(top_10_stocks):
    # Only need to load this one time for following operations:
    pytrends = TrendReq()
    master_df = pd.DataFrame()
    counter = 1
    for x in top_10_stocks:
        if x != top_10_stocks[-1]:
            kw_list = [x, top_10_stocks[-1]]
            pytrends.build_payload(kw_list, cat=7, timeframe='now 7-d', geo='US', gprop='')
            interest_over_time_df = pytrends.interest_over_time()
            interest_over_time_df.rename(columns={top_10_stocks[-1]: top_10_stocks[-1] + str(counter)}, inplace=True)
            del interest_over_time_df['isPartial']
            master_df = pd.concat([master_df, interest_over_time_df], axis=1)
            counter += 1
            sleep(0.15)

    master_df = master_df.loc[:, ~master_df.columns.duplicated()]

    nested_dictionary = {}
    tickers_plus_normalizers_list = list(master_df.columns)
    for x in tickers_plus_normalizers_list:
        # prepping variables for the coming while loop that uses them. We need to get the current_date before we can
        # cycle through the dictionary. current_date is critical to successful execution.
        ticker_only_dictionary = master_df.to_dict().get(x)  # grabs the ticker dictionary from the dataframe
        # print(ticker_only_dictionary)
        nested_dictionary.update({x: averager(ticker_only_dictionary)})

    # averaging out normalizing ticker across .......
    average_list = [0, 0, 0, 0, 0, 0, 0, 0]
    for x in nested_dictionary:
        for_loop_counter = 0

        if x[-1].isdigit():
            for xx in nested_dictionary[x]:
                average_list[for_loop_counter] += nested_dictionary[x][xx]
                for_loop_counter += 1

    weird_list = []     # cuz bug hunting, that's why! (the name, not the function)

    for x in average_list:  # average the results
        weird_list.append(x / 8.0)

    for_loop_counter = 0
    for x in nested_dictionary[tickers_plus_normalizers_list[1]]:
        nested_dictionary[tickers_plus_normalizers_list[1]][x] = weird_list[for_loop_counter]
        for_loop_counter += 1

    for_loop_counter = 0
    for x in tickers_plus_normalizers_list:
        if for_loop_counter == 0 or for_loop_counter == 1 or x == top_10_stocks[-1]:
            for xx in nested_dictionary[x]:
                nested_dictionary[x][xx] = round(nested_dictionary[x][xx], 2)
        elif for_loop_counter % 2 == 0:
            for xx in nested_dictionary[x]:
                nested_dictionary[x][xx] = round(nested_dictionary[x][xx], 2)

        for_loop_counter += 1

    # change normalized value so that it no longer has a trailing digit: ('1')
    nested_dictionary[tickers_plus_normalizers_list[1][:-1]] = nested_dictionary.pop(tickers_plus_normalizers_list[1])

    # remove relational values for normalization:
    for_loop_counter = 2
    while for_loop_counter < 10:
        del nested_dictionary[top_10_stocks[-1] + str(for_loop_counter)]
        for_loop_counter += 1

    return nested_dictionary
# END google_trends_normalized

# pytrends, pandas
# This does what normalized does but for one ticker only.
def pytrend_single(ticker):
    # Only need to load this one time for following operations:
    pytrends = TrendReq()

    kw_list = [ticker]
    pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='US', gprop='')
    interest_over_time_df = pytrends.interest_over_time()

    # prepping variables for the coming while loop that uses them.
    # We need to get the current_date before we can cycle through the dictionary.
    # current_date is critical to successful execution.
    ticker_only_dictionary = interest_over_time_df.to_dict().get(ticker)
    # grabs the ticker dictionary from the dataframe
    # print(interest_over_time_df.to_string())
    return averager(ticker_only_dictionary)
# END pytrend_single

# TWITTER()
# tweepy, pandas, re, nltk, textblob
# Gathers tweets for a ticker and then performs sentiment analysis on the tweets with nltk and textblob.
# Data is returned in a dictionary.
def twitter(ticker):
    # login stuff:
    consumer_key = 'Dvkp7foIvb2EMqxFoXCqcD4YZ'
    consumer_secret = 'gs0w56HCcSwuWJEyVKXL0ywv9ibE1R98ZomPUyDSbtl7kDy4sv'
    access_token = '1371241350746755074-zbpTUM7DqzTxie9tJ5VOvbVYSZ1CAI'
    access_token_secret = '9EazuwZG4XEnBR5eInRBqE1BzpEV72iJLoF8OzGzZBBnT'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # error checking
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication\n\n\n")

    # Pre-loop prep (keep preprocess_tweets below stop_words:
    nltk.download('stopwords')
    nltk.download('wordnet')
    stop_words = stopwords.words('english')

    # Removes stop words from each tweet as well as lemmatizing the words too
    # this function must sit below stop_words
    def preprocess_tweets(tweet, custom_stop_words):
        preprocessed_tweet = tweet
        preprocessed_tweet = re.sub('#\w+:?', '', preprocessed_tweet)
        preprocessed_tweet = re.sub('@\w+:?', '', preprocessed_tweet)
        preprocessed_tweet = re.sub('https?://[\w:\.\$\/_-]+', '', preprocessed_tweet)
        preprocessed_tweet.replace('[^\w\s]', '')
        preprocessed_tweet = " ".join(word for word in preprocessed_tweet.split() if word not in stop_words)
        preprocessed_tweet = " ".join(word for word in preprocessed_tweet.split() if word not in custom_stop_words)
        preprocessed_tweet = " ".join(Word(word).lemmatize() for word in preprocessed_tweet.split())
        return preprocessed_tweet

    custom_stopwords = ['RT']  # add to if necessary
    query = tweepy.Cursor(api.search_tweets,
                          q=ticker,
                          lang="en", ).items(200)  # removed since...
    tweets = [{'Tweets': tweet.text, 'Timestamp': tweet.created_at} for tweet in query]
    df = pd.DataFrame.from_dict(tweets)
    df['Processed Tweet'] = df['Tweets'].apply(lambda x: preprocess_tweets(x, custom_stopwords))

    # calculate sentiment
    df['polarity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[0])
    df['subjectivity'] = df['Processed Tweet'].apply(lambda x: TextBlob(x).sentiment[1])
    df.drop(df.columns[[0, 1, 2]], axis=1, inplace=True)
    ticker_dict = {ticker: [df['polarity'].mean(), df['subjectivity'].mean()]}

    return ticker_dict
# END twitter
