from app import create_app

# 创建应用（dev=开发环境，prod=生产环境）
app = create_app(config_name="dev")

if __name__ == "__main__":
    # 启动Flask服务
    app.run(host="0.0.0.0", port=5000, debug=True)




