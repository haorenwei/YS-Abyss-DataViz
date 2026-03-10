/**
 * 应用主入口
 */
const App = {
    // 加载数据
    async loadData() {
        try {
            const [sysRes, charRes, rankRes] = await Promise.all([
                axios.get('/api/character/system_info'),
                axios.get('/api/character/list'),
                axios.get('/api/character/ranks')
            ]);
            
            AppData.systemInfo = sysRes.data.data || {};
            AppData.characters = charRes.data.data || [];
            AppData.ranks = rankRes.data.data || [];
            
            // 预加载前20个角色的头像
            const topChars = Utils.getSortedCharacters(20);
            await Promise.all(topChars.map(c => Utils.preloadImage(c.avatar)));
            
            return true;
        } catch (error) {
            console.error('数据加载失败:', error);
            return false;
        }
    },

    // 初始化所有模块
    initModules() {
        LeftTop.init();
        LeftBottom.init();
        RightTop.init();
        RightBottom.init();
        Center.init();  // 初始化中间热门队伍模块
    },

    // 启动应用
    async start() {
        const loaded = await this.loadData();
        if (loaded) {
            this.initModules();
        }
    }
};

// 启动应用
App.start();
