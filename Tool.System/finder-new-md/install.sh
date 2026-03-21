#!/bin/bash

# Finder 右键新建 Markdown 文件功能安装脚本
# 自动创建 Automator 快速操作

set -e

echo "========================================="
echo "  Finder 右键新建 MD 文件 - 安装程序"
echo "========================================="
echo ""

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCRIPT_PATH="${SCRIPT_DIR}/create_new_md.sh"

# 确保脚本有执行权限
chmod +x "$SCRIPT_PATH"

# Automator 工作流保存路径
WORKFLOW_DIR="$HOME/Library/Services"
WORKFLOW_NAME="新建 Markdown 文件.workflow"
WORKFLOW_PATH="${WORKFLOW_DIR}/${WORKFLOW_NAME}"

echo "📝 步骤 1: 检查环境..."
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ 错误: 找不到 create_new_md.sh 脚本"
    exit 1
fi
echo "✅ 脚本文件存在"

echo ""
echo "📝 步骤 2: 创建 Automator 快速操作..."

# 创建服务目录（如果不存在）
mkdir -p "$WORKFLOW_DIR"

# 创建 workflow 目录结构
mkdir -p "$WORKFLOW_PATH/Contents"

# 创建 Info.plist
cat > "$WORKFLOW_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>NSServices</key>
	<array>
		<dict>
			<key>NSBackgroundColorName</key>
			<string>background</string>
			<key>NSIconName</key>
			<string>NSTouchBarCompose</string>
			<key>NSMenuItem</key>
			<dict>
				<key>default</key>
				<string>新建 Markdown 文件</string>
			</dict>
			<key>NSMessage</key>
			<string>runWorkflowAsService</string>
			<key>NSRequiredContext</key>
			<dict>
				<key>NSApplicationIdentifier</key>
				<string>com.apple.finder</string>
			</dict>
			<key>NSSendTypes</key>
			<array>
				<string>public.item</string>
			</array>
		</dict>
	</array>
	<key>CFBundleIdentifier</key>
	<string>com.apple.automator.新建 Markdown 文件</string>
	<key>CFBundleName</key>
	<string>新建 Markdown 文件</string>
	<key>CFBundleShortVersionString</key>
	<string>1.0</string>
	<key>CFBundleVersion</key>
	<string>1.0</string>
</dict>
</plist>
EOF

# 创建 document.wflow
cat > "$WORKFLOW_PATH/Contents/document.wflow" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AMApplicationBuild</key>
	<string>521.1</string>
	<key>AMApplicationVersion</key>
	<string>2.10</string>
	<key>AMDocumentVersion</key>
	<string>2</string>
	<key>actions</key>
	<array>
		<dict>
			<key>action</key>
			<dict>
				<key>AMAccepts</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Optional</key>
					<true/>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.path</string>
					</array>
				</dict>
				<key>AMActionVersion</key>
				<string>2.1.1</string>
				<key>AMApplication</key>
				<array>
					<string>Automator</string>
				</array>
				<key>AMParameterProperties</key>
				<dict>
					<key>COMMAND_STRING</key>
					<dict/>
					<key>inputMethod</key>
					<dict/>
					<key>shell</key>
					<dict/>
					<key>source</key>
					<dict/>
				</dict>
				<key>AMProvides</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.path</string>
					</array>
				</dict>
				<key>ActionBundlePath</key>
				<string>/System/Library/Automator/Run Shell Script.action</string>
				<key>ActionName</key>
				<string>运行 Shell 脚本</string>
				<key>ActionParameters</key>
				<dict>
					<key>COMMAND_STRING</key>
					<string>"$SCRIPT_PATH" "\$@"</string>
					<key>inputMethod</key>
					<integer>1</integer>
					<key>shell</key>
					<string>/bin/bash</string>
					<key>source</key>
					<string></string>
				</dict>
				<key>BundleIdentifier</key>
				<string>com.apple.RunShellScript</string>
				<key>CFBundleVersion</key>
				<string>2.1.1</string>
				<key>CanShowSelectedItemsWhenRun</key>
				<false/>
				<key>CanShowWhenRun</key>
				<true/>
				<key>Category</key>
				<array>
					<string>AMCategoryUtilities</string>
				</array>
				<key>Class Name</key>
				<string>RunShellScriptAction</string>
				<key>InputUUID</key>
				<string>12345678-1234-1234-1234-123456789012</string>
				<key>Keywords</key>
				<array>
					<string>Shell</string>
					<string>脚本</string>
					<string>命令</string>
					<string>运行</string>
					<string>Unix</string>
				</array>
				<key>OutputUUID</key>
				<string>12345678-1234-1234-1234-123456789013</string>
				<key>UUID</key>
				<string>12345678-1234-1234-1234-123456789014</string>
				<key>UnlocalizedApplications</key>
				<array>
					<string>Automator</string>
				</array>
				<key>arguments</key>
				<dict>
					<key>0</key>
					<dict>
						<key>default value</key>
						<integer>0</integer>
						<key>name</key>
						<string>inputMethod</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>0</string>
					</dict>
					<key>1</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>source</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>1</string>
					</dict>
					<key>2</key>
					<dict>
						<key>default value</key>
						<false/>
						<key>name</key>
						<string>CheckedForUserDefaultShell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>2</string>
					</dict>
					<key>3</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>COMMAND_STRING</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>3</string>
					</dict>
					<key>4</key>
					<dict>
						<key>default value</key>
						<string>/bin/sh</string>
						<key>name</key>
						<string>shell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>4</string>
					</dict>
				</dict>
				<key>isViewVisible</key>
				<integer>1</integer>
				<key>location</key>
				<string>449.500000:316.000000</string>
				<key>nibPath</key>
				<string>/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib</string>
			</dict>
			<key>isViewVisible</key>
			<integer>1</integer>
		</dict>
	</array>
	<key>connectors</key>
	<dict/>
	<key>workflowMetaData</key>
	<dict>
		<key>serviceApplicationBundleID</key>
		<string>com.apple.finder</string>
		<key>serviceApplicationPath</key>
		<string>/System/Library/CoreServices/Finder.app</string>
		<key>serviceInputTypeIdentifier</key>
		<string>com.apple.Automator.fileSystemObject</string>
		<key>serviceOutputTypeIdentifier</key>
		<string>com.apple.Automator.nothing</string>
		<key>serviceProcessesInput</key>
		<integer>0</integer>
		<key>workflowTypeIdentifier</key>
		<string>com.apple.Automator.servicesMenu</string>
	</dict>
</dict>
</plist>
EOF

echo "✅ Automator 快速操作已创建"

echo ""
echo "📝 步骤 3: 刷新系统服务..."
# 重建服务缓存（不同 macOS 版本命令可能不同）
/System/Library/CoreServices/pbs -flush 2>/dev/null || true
# 触摸文件以强制重新加载
touch "$WORKFLOW_PATH"
# 可选：重启 Finder 使更改立即生效
sleep 1

echo "✅ 系统服务已刷新"

echo ""
echo "========================================="
echo "  ✅ 安装完成！"
echo "========================================="
echo ""
echo "使用方法："
echo "1. 在 Finder 中，在任意文件夹空白处右键点击"
echo "2. 或者选中一个文件夹后右键点击"
echo "3. 选择「快速操作」→「新建 Markdown 文件」"
echo ""
echo "💡 提示："
echo "- 新文件会自动创建在当前目录"
echo "- 创建后会自动进入重命名模式"
echo "- 可以通过系统偏好设置自定义快捷键"
echo ""
echo "设置快捷键："
echo "「系统偏好设置」→「键盘」→「快捷键」→「服务」"
echo "→ 找到「新建 Markdown 文件」并设置快捷键"
echo ""
