const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

async function checkEvent() {
    const calendarId = 'feishu.cn_Ci9T1kqXRtbwS3RWmTRbGe@group.calendar.feishu.cn';

    const res = await client.request({
        method: 'GET',
        url: `/open-apis/calendar/v4/calendars/${encodeURIComponent(calendarId)}/events?user_id_type=open_id&start_time=${Math.floor(Date.now()/1000)}&end_time=${Math.floor(Date.now()/1000) + 86400*7}`,
    });

    console.log('Response code:', res.code);
    console.log('Response:', JSON.stringify(res.data.items[0], null, 2));
}

checkEvent();
