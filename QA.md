# QA文件

Q1：这个文件有用吗

A1：没用


Q2：config.py内容

A2：如下

```python
# 主机名
HOSTNAME = "127.0.0.1"
# 监听端口
PORT = 3306
# 链接sql用户名和密码
USERNAME = "%YOUNAME%"
PASSWORD = "%YOUPASSWORD%"
# 数据库名
DATEBASE = "bookshop"
# 链接
DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4".format(
    USERNAME, PASSWORD, HOSTNAME, PORT, DATEBASE)
SQLALCHEMY_DATABASE_URI = DB_URI
```
