from flask_sqlalchemy import SQLAlchemy

# 初始化SQLAlchemy（ORM工具，替代原生pymysql）
db = SQLAlchemy()

def init_extensions(app):
    """初始化所有扩展"""
    db.init_app(app)