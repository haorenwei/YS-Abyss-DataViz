from app.extensions import db


class SystemInfo(db.Model):
    """系统配置信息模型"""
    __tablename__ = "system_info"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), comment="标题")
    version = db.Column(db.String(50), comment="版本信息")
    now_version = db.Column(db.String(50), comment="本期版本")
    old_version = db.Column(db.String(50), comment="上期版本")
    last_update = db.Column(db.String(20), comment="最后更新时间")
    update_info = db.Column(db.String(100), comment="更新信息")
    top_own = db.Column(db.Integer, comment="有效样本数")
    tips = db.Column(db.Text, comment="数据总结")
    tips2 = db.Column(db.Text, comment="使用提示")
    star36_rate = db.Column(db.String(10), comment="36星通关率")
    visit_count = db.Column(db.Integer, default=0, comment="访问量")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "version": self.version,
            "now_version": self.now_version,
            "old_version": self.old_version,
            "last_update": self.last_update,
            "update_info": self.update_info,
            "top_own": self.top_own,
            "tips": self.tips,
            "tips2": self.tips2,
            "star36_rate": self.star36_rate,
            "visit_count": self.visit_count
        }


class GenshinCharacter(db.Model):
    """原神角色数据模型（对应之前的MySQL表）"""
    __tablename__ = "genshin_characters"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False, comment="角色名称")
    ename = db.Column(db.String(50), comment="英文名称")
    star = db.Column(db.SmallInteger, nullable=False, comment="星级（4/5）")
    avatar = db.Column(db.String(255), comment="头像URL")
    use_count = db.Column(db.Integer, comment="使用次数")
    own_count = db.Column(db.Integer, comment="持有次数")
    use_rate = db.Column(db.Numeric(5, 1), comment="使用率（%）")
    own_rate = db.Column(db.Numeric(5, 1), comment="持有率（%）")
    collection = db.Column(db.Numeric(3, 1), comment="收藏值")
    rank_class = db.Column(db.String(5), comment="评级类别（s1/s/a/b/f）")
    use_rate_old = db.Column(db.Numeric(5, 1), comment="历史使用率")
    use_rate_change = db.Column(db.Numeric(5, 1), comment="使用率变化")

    def to_dict(self):
        """模型转字典"""
        return {
            "id": self.id,
            "name": self.name,
            "ename": self.ename,
            "star": self.star,
            "avatar": self.avatar,
            "use_count": self.use_count,
            "own_count": self.own_count,
            "use_rate": float(self.use_rate) if self.use_rate else None,
            "own_rate": float(self.own_rate) if self.own_rate else None,
            "collection": float(self.collection) if self.collection else None,
            "rank_class": self.rank_class,
            "use_rate_old": float(self.use_rate_old) if self.use_rate_old else None,
            "use_rate_change": float(self.use_rate_change) if self.use_rate_change else None
        }


class GenshinCharacterRank(db.Model):
    """原神角色评级详情模型（含命之座数据）"""
    __tablename__ = "genshin_character_ranks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), db.ForeignKey('genshin_characters.name'), nullable=False, comment="角色名称")
    rank_name = db.Column(db.String(10), nullable=False, comment="评级名称（S+/S/A/B/C）")
    c0_rate = db.Column(db.Numeric(5, 1), comment="0命持有率（%）")
    c1_rate = db.Column(db.Numeric(5, 1), comment="1命持有率（%）")
    c2_rate = db.Column(db.Numeric(5, 1), comment="2命持有率（%）")
    c3_rate = db.Column(db.Numeric(5, 1), comment="3命持有率（%）")
    c4_rate = db.Column(db.Numeric(5, 1), comment="4命持有率（%）")
    c5_rate = db.Column(db.Numeric(5, 1), comment="5命持有率（%）")
    c6_rate = db.Column(db.Numeric(5, 1), comment="6命持有率（%）")
    time = db.Column(db.Integer, comment="时间字段")

    def to_dict(self):
        """模型转字典"""
        return {
            "id": self.id,
            "name": self.name,
            "rank_name": self.rank_name,
            "c0_rate": float(self.c0_rate) if self.c0_rate else None,
            "c1_rate": float(self.c1_rate) if self.c1_rate else None,
            "c2_rate": float(self.c2_rate) if self.c2_rate else None,
            "c3_rate": float(self.c3_rate) if self.c3_rate else None,
            "c4_rate": float(self.c4_rate) if self.c4_rate else None,
            "c5_rate": float(self.c5_rate) if self.c5_rate else None,
            "c6_rate": float(self.c6_rate) if self.c6_rate else None,
            "time": self.time
        }


class GenshinTeam(db.Model):
    """原神队伍组合数据模型"""
    __tablename__ = "genshin_teams"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_avatars = db.Column(db.Text, nullable=False, comment="队员头像URL（逗号分隔）")
    role_stars = db.Column(db.String(50), nullable=False, comment="队员星级（逗号分隔）")
    use_count = db.Column(db.Integer, comment="队伍使用次数")
    use_rate = db.Column(db.Numeric(5, 1), comment="队伍使用率（%）")
    has_count = db.Column(db.Integer, comment="可组建人数")
    has_rate = db.Column(db.Numeric(5, 1), comment="可组建率（%）")
    attend_rate = db.Column(db.Numeric(5, 1), comment="登场率（%）")
    up_use = db.Column(db.Numeric(5, 1), comment="使用率上升占比（%）")
    down_use = db.Column(db.Numeric(5, 1), comment="使用率下降占比（%）")
    up_use_num = db.Column(db.Integer, comment="上升使用次数")
    down_use_num = db.Column(db.Integer, comment="下降使用次数")

    def to_dict(self):
        """模型转字典"""
        return {
            "id": self.id,
            "role_avatars": self.role_avatars.split(',') if self.role_avatars else [],
            "role_stars": self.role_stars.split(',') if self.role_stars else [],
            "use_count": self.use_count,
            "use_rate": float(self.use_rate) if self.use_rate else None,
            "has_count": self.has_count,
            "has_rate": float(self.has_rate) if self.has_rate else None,
            "attend_rate": float(self.attend_rate) if self.attend_rate else None,
            "up_use": float(self.up_use) if self.up_use else None,
            "down_use": float(self.down_use) if self.down_use else None,
            "up_use_num": self.up_use_num,
            "down_use_num": self.down_use_num
        }