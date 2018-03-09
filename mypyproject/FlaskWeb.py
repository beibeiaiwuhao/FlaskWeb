import os
from flask_migrate import Migrate,MigrateCommand
from app import create_app,db
from app.models import User,Role
from flask_script import Manager,Shell


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app,db)
manager = Manager(app)


def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)


manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)


# 单元测试
# @manager.command
# def test():
#     import unittest
#     tests = unittest.TestLoader().discover('test')
#     unittest.TextTestRunner(verbosity=2).run(tests)
#


if __name__ == '__main__':
    app.run()




