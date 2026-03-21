const Lark = require("@larksuiteoapi/node-sdk");
const fs = require("fs");

const config = JSON.parse(fs.readFileSync("/Users/liuwei/.openclaw/feishu-accounts.json", "utf8"));
const account = config.accounts[0];

const client = new Lark.Client({
  appId: account.appId,
  appSecret: account.appSecret,
  appType: Lark.AppType.SelfBuild,
  domain: Lark.Domain.Feishu,
});

async function main() {
  const allUsers = [];
  const departments = [
    {id: "od-cfe4b93cda2b3d1d3d7b82e39a35ca9f", name: "神助攻小组"},
    {id: "od-e46c8f89d112fded5dda45b73b4a59ee", name: "产品规划与策略圈"},
    {id: "od-2eb785edbed1eadef5142923d04ba7b7", name: "KA经营圈"},
    {id: "od-1f992c5f8e78bbd15c44a08e9a978677", name: "战略经营课题圈"},
    {id: "od-a32f7d8b62a95f39b5c0988c3e26f9f4", name: "华南经营圈"},
    {id: "od-28113bdef90976a8308128ed4e05770e", name: "AI加速圈"},
    {id: "od-e1cec5d9136a48b9f6cbca0ba948861c", name: "效能圈"},
    {id: "od-aa4ec7c4487b7b6d427143d2343b5da6", name: "PMO圈"},
    {id: "od-f7eec4aca9c054049d91297342d643f2", name: "业务突破课题圈"},
    {id: "od-cd7c9778f83431cf2746f47fde6ec57f", name: "组织人才课题圈"},
    {id: "od-5265ede673608cd90a12f6c4b5fdd281", name: "华东经营圈"},
    {id: "od-6c552b14b7b39b1c8afcc91a83627833", name: "师资服务圈"},
    {id: "od-8cc316df713db0a3598b0c34323979b7", name: "小老师孵化圈"},
    {id: "od-6e347fc2f080c87558490af58cda4823", name: "华北经营圈"},
    {id: "od-eacfb99e33491bcd6cffd175afde1198", name: "餐饮经营圈"},
    {id: "od-d5e48569ed511fb14a19e04fd3d08ce2", name: "内容圈"},
    {id: "od-ef8587c1e5598d471c65c3613804ff78", name: "LMI课题圈"},
    {id: "od-e3448d8a796f663926e9f25059dd5c6a", name: "公开课运营圈"},
    {id: "od-984a15aae207badd2b520ed89bded9f3", name: "企业会员运营圈"},
    {id: "od-aed0c3f6dc12ea528c939c5dfa9811c9", name: "会员及公开课运营圈"},
    {id: "od-542760dae14058d5b7668f97ba8eff0a", name: "企业服务圈"},
    {id: "od-75f463a70c59a73fa6a4356eb555979b", name: "创始人经营圈"}
  ];

  for (const dept of departments) {
    try {
      const resp = await client.contact.user.list({
        params: { department_id: dept.id, department_id_type: "open_department_id", page_size: 50 }
      });
      if (resp.code === 0 && resp.data && resp.data.items) {
        for (const u of resp.data.items) {
          allUsers.push({
            name: u.name,
            email: u.email,
            dept: dept.name,
            open_id: u.open_id
          });
        }
      }
    } catch (e) {
      console.error(dept.name, e.message);
    }
  }
  
  // 去重
  const seen = new Set();
  const unique = [];
  for (const u of allUsers) {
    if (!seen.has(u.email)) {
      seen.add(u.email);
      unique.push(u);
    }
  }
  
  // 按姓名排序
  unique.sort((a, b) => a.name.localeCompare(b.name, "zh"));
  
  console.log(JSON.stringify(unique, null, 2));
}
main();
