// 高维学堂 H5 页面交互脚本

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 添加页面加载动画
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease-in-out';
        document.body.style.opacity = '1';
    }, 100);
    
    // 初始化装饰动画
    initDecorations();
    
    // 添加触摸反馈
    addTouchFeedback();
});

// 显示庆祝弹窗
function showCelebration() {
    const modal = document.getElementById('celebrationModal');
    modal.style.display = 'block';
    
    // 添加弹窗显示动画
    const modalContent = modal.querySelector('.modal-content');
    modalContent.style.transform = 'translateY(-50%) scale(0.8)';
    modalContent.style.opacity = '0';
    
    setTimeout(() => {
        modalContent.style.transition = 'all 0.3s ease-out';
        modalContent.style.transform = 'translateY(-50%) scale(1)';
        modalContent.style.opacity = '1';
    }, 10);
    
    // 播放庆祝音效（如果需要）
    // playCelebrationSound();
    
    // 添加额外的庆祝效果
    createFloatingFlowers();
}

// 关闭庆祝弹窗
function closeCelebration() {
    const modal = document.getElementById('celebrationModal');
    const modalContent = modal.querySelector('.modal-content');
    
    modalContent.style.transition = 'all 0.3s ease-in';
    modalContent.style.transform = 'translateY(-50%) scale(0.8)';
    modalContent.style.opacity = '0';
    
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// 分享奖励功能
function shareReward() {
    // 检查是否支持 Web Share API
    if (navigator.share) {
        navigator.share({
            title: '高维学堂流程型组织课100期庆典',
            text: '🎉 我在高维学堂流程型组织课100期庆典中获得了5朵小红花奖励！一起来学习成长吧！',
            url: window.location.href
        }).then(() => {
            showToast('分享成功！感谢您的推广！');
        }).catch((error) => {
            console.log('分享失败:', error);
            fallbackShare();
        });
    } else {
        // 降级处理：复制链接到剪贴板
        fallbackShare();
    }
}

// 降级分享处理
function fallbackShare() {
    const shareText = '🎉 高维学堂流程型组织课100期庆典！我获得了5朵小红花奖励！一起来学习成长吧！\n' + window.location.href;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(shareText).then(() => {
            showToast('链接已复制到剪贴板！');
        }).catch(() => {
            showShareModal(shareText);
        });
    } else {
        showShareModal(shareText);
    }
}

// 显示分享模态框
function showShareModal(text) {
    const shareModal = document.createElement('div');
    shareModal.className = 'modal';
    shareModal.innerHTML = `
        <div class="modal-content">
            <span class="close" onclick="this.parentElement.parentElement.remove()">&times;</span>
            <div class="modal-body">
                <h2>📤 分享内容</h2>
                <textarea readonly style="width: 100%; height: 100px; padding: 10px; border: 2px solid var(--light-blue); border-radius: 10px; resize: none; font-family: var(--font-chinese);">${text}</textarea>
                <p style="margin-top: 15px; font-size: 14px; opacity: 0.7;">请复制上述内容分享给朋友</p>
            </div>
        </div>
    `;
    document.body.appendChild(shareModal);
    shareModal.style.display = 'block';
}

// 显示提示消息
function showToast(message) {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: var(--primary-color);
        color: white;
        padding: 15px 25px;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 500;
        z-index: 2000;
        box-shadow: 0 4px 16px rgba(0, 160, 235, 0.3);
        font-family: var(--font-chinese);
        text-align: center;
        max-width: 80%;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    
    // 动画显示
    toast.style.opacity = '0';
    toast.style.transform = 'translate(-50%, -50%) scale(0.8)';
    setTimeout(() => {
        toast.style.transition = 'all 0.3s ease-out';
        toast.style.opacity = '1';
        toast.style.transform = 'translate(-50%, -50%) scale(1)';
    }, 10);
    
    // 自动消失
    setTimeout(() => {
        toast.style.transition = 'all 0.3s ease-in';
        toast.style.opacity = '0';
        toast.style.transform = 'translate(-50%, -50%) scale(0.8)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 2000);
}

// 创建飘落的花朵效果
function createFloatingFlowers() {
    const flowers = ['🌺', '🌸', '🌼', '🌻', '🌷'];
    const container = document.querySelector('.container');
    
    for (let i = 0; i < 15; i++) {
        setTimeout(() => {
            const flower = document.createElement('div');
            flower.textContent = flowers[Math.floor(Math.random() * flowers.length)];
            flower.style.cssText = `
                position: fixed;
                font-size: 24px;
                pointer-events: none;
                z-index: 1500;
                left: ${Math.random() * window.innerWidth}px;
                top: -50px;
                animation: floatDown 3s linear forwards;
            `;
            
            document.body.appendChild(flower);
            
            // 清理元素
            setTimeout(() => {
                if (flower.parentNode) {
                    flower.parentNode.removeChild(flower);
                }
            }, 3000);
        }, i * 200);
    }
}

// 添加飘落动画样式
if (!document.querySelector('#floatDownStyle')) {
    const style = document.createElement('style');
    style.id = 'floatDownStyle';
    style.textContent = `
        @keyframes floatDown {
            0% {
                transform: translateY(-50px) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(${window.innerHeight + 50}px) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// 初始化装饰动画
function initDecorations() {
    // 为二维码添加扫描线效果
    const qrContainer = document.querySelector('.qr-placeholder');
    if (qrContainer) {
        const scanLine = document.createElement('div');
        scanLine.style.cssText = `
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--primary-color), transparent);
            animation: scan 2s infinite;
        `;
        qrContainer.appendChild(scanLine);
        
        // 添加扫描动画
        if (!document.querySelector('#scanStyle')) {
            const scanStyle = document.createElement('style');
            scanStyle.id = 'scanStyle';
            scanStyle.textContent = `
                @keyframes scan {
                    0% { transform: translateY(0); opacity: 1; }
                    50% { opacity: 0.7; }
                    100% { transform: translateY(156px); opacity: 1; }
                }
            `;
            document.head.appendChild(scanStyle);
        }
    }
}

// 添加触摸反馈
function addTouchFeedback() {
    const buttons = document.querySelectorAll('button, .qr-container');
    
    buttons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('touchend', function() {
            this.style.transform = 'scale(1)';
        });
        
        button.addEventListener('touchcancel', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// 点击二维码的处理
document.addEventListener('DOMContentLoaded', function() {
    const qrContainer = document.querySelector('.qr-container');
    if (qrContainer) {
        qrContainer.addEventListener('click', function() {
            showToast('请使用微信扫描二维码领取奖励');
            
            // 添加点击效果
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
});

// 防止页面被意外刷新
window.addEventListener('beforeunload', function(e) {
    // 在生产环境中可以移除这个警告
    // e.preventDefault();
    // e.returnValue = '';
});

// 页面可见性变化处理
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // 页面隐藏时暂停动画
        document.body.style.animationPlayState = 'paused';
    } else {
        // 页面显示时恢复动画
        document.body.style.animationPlayState = 'running';
    }
});

// 错误处理
window.addEventListener('error', function(e) {
    console.error('页面错误:', e.error);
    // 在生产环境中可以发送错误报告
});

// 性能监控（可选）
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            console.log('页面加载时间:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
        }, 0);
    });
}