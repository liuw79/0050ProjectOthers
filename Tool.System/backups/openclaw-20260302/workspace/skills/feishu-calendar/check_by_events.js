const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

// 检查是否有其他方式查询忙闲
// 尝试直接查日历事件来推断忙闲状态

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

async function checkByEvents() {
    // 通过查询共享日历中的事件来间接获取忙闲信息
    const calendarId = 'feishu.cn_XPhMNlWBS0qz08CnYIrb0g@group.calendar.feishu.cn';
    const startTs = Math.floor(new Date('2026-02-24T00:00:00').getTime() / 1000);
    const endTs = Math.floor(new Date('2026-02-24T23:59:59').getTime() / 1000);
    
    console.log('查询共享日历 2026-02-24 的事件...\n');
    
    try {
        const res = await client.request({
            method: 'GET',
            url: `/open-apis/calendar/v4/calendars/${encodeURIComponent(calendarId)}/events`,
            params: {
                start_time: String(startTs),
                end_time: String(endTs)
            }
        });
        
        if (res.code === 0 && res.data.items) {
            console.log('✅ 找到的事件:');
            res.data.items.forEach(evt => {
                if (evt.status !== 'cancelled') {
                    const start = new Date(parseInt(evt.start_time.timestamp) * 1000).toLocaleString('zh-CN');
                    const end = new Date(parseInt(evt.end_time.timestamp) * 1000).toLocaleString('zh-CN');
                    console.log(`📅 ${evt.summary}`);
                    console.log(`   ${start} - ${end}`);
                    if (evt.attendees) {
                        console.log(`   参与者: ${evt.attendees.map(a => a.display_name).join(', ')}`);
                    }
                }
            });
        } else {
            console.log('无事件或查询失败');
        }
    } catch (e) {
        console.error('❌ 失败:', e.message);
    }
}

checkByEvents();
