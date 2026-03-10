# 原神螺旋深渊角色数据统计大屏

> 向着星辰与深渊 —— 一个基于 Flask + MySQL + ECharts 的游戏数据可视化大屏系统，展示原神深渊角色使用率、命座分布、热门队伍等数据。

<img width="1726" height="951" alt="image" src="https://github.com/user-attachments/assets/2bb8eb44-2f10-41e0-b1ea-d7e0659ed9b6" />

---

## 📖 项目简介

本项目是一个为《原神》玩家和内容创作者设计的**数据可视化大屏**，系统通过 ETL 流程处理深渊角色数据，并在一个仿“驾驶舱”风格的页面中动态展示角色排行、命座分布、队伍搭配等关键指标。后端采用 Flask 提供 RESTful API，前端使用 ECharts 渲染图表，整体布局适配大屏及不同分辨率设备。

---

## 🛠️ 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | HTML5, CSS3, jQuery, ECharts 5.x, flexible.js (rem 适配) |
| 后端 | Python 3.8+, Flask 2.3.3, Flask-SQLAlchemy 3.1.1, Flask-CORS |
| 数据库 | MySQL 8.0 |
| 数据处理 | Python 脚本 (ETL) |
| 部署 | Gunicorn / Nginx (可选) |

---

## 📁 项目目录结构
