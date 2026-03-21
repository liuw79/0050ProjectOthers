const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

async function testFreeBusy() {
    // 测试只查一个人
    const timeMin = '2026-02-24T00:00:00Z';
    const timeMax = '2026-02-24T23:59:59Z';
    
    console.log('测试单用户忙闲查询...\n');
    
    try {
        const res = await client.request({
            method: 'POST',
            url: '/open-apis/calendar/v4/freebusy/list',
            data: {
                time_min: timeMin,
                time_max: timeMax,
                user_id_type: 'open_id',
                attendees: [
                    { type: 'user', user_id: 'ou_b89c76c98db6919ae2dacdc44d876209' }
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

testFreeBusy();
