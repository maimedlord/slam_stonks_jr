# Alex Haas


from pymongo import MongoClient, DESCENDING
import datetime
from scraper import scrape_marketwatch
from api import pytrends_normalized


database_name = "ssjr"


def store_scrape_marketwatch():
    temp_storage = scrape_marketwatch()
    db_client = MongoClient()
    db = db_client[database_name]
    db_collection = db["top10"]
    db_collection.insert_one(temp_storage[0])
    db_collection = db["scrape_marketwatch"]
    db_collection.insert_many(temp_storage[1])


# # LEFT OFF HERE
# def store_pytrends():
#     # first, grab data:
#     db_client = MongoClient()
#     db = db_client[database_name]
#     mw_data_collection = db["scrape_marketwatch"]
#     mw_dict = mw_data_collection.find_one(sort=[('_id', DESCENDING)])
#     mw_dict.pop('_id')
#
#     # second, get data prepped:
#     top10 = []
#     counter = 0
#     while counter < 10:
#         temp_list = mw_dict[str(counter)]
#         top10.append(temp_list[0])
#         counter += 1
#
#     print(top10)




if __name__ == '__main__':
    store_scrape_marketwatch()