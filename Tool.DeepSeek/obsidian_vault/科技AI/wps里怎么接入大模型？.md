---
title: wps里怎么接入大模型？
category: 科技AI
tags: [科技AI, 教程, 推荐]
source: DeepSeek
messages: 2
processed: 2026-02-20
---
## User

wps里怎么接入大模型？

## Assistant

在 WPS Office 中接入大模型（如 GPT、文心一言等）可以通过以下两种方式实现，具体取决于你的需求和技术能力：

### 一、使用 WPS 官方内置的 AI 功能（推荐普通用户）

WPS 已推出 WPS AI 功能（集成文心大模型等），提供智能写作、表格分析、PPT 生成等功能，无需自行接入。操作步骤：

- 升级 WPS 至最新版本（需企业版或会员权限，部分功能在公测中）。

升级 WPS 至最新版本（需企业版或会员权限，部分功能在公测中）。

- 打开文档/表格/PPT，点击工具栏中的 「WPS AI」 按钮（或「智能助手」）。

打开文档/表格/PPT，点击工具栏中的 「WPS AI」 按钮（或「智能助手」）。

- 直接输入指令，如「生成工作总结」「分析数据趋势」等，AI 会自动处理。

直接输入指令，如「生成工作总结」「分析数据趋势」等，AI 会自动处理。

### 二、自行接入外部大模型（开发者或高级用户）

若需接入第三方大模型（如 OpenAI、Claude 等），需通过 WPS 开放平台 开发插件，调用 API 实现。

步骤示例：

- 注册大模型 API例如 OpenAI: 注册账号并获取 API Key。国内模型（文心一言、讯飞星火等）：申请企业接入权限。

注册大模型 API

- 例如 OpenAI: 注册账号并获取 API Key。

例如 OpenAI: 注册账号并获取 API Key。

- 国内模型（文心一言、讯飞星火等）：申请企业接入权限。

国内模型（文心一言、讯飞星火等）：申请企业接入权限。

- 开发 WPS 插件使用 WPS 开放平台 的 JSAPI 创建插件。示例代码（调用 OpenAI）：javascript复制下载// 在插件中发送用户输入到 OpenAI
async function generateText(userInput) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: userInput }]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content;
}

// 将 AI 返回内容插入文档
function insertTextToWPS(text) {
  Application.ActiveDocument.Range().Text = text;
}

开发 WPS 插件

- 使用 WPS 开放平台 的 JSAPI 创建插件。

使用 WPS 开放平台 的 JSAPI 创建插件。

- 示例代码（调用 OpenAI）：javascript复制下载// 在插件中发送用户输入到 OpenAI
async function generateText(userInput) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: userInput }]
    })
  });
  const data = await response.json();
  return data.choices[0].message.content;
}

// 将 AI 返回内容插入文档
function insertTextToWPS(text) {
  Application.ActiveDocument.Range().Text = text;
}

示例代码（调用 OpenAI）：

- 部署插件将插件打包发布到 WPS 应用商店，或本地加载测试。

部署插件

- 将插件打包发布到 WPS 应用商店，或本地加载测试。

将插件打包发布到 WPS 应用商店，或本地加载测试。

### 三、注意事项

- 网络权限：确保 WPS 可访问外部 API（企业环境可能需要配置代理）。

网络权限：确保 WPS 可访问外部 API（企业环境可能需要配置代理）。

- 数据安全：传输敏感数据时需加密，遵守《个人信息保护法》。

数据安全：传输敏感数据时需加密，遵守《个人信息保护法》。

- 成本控制：大模型 API 调用按量计费，需监控用量。

成本控制：大模型 API 调用按量计费，需监控用量。

### 四、替代方案

- 浏览器插件：安装 ChatGPT 等浏览器扩展，在 WPS 网页版中通过侧边栏调用。

浏览器插件：安装 ChatGPT 等浏览器扩展，在 WPS 网页版中通过侧边栏调用。

- 本地模型：部署本地化大模型（如 Llama、ChatGLM），通过局域网 API 接入 WPS。

本地模型：部署本地化大模型（如 Llama、ChatGLM），通过局域网 API 接入 WPS。

如需具体代码示例或进一步指导，可参考 WPS 开放平台文档 或说明你的使用场景。