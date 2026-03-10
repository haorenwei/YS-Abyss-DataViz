/**
 * 工具函数模块
 */
const Utils = {
    // 图片预加载函数
    preloadImage(url) {
        return new Promise((resolve) => {
            if (!url || AppData.imageCache.has(url)) {
                resolve(AppData.imageCache.get(url) || null);
                return;
            }
            const img = new Image();
            img.onload = () => {
                AppData.imageCache.set(url, url);
                resolve(url);
            };
            img.onerror = () => {
                AppData.imageCache.set(url, null);
                resolve(null);
            };
            img.src = url;
        });
    },

    // 获取排序后的角色列表
    getSortedCharacters(limit = null) {
        const sorted = [...AppData.characters]
            .sort((a, b) => (b.use_rate || 0) - (a.use_rate || 0));
        return limit ? sorted.slice(0, limit) : sorted;
    },

    // 格式化数字
    formatNumber(num) {
        return num ? num.toLocaleString() : '0';
    }
};
