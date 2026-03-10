/**
 * 右上区域模块 - 角色排行滚动列表
 */
const RightTop = {
    // 更新滚动列表
    update() {
        const sorted = Utils.getSortedCharacters();
        const scrollList = document.getElementById('scrollList');
        let html = '';
        
        // 复制两份用于无缝滚动
        for (let i = 0; i < 2; i++) {
            sorted.forEach(char => {
                const isFiveStar = char.star === 5;
                const placeholderClass = isFiveStar ? 'avatar-placeholder star5' : 'avatar-placeholder star4';
                const avatarHtml = char.avatar 
                    ? `<img src="${char.avatar}" alt="${char.name}" onerror="this.style.display='none';this.nextElementSibling.style.display='flex';"><div class="${placeholderClass}" style="display:none">${char.name.charAt(0)}</div>`
                    : `<div class="${placeholderClass}">${char.name.charAt(0)}</div>`;
                html += `
                    <div class="scroll-item" onclick="showCharacterDetail('${char.name}')">
                        ${avatarHtml}
                        <div class="info">
                            <span>${char.name}</span>
                            <span>${Utils.formatNumber(char.use_count)}</span>
                            <span>${Utils.formatNumber(char.own_count)}</span>
                            <span>${char.own_rate || 0}%</span>
                            <span class="use-rate-highlight">${char.use_rate || 0}%</span>
                        </div>
                    </div>
                `;
            });
        }
        
        scrollList.innerHTML = html;
    },

    // 初始化
    init() {
        this.update();
    }
};
