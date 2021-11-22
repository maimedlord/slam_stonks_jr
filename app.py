from flask import Flask, render_template
from dbi import get_top10, get_pytrend_normalized, get_stock, get_yfhistdf


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
    short_interest = stock_obj["short_interest"]
    float_shorted = stock_obj["float_shorted"]
    dates = list(stock_obj["pytrend"].keys())[::-1]
    values = list(stock_obj["pytrend"].values())[::-1]
    # stock info:
    stock_obj = get_yfhistdf(ticker)
    yf_dates_array = stock_obj["Date"]
    yf_high_array = stock_obj["High"]
    yf_low_array = stock_obj["Low"]
    yf_open_array = stock_obj["Open"]
    yf_close_array = stock_obj["Close"]
    yf_volume_array = stock_obj["Volume"]
    return render_template('ticker.html', top10_array=top10_array, ticker=ticker, name=name, price=price, short_interest=short_interest, float_shorted=float_shorted, dates=dates, values=values, yf_dates_array=yf_dates_array, yf_high_array=yf_high_array, yf_low_array=yf_low_array, yf_open_array=yf_open_array, yf_close_array=yf_close_array, yf_volume_array=yf_volume_array)


if __name__ == '__main__':
    app.run(debug=True)
