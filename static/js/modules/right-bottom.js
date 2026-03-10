/**
 * 右下区域模块 - 使用率变化动态滑动图表
 */
const RightBottom = {
    chart: null,
    allData: [],
    totalGroups: 0,

    // 准备数据
    prepareData() {
        const topChars = AppData.characters
            .filter(c => c.use_rate !== null && c.use_rate >= 10) // 过滤本期使用率低于10%的数据
            .sort((a, b) => (b.use_rate || 0) - (a.use_rate || 0));
        
        this.allData = topChars;
        this.totalGroups = Math.ceil(topChars.length / AppConfig.rateChartGroupSize);
    },

    // 获取当前组数据
    getCurrentGroupData() {
        const size = AppConfig.rateChartGroupSize;
        const start = AppData.currentRateGroupIndex * size;
        const group = this.allData.slice(start, start + size);
        
        return {
            names: group.map(c => c.name),
            current: group.map(c => c.use_rate || 0),
            old: group.map(c => c.use_rate_old || 0),
            change: group.map(c => c.use_rate_change || 0)
        };
    },

    // 更新图表（带动画）
    updateChart(isInit = false) {
        if (!this.chart) {
            this.chart = echarts.init(document.getElementById('echart4'));
        }
        
        const data = this.getCurrentGroupData();
        const groupInfo = `(${AppData.currentRateGroupIndex + 1}/${this.totalGroups})`;
        
        const option = {
            tooltip: {
                trigger: 'axis',
                axisPointer: { type: 'shadow' },
                formatter: function(params) {
                    let result = params[0].name + '<br/>';
                    params.forEach(p => {
                        result += p.marker + p.seriesName + ': ' + p.value + '%<br/>';
                    });
                    return result;
                }
            },
            legend: {
                top: '0%',
                data: ['上期使用率', '本期使用率', '涨跌幅'],
                textStyle: { color: 'rgba(255,255,255,.4)', fontSize: 12 }
            },
            grid: {
                left: '3%', top: '18%', right: '3%', bottom: '5%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: data.names,
                axisLine: { lineStyle: { color: 'rgba(80,80,80,.5)' } },
                axisLabel: { 
                    color: 'rgba(255,255,255,.5)', 
                    fontSize: 11,
                    rotate: 0,
                    interval: 0
                },
                animationDuration: isInit ? 0 : 800,
                animationDurationUpdate: 800
            },
            yAxis: [
                {
                    type: 'value',
                    name: '使用率(%)',
                    nameTextStyle: { color: 'rgba(255,255,255,.4)', fontSize: 10 },
                    axisLine: { lineStyle: { color: 'rgba(80,80,80,.5)' } },
                    axisLabel: { color: 'rgba(255,255,255,.4)', fontSize: 10 },
                    splitLine: { lineStyle: { color: 'rgba(80,80,80,.3)' } }
                },
                {
                    type: 'value',
                    name: '涨跌幅(%)',
                    nameTextStyle: { color: 'rgba(255,255,255,.4)', fontSize: 10 },
                    axisLine: { lineStyle: { color: 'rgba(80,80,80,.5)' } },
                    axisLabel: { color: 'rgba(255,255,255,.4)', fontSize: 10 },
                    splitLine: { show: false }
                }
            ],
            animationDuration: isInit ? 300 : 800,
            animationDurationUpdate: 800,
            animationEasing: 'cubicOut',
            series: [
                {
                    name: '上期使用率',
                    type: 'bar',
                    barWidth: '25%',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#66ccff' },
                            { offset: 1, color: 'rgba(102, 204, 255, 0.3)' }
                        ]),
                        barBorderRadius: [3, 3, 0, 0]
                    },
                    data: data.old,
                    animationDelay: idx => idx * 50
                },
                {
                    name: '本期使用率',
                    type: 'bar',
                    barWidth: '25%',
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#00ffcc' },
                            { offset: 1, color: 'rgba(0, 255, 204, 0.3)' }
                        ]),
                        barBorderRadius: [3, 3, 0, 0]
                    },
                    data: data.current,
                    animationDelay: idx => idx * 50 + 100
                },
                {
                    name: '涨跌幅',
                    type: 'line',
                    yAxisIndex: 1,
                    smooth: true,
                    symbol: 'circle',
                    symbolSize: 8,
                    lineStyle: { color: '#ffcc00', width: 2 },
                    itemStyle: {
                        color: function(params) {
                            return params.value >= 0 ? '#ff6666' : '#66ff66';
                        },
                        borderColor: '#1a1a1a',
                        borderWidth: 1
                    },
                    data: data.change,
                    animationDelay: idx => idx * 50 + 200
                }
            ]
        };
        
        this.chart.setOption(option, !isInit);
    },

    // 切换到下一组
    nextGroup() {
        AppData.currentRateGroupIndex = (AppData.currentRateGroupIndex + 1) % this.totalGroups;
        this.updateChart(false);
    },

    // 初始化
    init() {
        this.prepareData();
        this.updateChart(true);
        
        // 定时切换组（4秒）
        setInterval(() => {
            this.nextGroup();
        }, AppConfig.rateChartSlideInterval);
        
        // 响应式
        window.addEventListener('resize', () => {
            this.chart && this.chart.resize();
        });
    }
};
