from flask import Flask
from flask_cors import CORS
from app.config import config_map
from app.extensions import init_extensions
from app.api.file_api import file_bp
from app.api.character_api import character_bp
import os


def create_app(config_name="dev"):
    """创建Flask应用实例（工厂函数）"""
    # 配置静态文件路径
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    # 加载配置
    app.config.from_object(config_map[config_name])

    # 启用CORS跨域支持
    CORS(app)

    # 初始化扩展（数据库等）
    init_extensions(app)

    # 注册蓝图（API路由）
    app.register_blueprint(file_bp)
    app.register_blueprint(character_bp)

    # 创建数据库表（首次运行自动创建）
    with app.app_context():
        from app.extensions import db
        db.create_all()

    # 首页路由
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app