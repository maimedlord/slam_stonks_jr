# Alex Haas


from pymongo import MongoClient
import scraper


database_name = "ssjr"


def store_scrape_marketwatch():
    top10 = scraper.scrape_marketwatch()
    db_client = MongoClient()
    db = db_client["scrape_marketwatch"]
    db_collection = db[]
    print(top10.keys())


if __name__ == '__main__':
    store_scrape_marketwatch()