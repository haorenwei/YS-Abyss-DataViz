/**
 * 中间区域模块 - 热门队伍滚动大屏
 */
const Center = {
    teams: [],
    scrollInterval: null,
    
    // 加载队伍数据
    async loadTeams() {
        try {
            const res = await axios.get('/api/character/teams?limit=50');
            if (res.data.code === 200) {
                this.teams = res.data.data || [];
                AppData.teams = this.teams;
                return true;
            }
        } catch (error) {
            console.error('队伍数据加载失败:', error);
        }
        return false;
    },

    // 根据头像URL获取角色名首字
    getCharNameByAvatar(avatarUrl) {
        const char = AppData.characters.find(c => c.avatar === avatarUrl);
        return char ? char.name.charAt(0) : '?';
    },

    // 渲染队伍列表
    renderTeamList() {
        const container = document.getElementById('teamScrollList');
        if (!container || this.teams.length === 0) return;
        
        let html = '';
        
        this.teams.forEach((team, index) => {
            const avatars = team.role_avatars || [];
            const stars = team.role_stars || [];
            const useRate = team.use_rate || 0;
            
            // 队员头像HTML
            let avatarsHtml = '';
            avatars.forEach((avatar, i) => {
                const star = parseInt(stars[i]) || 4;
                const starClass = star === 5 ? 'star5' : 'star4';
                const charInitial = this.getCharNameByAvatar(avatar);
                const placeholderClass = star === 5 ? 'team-member-placeholder star5' : 'team-member-placeholder star4';
                
                avatarsHtml += `
                    <div class="team-member ${starClass}">
                        <img src="${avatar}" alt="角色" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><div class="${placeholderClass}" style="display:none">${charInitial}</div>
                    </div>
                `;
            });
            
            html += `
                <div class="team-item">
                    <div class="team-rank">${index + 1}</div>
                    <div class="team-members">
                        ${avatarsHtml}
                    </div>
                    <div class="team-stats">
                        <div class="team-rate">${useRate.toFixed(1)}%</div>
                        <div class="team-label">使用率</div>
                    </div>
                </div>
            `;
        });
        
        // 复制一份用于无缝滚动
        container.innerHTML = html + html;
    },

    // 初始化
    async init() {
        await this.loadTeams();
        this.renderTeamList();
        
        // 设置滚动动画
        const scrollList = document.getElementById('teamScrollList');
        if (scrollList) {
            // 计算滚动时长基于队伍数量
            const duration = Math.max(60, this.teams.length * 3);
            scrollList.style.animationDuration = `${duration}s`;
        }
    }
};
