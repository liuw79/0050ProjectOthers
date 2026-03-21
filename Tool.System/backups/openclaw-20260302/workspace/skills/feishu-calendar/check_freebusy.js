const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

// 转换为UTC时间的RFC3339格式
function toRFC3339(date) {
    return date.toISOString(); // 2026-02-24T00:00:00.000Z
}

async function checkFreeBusy() {
    // 后天 2026-02-24 的 UTC 时间
    const startTime = new Date('2026-02-24T00:00:00+08:00'); // 北京时间0点
    const endTime = new Date('2026-02-24T23:59:59+08:00');   // 北京时间23:59
    
    const timeMin = toRFC3339(startTime);
    const timeMax = toRFC3339(endTime);
    
    console.log('TimeMin:', timeMin);
    console.log('TimeMax:', timeMax);
    console.log('查询中...\n');
    
    try {
        const res = await client.request({
            method: 'POST',
            url: '/open-apis/calendar/v4/freebusy/list',
            data: {
                time_min: timeMin,
                time_max: timeMax,
                user_id_type: 'open_id',
                attendees: [
                    { type: 'user', user_id: 'ou_b89c76c98db6919ae2dacdc44d876209' },
                    { type: 'user', user_id: 'ou_a928326cc83b6bdb6933eae35d9ea9bb' },
                    { type: 'user', user_id: 'ou_8a097536f4b66556175931c91110ae95' }
                ]
            }
        });
        
        console.log('✅ 成功！');
        console.log(JSON.stringify(res.data, null, 2));
    } catch (e) {
        console.error('❌ 失败:', e.message);
        if (e.response && e.response.data) {
            console.error('错误详情:', JSON.stringify(e.response.data, null, 2));
        }
    }
}

checkFreeBusy();
