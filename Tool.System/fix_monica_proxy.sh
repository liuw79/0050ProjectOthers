#!/bin/bash

# 定义要修改的 Clash Verge Rev 配置文件路径
CONFIG_DIR="$HOME/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles"

# 我们需要修改这四个远程订阅对应的预处理脚本
FILES=(
  "$CONFIG_DIR/sN4VU0RLLAXi.js"
  "$CONFIG_DIR/s0i1Fs888kSc.js"
  "$CONFIG_DIR/scF3IyyrQnDc.js"
  "$CONFIG_DIR/sb1Dl9lemYLB.js"
)

# 生成新的脚本内容
SCRIPT_CONTENT='// Define main function (script entry)
function main(config, profileName) {
  if (!config.rules) config.rules = [];
  
  let mainGroup = "PROXY";
  if (config["proxy-groups"] && config["proxy-groups"].length > 0) {
    mainGroup = config["proxy-groups"][0].name;
  }
  
  config.rules.unshift(
    "DOMAIN-SUFFIX,monica.im," + mainGroup,
    "DOMAIN-SUFFIX,monica.io," + mainGroup,
    "DOMAIN-SUFFIX,api.monica.im," + mainGroup,
    "DOMAIN-KEYWORD,monica," + mainGroup
  );
  
  return config;
}
'

echo "开始为 Clash Verge 注入 Monica 代理规则..."

for FILE in "${FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "$SCRIPT_CONTENT" > "$FILE"
    echo "✅ 已更新配置: $(basename "$FILE")"
  else
    echo "⚠️ 未找到文件: $(basename "$FILE")"
  fi
done

echo ""
echo "🎉 注入完成！"
echo "请打开 Clash Verge Rev，右键点击你当前的订阅节点，选择【激活 (Use)】或者【刷新】以应用最新规则。"
