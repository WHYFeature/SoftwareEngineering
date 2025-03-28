# 将数据库操作对象db独立出来，便于封装SQL模型
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()