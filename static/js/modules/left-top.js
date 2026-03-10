/**
 * 左上区域模块 - 系统信息、统计扇形图、最热门角色和队伍
 */
const LeftTop = {
    pieChart: null,

    // 更新系统信息
    updateSystemInfo() {
        const info = AppData.systemInfo;
        if (info.title) {
            document.getElementById('mainTitle').textContent = info.title;
        }
        if (info.visit_count !== undefined) {
            document.getElementById('visitCount').textContent = info.visit_count;
        }
        if (info.top_own) {
            document.getElementById('topOwn').textContent = Utils.formatNumber(info.top_own);
        }
        // 显示提示信息
        let tipsHtml = '';
        if (info.update_info) tipsHtml += info.update_info + '<br>';
        if (info.tips) tipsHtml += info.tips;
        document.getElementById('tipsInfo').innerHTML = tipsHtml;
    },

    // 更新统计数据
    updateStatCards() {
        const chars = AppData.characters;
        const total = chars.length;
        const fiveStar = chars.filter(c => c.star === 5).length;
        const fourStar = chars.filter(c => c.star === 4).length;
        
        document.getElementById('totalCharacters').textContent = total;
        
        // 更新扇形图
        this.updatePieChart(fiveStar, fourStar);
    },

    // 更新扇形图
    updatePieChart(fiveStar, fourStar) {
        if (!this.pieChart) {
            this.pieChart = echarts.init(document.getElementById('starPieChart'));
        }
        
        const option = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)'
            },
            legend: {
                orient: 'vertical',
                right: '5%',
                top: 'center',
                textStyle: {
                    color: 'rgba(255,255,255,.7)',
                    fontSize: 12
                }
            },
            series: [{
                type: 'pie',
                radius: ['40%', '70%'],
                center: ['35%', '50%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 6,
                    borderColor: '#1a1a1a',
                    borderWidth: 2
                },
                label: {
                    show: false
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 16,
                        fontWeight: 'bold',
                        formatter: '{b}\n{c}个'
                    }
                },
                labelLine: { show: false },
                data: [
                    { 
                        value: fiveStar, 
                        name: '五星角色',
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                                { offset: 0, color: '#ffd700' },
                                { offset: 1, color: '#ffaa00' }
                            ])
                        }
                    },
                    { 
                        value: fourStar, 
                        name: '四星角色',
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
                                { offset: 0, color: '#a855f7' },
                                { offset: 1, color: '#8b5cf6' }
                            ])
                        }
                    }
                ]
            }]
        };
        
        this.pieChart.setOption(option);
    },

    // 更新最热门角色和队伍展示
    updateHotDisplay() {
        // 获取最热门角色（使用率最高）
        const topChar = Utils.getSortedCharacters(1)[0];
        const hotCharContainer = document.getElementById('hotCharacter');
        
        if (topChar && hotCharContainer) {
            const isFiveStar = topChar.star === 5;
            const placeholderClass = isFiveStar ? 'hot-char-placeholder star5' : 'hot-char-placeholder star4';
            const avatarHtml = topChar.avatar 
                ? `<img src="${topChar.avatar}" alt="${topChar.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><div class="${placeholderClass}" style="display:none">${topChar.name.charAt(0)}</div>`
                : `<div class="${placeholderClass}">${topChar.name.charAt(0)}</div>`;
            
            hotCharContainer.innerHTML = `
                ${avatarHtml}
                <div class="hot-char-info">
                    <div class="hot-char-name">${topChar.name}</div>
                    <div class="hot-char-rate">使用率: ${topChar.use_rate || 0}%</div>
                </div>
            `;
        }
        
        // 获取最热门队伍
        const teams = AppData.teams || [];
        const topTeam = teams[0];
        const hotTeamContainer = document.getElementById('hotTeam');
        
        if (topTeam && hotTeamContainer) {
            const avatars = topTeam.role_avatars || [];
            const stars = topTeam.role_stars || [];
            let avatarsHtml = '';
            
            avatars.forEach((avatar, i) => {
                const star = parseInt(stars[i]) || 4;
                const starClass = star === 5 ? 'star5' : 'star4';
                // 根据头像获取角色名首字
                const char = AppData.characters.find(c => c.avatar === avatar);
                const charInitial = char ? char.name.charAt(0) : '?';
                const placeholderClass = star === 5 ? 'hot-team-placeholder star5' : 'hot-team-placeholder star4';
                
                avatarsHtml += `
                    <div class="hot-team-member ${starClass}">
                        <img src="${avatar}" alt="角色" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><div class="${placeholderClass}" style="display:none">${charInitial}</div>
                    </div>
                `;
            });
            
            hotTeamContainer.innerHTML = `
                <div class="hot-team-avatars">
                    ${avatarsHtml}
                </div>
                <div class="hot-team-rate">使用率: ${topTeam.use_rate || 0}%</div>
            `;
        }
    },

    // 初始化
    init() {
        this.updateSystemInfo();
        this.updateStatCards();
        
        // 延迟加载热门展示（等待队伍数据加载完成）
        setTimeout(() => {
            this.updateHotDisplay();
        }, 1500);
        
        // 响应式
        window.addEventListener('resize', () => {
            this.pieChart && this.pieChart.resize();
        });
    }
};
