import os
from flask import Flask,url_for,redirect,render_template,session
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_script import Manager
from threading import Thread

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['FLASKY_MAIL_SUJECT_PREFIX'] = '[Flasky]'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SENDER'] = os.environ.get('MAIL_USERNAME')
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)
manager = Manager(app)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User', backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>'%self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

# 异步发送电子邮件
def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUJECT_PREFIX']+' '+ subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)
    thr = Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr


# 同步发送电子邮件，会有延迟
# def send_email(to,subject,template,**kwargs):
#     msg = Message(app.config['FLASKY_MAIL_SUJECT_PREFIX']+' '+ subject,sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
#     msg.body = render_template(template + '.txt',**kwargs)
#     msg.html = render_template(template + '.html',**kwargs)
#     mail.send(msg)



class NameForm(FlaskForm):
    name = StringField('你的名字是?',validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('400.html'),404

@app.errorhandler(500)
def internal_server_template(e):
    return render_template('500.html'),500


@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user_role = Role(name=form.name.data)
            user = User(username=form.name.data, role=user_role)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            print(app.config['FLASKY_ADMIN'])
            print(app.config['MAIL_USERNAME'])
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index2.html',form=form,name=session.get('name'),known=session.get('known',False))





if __name__ == '__main__':
    app.run()







