from app.extensions import db


class FileEntity(db.Model):
    """文件数据模型（对应你最初的JSON字段）"""
    __tablename__ = "yuanshen_db"  # MySQL表名

    # 字段定义（与JSON字段一一对应）
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    identifier = db.Column(db.String(64), unique=True, nullable=False, comment="唯一标识")
    entity_type = db.Column(db.Integer, comment="实体类型")
    file_name = db.Column(db.String(128), comment="文件名")
    file_key = db.Column(db.String(255), comment="文件存储key")
    file_size = db.Column(db.Integer, comment="文件大小（字节）")
    file_type = db.Column(db.Integer, comment="文件类型")
    file_name_state = db.Column(db.Integer, comment="文件名状态")
    file_parse_state = db.Column(db.Integer, comment="文件解析状态")

    def to_dict(self):
        """模型转字典（方便接口返回JSON）"""
        return {
            "identifier": self.identifier,
            "entity_type": self.entity_type,
            "file_name": self.file_name,
            "file_key": self.file_key,
            "file_size": self.file_size,
            "file_type": self.file_type,
            "file_name_state": self.file_name_state,
            "file_parse_state": self.file_parse_state
        }