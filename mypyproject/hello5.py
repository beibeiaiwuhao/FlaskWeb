from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_bootstrap import Bootstrap
from flask import Flask,render_template,session,redirect,url_for
from wtforms.validators import DataRequired
from flask_moment import Moment


class NameForm(FlaskForm):
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
        # name = form.name.data
        # form.name.data = ''
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index1.html',form=form,name=session.get('name'))


if __name__ == "__main__":
    app.run(debug=True)


