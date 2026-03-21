const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

async function renameCalendar() {
    const calendarId = 'feishu.cn_XPhMNlWBS0qz08CnYIrb0g@group.calendar.feishu.cn';

    const res = await client.request({
        method: 'PATCH',
        url: `/open-apis/calendar/v4/calendars/${encodeURIComponent(calendarId)}`,
        data: {
            summary: '刘伟(openclaw)'
        }
    });

    console.log('Response:', JSON.stringify(res.data, null, 2));
}

renameCalendar();
