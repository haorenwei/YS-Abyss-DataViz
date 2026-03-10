/**
 * 左下区域模块 - 角色图像（左）+ 命座持有率饼图（右）
 */
const LeftBottom = {
    chart: null,

    // 更新角色详情和命座图表
    async update() {
        if (AppData.characters.length === 0) return;
        
        const topChars = Utils.getSortedCharacters(20);
        const char = topChars[AppData.currentCharIndex % topChars.length];
        
        // 更新角色头像区域 - 使用与right-top相同的方式
        const avatarArea = document.getElementById('charAvatarArea');
        if (avatarArea) {
            const isFiveStar = char.star === 5;
            const placeholderClass = isFiveStar ? 'char-avatar-placeholder star5' : 'char-avatar-placeholder star4';
            const avatarHtml = char.avatar 
                ? `<img src="${char.avatar}" alt="${char.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><div class="${placeholderClass}" style="display:none">${char.name.charAt(0)}</div>`
                : `<div class="${placeholderClass}">${char.name.charAt(0)}</div>`;
            avatarArea.innerHTML = avatarHtml;
        }
        
        document.getElementById('charName').textContent = char.name;
        document.getElementById('charStar').textContent = '★'.repeat(char.star || 5);
        
        // 获取该角色的命座数据
        const charRank = AppData.ranks.find(r => r.name === char.name);
        if (charRank) {
            this.updateChart(charRank);
        }
    },

    // 更新命座饼图
    updateChart(rankData) {
        if (!this.chart) {
            this.chart = echarts.init(document.getElementById('constellation-pie'));
        }
        
        // 显示全部 0-6 命
        const pieData = [
            { value: rankData.c0_rate || 0, name: '0命' },
            { value: rankData.c1_rate || 0, name: '1命' },
            { value: rankData.c2_rate || 0, name: '2命' },
            { value: rankData.c3_rate || 0, name: '3命' },
            { value: rankData.c4_rate || 0, name: '4命' },
            { value: rankData.c5_rate || 0, name: '5命' },
            { value: rankData.c6_rate || 0, name: '6命' }
        ];
        
        const pieColors = [
            '#00ffcc',  // 0命 - 青色
            '#ffcc00',  // 1命 - 金色
            '#ff6699',  // 2命 - 粉色
            '#66ff66',  // 3命 - 绿色
            '#ff9933',  // 4命 - 橙色
            '#cc66ff',  // 5命 - 紫色
            '#66ccff'   // 6命 - 蓝色
        ];
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c}%'
            },
            legend: {
                orient: 'vertical',
                right: '5%',
                top: 'center',
                textStyle: {
                    color: 'rgba(255,255,255,.7)',
                    fontSize: 10
                },
                itemWidth: 10,
                itemHeight: 10
            },
            series: [{
                type: 'pie',
                radius: ['30%', '60%'],
                center: ['35%', '50%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 4,
                    borderColor: '#1a1a1a',
                    borderWidth: 2
                },
                label: {
                    show: false
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 14,
                        fontWeight: 'bold',
                        formatter: '{b}\n{c}%'
                    }
                },
                labelLine: { show: false },
                data: pieData.map((item, i) => ({
                    ...item,
                    itemStyle: { color: pieColors[i] }
                }))
            }]
        };
        
        this.chart.setOption(option);
    },

    // 显示指定角色
    showCharacter(name) {
        const topChars = Utils.getSortedCharacters(20);
        const index = topChars.findIndex(c => c.name === name);
        if (index !== -1) {
            AppData.currentCharIndex = index;
            this.update();
        }
    },

    // 初始化
    init() {
        this.update();
        
        // 定时切换角色
        setInterval(() => {
            const topChars = Utils.getSortedCharacters(20);
            AppData.currentCharIndex = (AppData.currentCharIndex + 1) % topChars.length;
            this.update();
        }, AppConfig.charSwitchInterval);
        
        // 响应式
        window.addEventListener('resize', () => {
            this.chart && this.chart.resize();
        });
    }
};

// 全局函数供点击调用
function showCharacterDetail(name) {
    LeftBottom.showCharacter(name);
}
