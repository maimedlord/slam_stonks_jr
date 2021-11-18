# Alex Haas


from pymongo import MongoClient, DESCENDING
import datetime
from scraper import scrape_marketwatch
from api import pytrend_single, pytrend_normalized, twitter


database_name = "ssjr"

def get_pytrend_normalized():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["pytrend_normalized"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    temp_object = mongodb_obj.get("pytrend_normalized")
    return temp_object

def get_top10():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    return mongodb_obj.get("top10array")

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
        db_collection.replace_one({"_id": temp_id}, temp_obj, upsert=True)

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

def store_pytrend_normalized():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    top10_array = mongodb_obj.get("top10array")
    db_collection = db["pytrend_normalized"]
    now_date = datetime.datetime.today().replace(microsecond=0)
    temp_obj = pytrend_normalized(top10_array)
    db_collection.insert_one({"date": now_date, "pytrend_normalized": temp_obj})

# NOT COMPLETE #########################################################################################################
def store_twitter():
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    mongodb_obj = db_collection.find_one(sort=[('_id', DESCENDING)])
    top10_array = mongodb_obj.get("top10array")
    for x in top10_array: ##############################################################################################
        print(twitter(x))

if __name__ == '__main__':
    # store_stocks()
    # store_pytrend()
    # store_pytrend_normalized()
    # store_twitter()
    get_pytrend_normalized()
    pass