import json
import os

# 配置文件路径
INPUT_FILE = "shen_yuan.json"
OUTPUT_FILE = "purified_character_data.json"

def purify_character_data(input_file, output_file):
    """
    提纯原神角色适配数据：
    1. 提取系统信息（title, tips, last_update等）
    2. 提取角色基础数据（has_list）
    3. 提取角色评级和命座数据（result[0]）
    4. 提取角色使用率变化数据（result[1]）- 含上期使用率和涨跌幅
    5. 提取队伍数据（result[3]）
    """
    full_input_path = os.path.join("../Date/", input_file)
    full_output_path = os.path.join("../Date/", output_file)

    if not os.path.exists(full_input_path):
        print(f"错误：找不到文件 {full_input_path}")
        return

    try:
        with open(full_input_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # 1. 提取系统配置信息
        system_info = {
            "title": raw_data.get("title", ""),
            "version": raw_data.get("version", ""),
            "now_version": raw_data.get("now_version", ""),
            "old_version": raw_data.get("old_version", ""),
            "last_update": raw_data.get("last_update", ""),
            "update": raw_data.get("update", ""),
            "top_own": raw_data.get("top_own", 0),
            "tips": raw_data.get("tips", ""),
            "tips2": raw_data.get("tips2", ""),
            "star36_rate": raw_data.get("star36_rate", ""),
        }

        # 2. 提取角色基础数据
        has_list = raw_data.get("has_list", [])

        # 3. 提取result数据
        result = raw_data.get("result", [])
        
        # result[0]: 角色评级和命座数据
        character_ranks = []
        if len(result) > 0:
            for rank_group in result[0]:
                rank_name = rank_group.get("rank_name")
                for char in rank_group.get("list", []):
                    char["rank_name"] = rank_name
                    character_ranks.append(char)
        
        # result[1]: 角色使用率变化数据（含上期使用率和涨跌幅）
        use_rate_changes = []
        if len(result) > 1:
            use_rate_changes = result[1]
        
        # result[3]: 队伍数据
        teams = []
        if len(result) > 3:
            teams = result[3]

        # 4. 整合提纯数据
        purified_data = {
            "system_info": system_info,
            "has_list": has_list,
            "character_ranks": character_ranks,
            "use_rate_changes": use_rate_changes,
            "teams": teams,
        }

        # 5. 保存数据
        with open(full_output_path, 'w', encoding='utf-8') as f:
            json.dump(purified_data, f, ensure_ascii=False, indent=2)

        # 输出统计
        print("=" * 50)
        print("数据提纯完成！")
        print(f"系统信息: {system_info['title']}")
        print(f"角色基础数据: {len(has_list)} 条")
        print(f"角色评级数据: {len(character_ranks)} 条")
        print(f"使用率变化数据: {len(use_rate_changes)} 条")
        print(f"队伍数据: {len(teams)} 条")
        print(f"已保存至: {full_output_path}")

    except json.JSONDecodeError:
        print("错误：文件不是有效的JSON格式")
    except Exception as e:
        print(f"处理过程中发生错误：{str(e)}")


if __name__ == "__main__":
    purify_character_data(INPUT_FILE, OUTPUT_FILE)