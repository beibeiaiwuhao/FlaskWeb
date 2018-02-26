from flask import Flask,render_template

from flask_moment import Moment
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)


moment = Moment(app)
bootstrap = Bootstrap(app)

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            current_time=datetime.utcnow())

@app.route('/')
def index():
    return render_template('index.html',
                           current_time=datetime.utcnow())


if __name__ == "__main__":
    app.run(debug=True)