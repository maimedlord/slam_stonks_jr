from flask import Flask, render_template
from dbi import get_top10, get_pytrend_normalized, get_stock


app = Flask(__name__)


@app.route('/')
def index():
    top10_array = get_top10()
    pnorm_obj = get_pytrend_normalized()
    tickers = list(pnorm_obj.keys())[::-1]
    dates = list(pnorm_obj.get(tickers[0]).keys())[::-1] #  BE CAREFUL OF DESCENDING/ASCENDING DATES NOT MATHCING THEIR VALUES
    return render_template('index.html', top10_array=top10_array, pnorm_obj=pnorm_obj, tickers=tickers, dates=dates)


@app.route('/<string:ticker>')
def ticker_page(ticker):
    top10_array = get_top10()
    stock_obj = get_stock(ticker)
    name = stock_obj["name"]
    price = stock_obj["price"]
    short_interest =  stock_obj["short_interest"]
    float_shorted =  stock_obj["float_shorted"]
    dates = list(stock_obj["pytrend"].keys())[::-1]
    values = list(stock_obj["pytrend"].values())[::-1]
    return render_template('ticker.html', top10_array=top10_array, ticker=ticker, name=name, price=price, short_interest=short_interest, float_shorted=float_shorted, dates=dates, values=values)


if __name__ == '__main__':
    app.run(debug=True)
