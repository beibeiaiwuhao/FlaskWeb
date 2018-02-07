from flask import Flask
from  flask import make_response,redirect,abort
from flask.ext.script import Manager

app = Flask(__name__)

# @app.route("/user/<name>")
# def user(name):
#     return "<h1>Hello %s </h1>"%name

@app.route("/")
def index():
    # response = make_response("<h1>This document carries a cookie !</h1>")
    # response.set_cookie('answer',42)
    # return response
    return redirect("http://www.baidu.com")

@app.route("/user/<id>")
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return "<h1>Hello %s</h1>"%user


def load_user(id):
    return "wuhao"



manager = Manager(app)

if __name__ == "__main__":
    manager.run()



# if __name__ == "__main__":
#     app.run(debug=True)



