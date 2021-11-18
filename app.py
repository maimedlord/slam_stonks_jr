from flask import Flask, render_template
from dbi import get_top10, get_pytrend_normalized


app = Flask(__name__)


@app.route('/')
def index():
    top10_array = get_top10()
    pytrend_norm_obj = get_pytrend_normalized()

    return render_template('index.html', top10_array=top10_array, pytrend_norm_obj=pytrend_norm_obj)


if __name__ == '__main__':
    app.run(debug=True)
