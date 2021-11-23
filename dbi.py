# Alex Haas



import datetime
from time import sleep
from pymongo import MongoClient, DESCENDING
import tweepy
import yfinance as yf
from scraper import scrape_marketwatch
from api import api_loop, pytrend_single, pytrend_normalized, twitter


database_name = "ssjr"

def date_now():
    return datetime.datetime.today().replace(microsecond=0)

def do_api_loop():
    api_loop()

def get_pytrend_normalized():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["pytrend_normalized"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    pnorm_obj = mongodb_obj.get("pytrend_normalized")
    return pnorm_obj

def get_stock(ticker):
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["stocks"]
    stock_obj = db_collection.find_one({'_id': ticker})
    return(stock_obj)

def get_top10():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    return mongodb_obj.get("top10array")

def get_yfhistdf(ticker):
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["stocks"]
    mongodb_obj = db_collection.find_one({'_id': ticker})
    stock_info_obj = mongodb_obj.get("yf_hist_dataframe")
    return stock_info_obj

def store_yfhistdf():
    top10_array = get_top10()
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["stocks"]
    for ticker in top10_array:
        yf_obj = yf.Ticker(ticker)
        history = yf_obj.history(period="1y")
        history.reset_index(inplace=True)       #.reset_index(inplace=True) # includes Reset Index for Pandas DF
        history = history.to_dict("list")
        db_collection.update_one({"_id": ticker}, {"$set": {"yf_hist_dataframe": history}})
        sleep(1)

def store_stocks():
    temp_storage = scrape_marketwatch()
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    db_collection.insert_one(temp_storage[0])
    db_collection = db["stocks"]
    for x in temp_storage[1]:
        temp_id = str(list(x.keys())[0])
        temp_obj = dict(list(x.values())[0])
        #print(temp_obj)
        #db_collection.replace_one({"_id": temp_id}, temp_obj, upsert=True)
        db_collection.update_one({"_id": temp_obj["_id"]}, {"$set": {"date": temp_obj["date"], "name": temp_obj["name"], "price": temp_obj["price"], "short_interest": temp_obj["short_interest"], "float_shorted": temp_obj["float_shorted"]}}, upsert=True)

def store_pytrend():
    list_of_dicts = {}
    # pull tickers from db:
    # db_client = MongoClient()
    # db = db_client[database_name]
    # db_collection = db["top10"]
    # mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    top10_array = get_top10()
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["stocks"]
    for x in top10_array:
        pytrend_dict = pytrend_single(x)
        db_collection.update_one({"_id": x}, {"$set": {"pytrend": pytrend_dict}})

def store_pytrend_normalized(now_date):
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    top10_array = mongodb_obj.get("top10array")
    db_collection = db["pytrend_normalized"]
    temp_obj = pytrend_normalized(top10_array)
    db_collection.insert_one({"date": now_date, "pytrend_normalized": temp_obj})

# NOT COMPLETE #########################################################################################################
def store_twitter(date_rn):
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    top10_array = mongodb_obj.get("top10array")
    db_collection = db["stocks"]
    temp_tuple = ()
    for x in top10_array:
        temp_tuple = twitter(x)
        db_collection.update_one({'_id': x}, {"$push": {"twitter_sentiment.date": date_rn, "twitter_sentiment.polarity": temp_tuple[0], "twitter_sentiment.subjectivity": temp_tuple[1]}}, upsert=True)
        print(str(temp_tuple[0]) + " yo " + str(temp_tuple[1]))
        sleep(30)


if __name__ == '__main__':
    date_rn = date_now()
    do_api_loop()
    store_stocks()
    store_pytrend()
    store_pytrend_normalized(date_rn)
    #get_pytrend_normalized()
    #get_stock("CRTX")
    store_yfhistdf()
    store_twitter(date_rn)
    #get_yfhistdf("CRTX")
    #sleep(14400)