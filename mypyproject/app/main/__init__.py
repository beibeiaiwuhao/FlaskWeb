from flask import Blueprint  # 蓝本

# 这个构造函数有两个必须指定的参数：蓝本的名字和蓝本所在的包或模块
main = Blueprint('main',__name__)

from . import errors,views