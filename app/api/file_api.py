from flask import Blueprint, jsonify, request
from app.models.file import FileEntity
from app.extensions import db

# 创建蓝图（模块化路由）
file_bp = Blueprint("file", __name__, url_prefix="/api/file")


@file_bp.route("/list", methods=["GET"])
def get_file_list():
    """获取所有文件数据"""
    files = FileEntity.query.all()
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": [f.to_dict() for f in files]
    })


@file_bp.route("/detail/<string:identifier>", methods=["GET"])
def get_file_detail(identifier):
    """根据唯一标识获取文件详情"""
    file = FileEntity.query.filter_by(identifier=identifier).first()
    if not file:
        return jsonify({"code": 404, "msg": "文件不存在"}), 404
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": file.to_dict()
    })


@file_bp.route("/add", methods=["POST"])
def add_file():
    """新增文件数据（接收JSON）"""
    data = request.get_json()
    if not data or not data.get("identifier"):
        return jsonify({"code": 400, "msg": "缺少必填参数"}), 400

    # 检查是否已存在
    if FileEntity.query.filter_by(identifier=data["identifier"]).first():
        return jsonify({"code": 409, "msg": "文件已存在"}), 409

    # 创建文件记录
    new_file = FileEntity(
        identifier=data["identifier"],
        entity_type=data.get("entity_type"),
        file_name=data.get("file_name"),
        file_key=data.get("file_key"),
        file_size=data.get("file_size"),
        file_type=data.get("file_type"),
        file_name_state=data.get("file_name_state"),
        file_parse_state=data.get("file_parse_state")
    )
    db.session.add(new_file)
    db.session.commit()

    return jsonify({"code": 201, "msg": "新增成功", "data": new_file.to_dict()}), 201