from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask import Flask,render_template

from wtforms.validators import DataRequired
from flask_moment import Moment


class NameForm(Form):
    name = StringField("What's your name",validators=[Required()])
    submit = SubmitField("Submit")

app = Flask(__name__)
boostrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index1.html',form=form,name=name)


if __name__ == "__main__":
    app.run(debug=True)


