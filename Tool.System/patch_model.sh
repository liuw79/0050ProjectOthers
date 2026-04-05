cat /Users/liuwei/SynologyDrive/claude-config/settings.json > /tmp/settings.json
node -e 'const fs=require("fs");let data=JSON.parse(fs.readFileSync("/tmp/settings.json","utf8"));data.env.ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-5.1";data.env.ANTHROPIC_DEFAULT_SONNET_MODEL="glm-5.1";data.env.ANTHROPIC_DEFAULT_OPUS_MODEL="glm-5.1";fs.writeFileSync("/tmp/settings.json",JSON.stringify(data,null,2));'
cat /tmp/settings.json > /Users/liuwei/SynologyDrive/claude-config/settings.json
cat /Users/liuwei/SynologyDrive/claude-config/settings.json | grep -i glm
