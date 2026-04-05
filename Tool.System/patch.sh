cat /Users/liuwei/SynologyDrive/claude-config/settings.json > /tmp/settings.json
node -e 'const fs=require("fs");let data=JSON.parse(fs.readFileSync("/tmp/settings.json","utf8"));data.env.ANTHROPIC_AUTH_TOKEN="aff9f130dc5c475ea3ebfe42cf1c5fca.IH6YqpihLtS7nhJX";data.env.ANTHROPIC_BASE_URL="https://open.bigmodel.cn/api/anthropic";data.env.API_TIMEOUT_MS="3000000";data.env.CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1";fs.writeFileSync("/tmp/settings.json",JSON.stringify(data,null,2));'
cat /tmp/settings.json > /Users/liuwei/SynologyDrive/claude-config/settings.json
