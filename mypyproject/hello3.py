
from flask import Flask,render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

@app.route('/bootstrap/<name>')
def bootstrapIndex(name):
    return render_template('bootstrapUser.html',name=name)

@app.route('/')
def index():
    return render_template('index1.html')




bootstap = Bootstrap(app)

if __name__ == "__main__":
    app.run(debug=True)

