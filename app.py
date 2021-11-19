from flask import Flask, render_template
from dbi import get_top10, get_pytrend_normalized


app = Flask(__name__)


@app.route('/')
def index():
    top10_array = get_top10()
    pnorm_obj = get_pytrend_normalized()
    tickers = list(pnorm_obj.keys())[::-1]
    dates = list(pnorm_obj.get(tickers[0]).keys())[::-1] #  BE CAREFUL OF DESCENDING/ASCENDING DATES NOT MATHCING THEIR VALUES
    return render_template('index.html', top10_array=top10_array, pnorm_obj=pnorm_obj, tickers=tickers, dates=dates)


@app.route('/<string: ticker>')
def ticker():
    return render_template('ticker.html')


if __name__ == '__main__':
    app.run(debug=True)
