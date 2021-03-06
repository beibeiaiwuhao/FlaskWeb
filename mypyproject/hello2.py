from flask import Flask,render_template


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name,comments=(1,2,3,4,5,10,6,7))

if __name__ == "__main__":
    app.run()
