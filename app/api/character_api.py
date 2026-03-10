from flask import Blueprint, jsonify, request
from app.models.character import GenshinCharacter, GenshinCharacterRank, SystemInfo, GenshinTeam
from app.extensions import db

character_bp = Blueprint("character", __name__, url_prefix="/api/character")

# 获取系统信息并增加访问量
@character_bp.route("/system_info", methods=["GET"])
def get_system_info():
    """获取系统信息并增加访问量"""
    info = SystemInfo.query.first()
    if not info:
        return jsonify({"code": 404, "msg": "系统信息未配置"}), 404
    
    # 增加访问量
    info.visit_count = (info.visit_count or 0) + 1
    db.session.commit()
    
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": info.to_dict()
    })

# 获取角色列表（支持按星级筛选）
@character_bp.route("/list", methods=["GET"])
def get_character_list():
    """获取角色列表（支持按星级筛选）"""
    star = request.args.get("star")
    query = GenshinCharacter.query
    if star:
        query = query.filter_by(star=star)
    characters = query.all()
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": [c.to_dict() for c in characters]
    })

# 根据名称获取角色详情
@character_bp.route("/detail/<string:name>", methods=["GET"])
def get_character_detail(name):
    """根据名称获取角色详情"""
    character = GenshinCharacter.query.filter_by(name=name).first()
    if not character:
        return jsonify({"code": 404, "msg": "角色不存在"}), 404
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": character.to_dict()
    })

# 获取所有角色评级数据
@character_bp.route("/ranks", methods=["GET"])
def get_character_ranks():
    """获取所有角色评级数据"""
    name = request.args.get("name")
    rank_name = request.args.get("rank_name")
    
    query = GenshinCharacterRank.query
    if name:
        query = query.filter_by(name=name)
    if rank_name:
        query = query.filter_by(rank_name=rank_name)
    
    ranks = query.all()
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": [r.to_dict() for r in ranks]
    })

# 获取热门队伍列表（按使用率降序）
@character_bp.route("/teams", methods=["GET"])
def get_teams():
    """获取热门队伍列表（按使用率降序）"""
    limit = request.args.get("limit", 50, type=int)
    
    teams = GenshinTeam.query.order_by(GenshinTeam.use_rate.desc()).limit(limit).all()
    return jsonify({
        "code": 200,
        "msg": "success",
        "data": [t.to_dict() for t in teams]
    })