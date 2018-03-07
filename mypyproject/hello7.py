
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,session,redirect,url_for,render_template
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
# from flask.ext.script import Shell
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
# 配置数据库

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


class NameForm(FlaskForm):
    name = StringField("What's your name",validators=[DataRequired()])
    submit = SubmitField("Submit")

#db.Column 类构造函数的第一个参数是数据库列和模型属性的类型

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64),unique=True)

    users = db.relationship('User',backref='role')

    def __repr__(self):
        return '<Role %r>'%self.name



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User> %r'%self.username


@app.shell_context_processor
def make_shell_context():
    return dict(db=db,User=User,Role=Role)





@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        print(form.name.data)
        user = User.query.filter_by(username=form.name.data).first()

        if user is None:
            user_role = Role(name=form.name.data)
            user = User(username=form.name.data,role=user_role)
            db.session.add(user)
            db.session.commit()
            print(user.username)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index2.html',form=form,name=session.get('name'),known=session.get('known',False))



if __name__ == '__main__':
    manager.run()


