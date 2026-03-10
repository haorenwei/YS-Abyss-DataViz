import json
import pymysql
from pymysql.err import OperationalError, ProgrammingError

# -------------------------- 配置参数 --------------------------
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_DB = "yuanshen_db"
MYSQL_PORT = 3306
JSON_FILE_PATH = "../Date/purified_character_data.json"

# -------------------------- 数据库连接函数 --------------------------
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DB} DEFAULT CHARACTER SET utf8mb4")
        conn.select_db(MYSQL_DB)
        return conn
    except OperationalError as e:
        print(f"数据库连接失败：{e}")
        exit(1)


# -------------------------- 创建数据表 --------------------------
def create_tables(conn):
    create_sqls = [
        # 系统信息表
        """
        CREATE TABLE IF NOT EXISTS system_info (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) COMMENT '标题',
            version VARCHAR(50) COMMENT '版本信息',
            now_version VARCHAR(50) COMMENT '本期版本',
            old_version VARCHAR(50) COMMENT '上期版本',
            last_update VARCHAR(20) COMMENT '最后更新时间',
            update_info VARCHAR(100) COMMENT '更新信息',
            top_own INT COMMENT '有效样本数',
            tips TEXT COMMENT '数据总结',
            tips2 TEXT COMMENT '使用提示',
            star36_rate VARCHAR(10) COMMENT '36星通关率',
            visit_count INT DEFAULT 0 COMMENT '访问量'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统配置信息表';
        """,
        # 角色基础数据表
        """
        CREATE TABLE IF NOT EXISTS genshin_characters (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL COMMENT '角色名称',
            ename VARCHAR(50) COMMENT '英文名称',
            star TINYINT NOT NULL COMMENT '星级（4/5）',
            avatar VARCHAR(255) COMMENT '头像URL',
            use_count INT COMMENT '使用次数',
            own_count INT COMMENT '持有次数',
            use_rate DECIMAL(5,1) COMMENT '使用率（%）',
            own_rate DECIMAL(5,1) COMMENT '持有率（%）',
            collection DECIMAL(3,1) COMMENT '收藏值',
            rank_class VARCHAR(5) COMMENT '评级类别',
            use_rate_old DECIMAL(5,1) COMMENT '上期使用率',
            use_rate_change DECIMAL(5,1) COMMENT '使用率变化',
            UNIQUE KEY uk_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原神角色基础数据表';
        """,
        # 角色评级详情表
        """
        CREATE TABLE IF NOT EXISTS genshin_character_ranks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL COMMENT '角色名称',
            rank_name VARCHAR(10) NOT NULL COMMENT '评级名称',
            c0_rate DECIMAL(5,1) COMMENT '0命持有率',
            c1_rate DECIMAL(5,1) COMMENT '1命持有率',
            c2_rate DECIMAL(5,1) COMMENT '2命持有率',
            c3_rate DECIMAL(5,1) COMMENT '3命持有率',
            c4_rate DECIMAL(5,1) COMMENT '4命持有率',
            c5_rate DECIMAL(5,1) COMMENT '5命持有率',
            c6_rate DECIMAL(5,1) COMMENT '6命持有率',
            time INT COMMENT '时间字段',
            UNIQUE KEY uk_name_rank (name, rank_name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原神角色评级详情表';
        """,
        # 队伍组合数据表
        """
        CREATE TABLE IF NOT EXISTS genshin_teams (
            id INT AUTO_INCREMENT PRIMARY KEY,
            role_avatars TEXT NOT NULL COMMENT '队员头像URL',
            role_stars VARCHAR(50) NOT NULL COMMENT '队员星级',
            use_count INT COMMENT '队伍使用次数',
            use_rate DECIMAL(5,1) COMMENT '队伍使用率',
            has_count INT COMMENT '可组建人数',
            has_rate DECIMAL(5,1) COMMENT '可组建率',
            attend_rate DECIMAL(5,1) COMMENT '登场率',
            up_use DECIMAL(5,1) COMMENT '使用率上升占比',
            down_use DECIMAL(5,1) COMMENT '使用率下降占比',
            up_use_num INT COMMENT '上升使用次数',
            down_use_num INT COMMENT '下降使用次数'
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='原神队伍组合数据表';
        """
    ]

    with conn.cursor() as cursor:
        for sql in create_sqls:
            try:
                cursor.execute(sql)
            except ProgrammingError as e:
                print(f"创建表失败：{e}")
                conn.rollback()
                return False
    conn.commit()
    print("数据表创建成功！")
    return True

# -------------------------- 解析JSON数据 --------------------------
def parse_json_data(json_path):
    """解析提纯后的JSON文件"""
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        system_info = data.get("system_info", {})
        has_list = data.get("has_list", [])
        character_ranks = data.get("character_ranks", [])
        use_rate_changes = data.get("use_rate_changes", [])
        teams = data.get("teams", [])
        
        return system_info, has_list, character_ranks, use_rate_changes, teams
    except FileNotFoundError:
        print(f"JSON文件未找到：{json_path}")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"JSON解析失败：{e}")
        exit(1)

# -------------------------- 插入数据 --------------------------
def insert_data(conn, system_info, has_list, character_ranks, use_rate_changes, teams):
    try:
        with conn.cursor() as cursor:
            # 1. 插入系统信息
            cursor.execute("DELETE FROM system_info")  # 清空旧数据
            sys_sql = """
                INSERT INTO system_info 
                (title, version, now_version, old_version, last_update, update_info, top_own, tips, tips2, star36_rate, visit_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0)
            """
            cursor.execute(sys_sql, (
                system_info.get("title"),
                system_info.get("version"),
                system_info.get("now_version"),
                system_info.get("old_version"),
                system_info.get("last_update"),
                system_info.get("update"),
                system_info.get("top_own"),
                system_info.get("tips"),
                system_info.get("tips2"),
                system_info.get("star36_rate")
            ))
            print("插入系统信息成功")

            # 2. 构建使用率变化映射表
            rate_change_map = {}
            for item in use_rate_changes:
                name = item.get("name")
                rate_change_map[name] = {
                    "use_rate_old": item.get("use_rate_old"),
                    "use_rate_change": item.get("use_rate_change")
                }

            # 3. 插入角色基础数据（合并使用率变化数据）
            char_sql = """
                INSERT INTO genshin_characters 
                (name, star, avatar, use_count, own_count, use_rate, own_rate, collection, rank_class, use_rate_old, use_rate_change)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    star=VALUES(star), avatar=VALUES(avatar), use_count=VALUES(use_count),
                    own_count=VALUES(own_count), use_rate=VALUES(use_rate), own_rate=VALUES(own_rate),
                    collection=VALUES(collection), rank_class=VALUES(rank_class),
                    use_rate_old=VALUES(use_rate_old), use_rate_change=VALUES(use_rate_change)
            """
            char_params = []
            for char in has_list:
                name = char.get("name")
                rate_info = rate_change_map.get(name, {})
                use_rate_old = rate_info.get("use_rate_old")
                use_rate_change = rate_info.get("use_rate_change")
                # 处理"-"值
                if use_rate_old == "-":
                    use_rate_old = None
                char_params.append((
                    name,
                    char.get("star"),
                    char.get("avatar"),
                    char.get("use"),
                    char.get("own"),
                    char.get("use_rate"),
                    char.get("own_rate"),
                    char.get("collection"),
                    char.get("rank_class"),
                    use_rate_old,
                    use_rate_change
                ))
            cursor.executemany(char_sql, char_params)
            print(f"插入角色基础数据：{len(char_params)} 条")

            # 4. 插入角色评级详情数据
            rank_sql = """
                INSERT INTO genshin_character_ranks 
                (name, rank_name, c0_rate, c1_rate, c2_rate, c3_rate, c4_rate, c5_rate, c6_rate, time)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    c0_rate=VALUES(c0_rate), c1_rate=VALUES(c1_rate), c2_rate=VALUES(c2_rate),
                    c3_rate=VALUES(c3_rate), c4_rate=VALUES(c4_rate), c5_rate=VALUES(c5_rate),
                    c6_rate=VALUES(c6_rate), time=VALUES(time)
            """
            rank_params = []
            for rank in character_ranks:
                rank_params.append((
                    rank.get("name"),
                    rank.get("rank_name"),
                    rank.get("c0_rate"),
                    rank.get("c1_rate"),
                    rank.get("c2_rate"),
                    rank.get("c3_rate"),
                    rank.get("c4_rate"),
                    rank.get("c5_rate"),
                    rank.get("c6_rate"),
                    rank.get("time")
                ))
            cursor.executemany(rank_sql, rank_params)
            print(f"插入角色评级数据：{len(rank_params)} 条")

            # 5. 插入队伍组合数据
            cursor.execute("DELETE FROM genshin_teams")  # 清空旧数据
            team_sql = """
                INSERT INTO genshin_teams 
                (role_avatars, role_stars, use_count, use_rate, has_count, has_rate, attend_rate, up_use, down_use, up_use_num, down_use_num)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            team_params = []
            for team in teams:
                role_avatars = ",".join([r.get("avatar", "") for r in team.get("role", [])])
                role_stars = ",".join([str(r.get("star", "")) for r in team.get("role", [])])
                team_params.append((
                    role_avatars,
                    role_stars,
                    team.get("use"),
                    team.get("use_rate"),
                    team.get("has"),
                    team.get("has_rate"),
                    team.get("attend_rate"),
                    team.get("up_use"),
                    team.get("down_use"),
                    team.get("up_use_num"),
                    team.get("down_use_num")
                ))
            cursor.executemany(team_sql, team_params)
            print(f"插入队伍数据：{len(team_params)} 条")

        conn.commit()
        print("所有数据插入成功！")
    except Exception as e:
        conn.rollback()
        print(f"数据插入失败：{e}")
        return False
    return True


# -------------------------- 主函数 --------------------------
def main():
    conn = get_db_connection()
    if not create_tables(conn):
        conn.close()
        return
    system_info, has_list, character_ranks, use_rate_changes, teams = parse_json_data(JSON_FILE_PATH)
    insert_data(conn, system_info, has_list, character_ranks, use_rate_changes, teams)
    conn.close()


if __name__ == "__main__":
    main()