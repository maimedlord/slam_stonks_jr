from requests import get                # pulls html
from re import search                   # regular expressions


# returns dictionary with 0-9 as keys and a list [ticker, name, price, short interest, and float shorted for the values.
def scrape_marketwatch():
    # requests will use .get() to pull from marketwatch.com
    requests_get_short_html = get('http://www.marketwatch.com/tools/screener/short-interest')
    # r.raise_for_status() # will return error if http isn't up

    newline_delimited = requests_get_short_html.text.split('\n')
    top_10_stocks = {}

    # the content we want starts a bit after line 675:
    i = 675
    counter = 0
    while i < len(newline_delimited) and counter < 10:
        none_or_match = search("<div class=\"cell__content\">[A-Z]{3,5}</div>", newline_delimited[i])

        if none_or_match is not None:
            one_stock_list = []
            # grabs ticker:
            temp_string = search(".*>(.*)<.*", none_or_match.group(0))  # pulls substring from match object
            one_stock_list.append(temp_string.group(1))
            # grabs company name
            i += 3
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            one_stock_list.append(temp_string.group(1))
            # grabs price:
            i += 3
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            one_stock_list.append(temp_string.group(1))
            # grabs short interest
            i += 8
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            one_stock_list.append(temp_string.group(1))
            # grabs float shorted
            i += 9
            temp_string = search(".*>(.*)<.*", newline_delimited[i])
            one_stock_list.append(temp_string.group(1))

            top_10_stocks.update({counter: one_stock_list})
            counter += 1
            # end if

        i += 1
        # end while

    return top_10_stocks
# END scraper
