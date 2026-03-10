import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """基础配置"""
    # Flask 核心配置
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_123")
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # MySQL 数据库配置（与 json_to_sql.py 保持一致）
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
    MYSQL_DB = os.getenv("MYSQL_DB", "yuanshen_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    
    # SQLAlchemy 数据库配置（使用上面的变量构建）
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # JSON 数据文件路径（整合后的路径）
    JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "purified_character_data.json")


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


config_map = {
    "dev": DevelopmentConfig,
    "prod": ProductionConfig
}