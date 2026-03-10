原神螺旋深渊角色数据统计大屏

向着星辰与深渊 —— 一个基于 Flask + MySQL + ECharts 的游戏数据可视化大屏系统，展示《原神》深渊角色使用率、命座分布与热门队伍数据。

📷 项目预览
<img width="1726" alt="dashboard-preview" src="https://github.com/user-attachments/assets/2bb8eb44-2f10-41e0-b1ea-d7e0659ed9b6" />
📖 项目简介

本项目是一个为 《原神》玩家与游戏内容创作者设计的数据可视化系统。

系统通过 ETL 数据处理流程对深渊角色数据进行清洗、分析，并在一个仿 数据驾驶舱（Data Dashboard） 风格的大屏中展示关键指标，例如：

角色使用率排行

命座分布统计

热门深渊队伍组合

角色使用趋势变化

后端采用 Flask 提供 RESTful API，前端使用 ECharts 实现数据可视化图表，整体界面适配大屏设备和不同分辨率。

🛠 技术栈
层级	技术
前端	HTML5、CSS3、jQuery、ECharts 5.x
自适应	flexible.js（REM 适配）
后端	Python、Flask
ORM	Flask-SQLAlchemy
数据库	MySQL 8.0
数据处理	Python ETL 脚本
部署	Gunicorn + Nginx（可选）
📂 项目结构
YuanShen
│
├── app                 # Flask 后端应用
│   ├── models          # 数据模型 (SQLAlchemy)
│   └── api             # API 接口蓝图
│
├── static              # 前端资源
│   ├── js
│   │   └── modules     # 图表模块 / 数据请求模块
│   └── index.html      # 大屏主页面
│
├── Script              # 数据处理脚本 (ETL)
│
├── Data                # 原始数据文件
│
├── run.py              # Flask 启动入口
│
└── requirements.txt    # Python 依赖
🧱 系统架构

系统采用经典 四层架构设计：

用户访问层
     │
浏览器 / 大屏终端
     │
前端展示层
HTML + CSS + jQuery + ECharts
     │
后端服务层
Flask + RESTful API + SQLAlchemy
     │
数据持久层
MySQL 8.0
🔄 数据处理流程（ETL）

数据处理流程如下：

1️⃣ 数据采集

原始数据来源：

提瓦特小助手

https://www.yshelper.com/

数据格式：

shen_yuan.json
2️⃣ 数据清洗

执行 ETL 脚本：

python Script/purify.py

主要处理：

空值处理

百分比转换

字段标准化

主键冲突处理

生成清洗数据：

purified_character_data.json
3️⃣ 数据入库

通过 SQLAlchemy ORM 将数据写入 MySQL 数据库。

4️⃣ 数据可视化

前端通过 Ajax 请求 API 获取数据，并使用 ECharts 绘制图表。

📡 API 接口设计

系统遵循 RESTful API 规范，返回 JSON 数据。

方法	接口	功能
GET	/api/character/list	获取全部角色信息
GET	/api/character/detail/<name>	获取角色详细信息
GET	/api/character/constellation/<name>	获取角色命座分布
GET	/api/character/teams	获取热门队伍排行
GET	/api/system/info	获取系统信息

支持：

JSON 数据返回

跨域访问（Flask-CORS）

🖥 大屏布局设计

页面分为 六个核心区域：

1️⃣ 顶部标题区

项目名称

欢迎语

实时时间

2️⃣ 左上统计区

访问量

角色数量

样本数量

星级分布饼图

3️⃣ 左下角色区

角色头像

命座分布

自动轮播

4️⃣ 中间队伍区

热门深渊队伍排行

卡片式展示

自动滚动

5️⃣ 右上排行区

角色使用率排行

点击查看详情

6️⃣ 右下趋势区

使用率变化

柱状图 + 折线图

✨ 功能模块
模块	功能
角色统计	统计角色使用率与持有率
命座分析	0-6 命座持有率分布
队伍推荐	热门深渊队伍排行
趋势变化	角色使用率环比变化
自动轮播	角色与排行榜自动滚动
响应式布局	适配不同屏幕分辨率
🎨 视觉设计

界面设计参考 原神 UI 风格：

深色背景

青色发光高亮

数据驾驶舱风格布局

视觉规则：

⭐ 五星角色：金色边框

⭐ 四星角色：紫色边框

🥇 排行榜前三名：金 / 银 / 铜标识

🎯 命座分布：0-6 命不同颜色区分

🖱 交互体验

系统提供多种交互效果：

图表动画

鼠标悬停提示

点击查看角色详情

自动轮播

无缝滚动

实时时间刷新

适合：

数据大屏展示

视频直播背景

游戏社区展示

🚀 部署运行
环境要求

Python 3.8+

MySQL 8.0

pip

1️⃣ 克隆项目
git clone https://github.com/yourname/YuanShen.git
cd YuanShen
2️⃣ 安装依赖
pip install -r requirements.txt
3️⃣ 配置数据库

创建数据库：

yuanshen

修改配置：

app/config.py

填写 MySQL 连接信息。

4️⃣ 数据处理（可选）
python Script/purify.py
5️⃣ 启动服务
python run.py

访问：

http://127.0.0.1:5000
💡 项目价值
🎮 应用场景

游戏社区数据展示

B站 / 直播数据背景

玩家数据分析

游戏攻略制作

数据可视化教学案例

🧠 技术价值

Flask Web 项目完整架构

RESTful API 设计实践

SQLAlchemy ORM 使用

ECharts 数据可视化

ETL 数据处理流程

数据大屏设计实践

📊 应用价值

为玩家提供 数据驱动的角色培养与配队参考

为内容创作者提供 高质量数据素材

为游戏社区提供 可视化展示方案

愿此行，终抵群星。

📄 数据来源

原始数据来源：

提瓦特小助手

https://www.yshelper.com/
