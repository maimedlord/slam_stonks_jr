from requests import get                # pulls html
from re import search                   # regular expressions
import datetime


# returns dictionary with 0-9 as keys and a list [ticker, name, price, short interest, and float shorted for the values.
def scrape_marketwatch():
    # used to sync dates for individual tickers and the list of tickers
    now_date = datetime.datetime.today().replace(microsecond=0)
    # pull data from marketwatch
    requests_get_short_html = get('http://www.marketwatch.com/tools/screener/short-interest')

    newline_delimited = requests_get_short_html.text.split('\n')
    top10_list = []
    top10_obj_list = []
    i = 675     # the content we want starts a bit after line 675
    counter = 0
    while i < len(newline_delimited) and counter < 10:
        none_or_match = search("<div class=\"cell__content\">[A-Z]{3,5}</div>", newline_delimited[i])
        if none_or_match is not None:
            # grabs ticker:
            temp_string = search(".*>(.*)<.*", none_or_match.group(0))  # pulls substring from match object
            top10_list.append(temp_string.group(1))
            ticker = temp_string.group(1)
            # grabs company name
            i += 3
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            name = temp_string.group(1)
            # grabs price:
            i += 3
            temp_string = search(".*>\$(.*)<.*", newline_delimited[i])
            price = temp_string.group(1)
            # grabs short interest
            i += 8
            temp_string = search(".*>([^,].*)<.*", newline_delimited[i])
            short_interest = temp_string.group(1)
            # grabs float shorted
            i += 9
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            float_shorted = temp_string.group(1)

            top10_obj_list.append({
                ticker: {
                    "_id": ticker,
                    "date": now_date,
                    "name": name,
                    "price": float(price),
                    "short_interest": short_interest,
                    "float_shorted": float_shorted,
                    "pytrend": {}
                }
            })
            counter += 1
            # end if

        i += 1
        # end while

    return {"date": now_date, "top10array": top10_list}, top10_obj_list
# END scraper
