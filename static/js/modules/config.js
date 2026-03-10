/**
 * 全局配置和数据存储模块
 */
const AppConfig = {
    // API基础地址
    baseURL: 'http://127.0.0.1:5000',
    
    // 动画配置
    charSwitchInterval: 5000,      // 角色切换间隔(ms)
    rateChartSlideInterval: 4000,  // 右下图表滑动间隔(ms)
    rateChartGroupSize: 5          // 右下图表每组显示数量
};

// 全局数据存储
const AppData = {
    characters: [],
    ranks: [],
    teams: [],
    systemInfo: {},
    currentCharIndex: 0,
    currentRateGroupIndex: 0,
    imageCache: new Map()
};

// 初始化 axios
axios.defaults.baseURL = AppConfig.baseURL;
