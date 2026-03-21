const Lark = require('@larksuiteoapi/node-sdk');
require('dotenv').config({ path: require('path').resolve(__dirname, '../../.env') });

const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
});

async function addAttendee() {
    const calendarId = 'feishu.cn_XPhMNlWBS0qz08CnYIrb0g@group.calendar.feishu.cn';
    const eventId = '79f82173-e1b7-4378-a02a-5baacb473d07_0';
    const userOpenId = 'ou_b89c76c98db6919ae2dacdc44d876209';

    console.log('Adding attendee to event...');
    
    try {
        const res = await client.request({
            method: 'POST',
            url: `/open-apis/calendar/v4/calendars/${encodeURIComponent(calendarId)}/events/${eventId}/attendees?user_id_type=open_id`,
            data: {
                attendees: [{
                    type: 'user',
                    user_id: userOpenId
                }],
                need_notification: true
            }
        });

        console.log('Response:', JSON.stringify(res, null, 2));
    } catch (e) {
        console.error('Error:', e.message);
    }
}

addAttendee();
