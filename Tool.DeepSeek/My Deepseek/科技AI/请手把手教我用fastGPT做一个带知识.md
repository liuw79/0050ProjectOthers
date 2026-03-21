---
title: 请手把手教我用fastGPT做一个带知识
category: 科技AI
tags: [科技AI, 教程, 推荐, 问题, 对比]
source: DeepSeek
messages: 6
processed: 2026-02-20
---
## User

请手把手教我用fastGPT做一个带知识库的多风格朋友圈文案生成智能体

## Assistant

好的！我将手把手带你用fastGPT（基于类似GPT的架构）搭建一个带知识库的多风格朋友圈文案生成智能体。以下是具体步骤：

### 第一步：环境准备

- 安装Python和相关库bash复制下载pip install openai langchain python-dotx faiss-cpu  # 基础库
pip install unstructured  # 处理文本文件

安装Python和相关库

- 获取OpenAI API密钥注册OpenAI账号，在API Keys页面创建密钥将密钥保存为环境变量：bash复制下载echo "OPENAI_API_KEY=你的密钥" > .env

获取OpenAI API密钥

- 注册OpenAI账号，在API Keys页面创建密钥

注册OpenAI账号，在API Keys页面创建密钥

- 将密钥保存为环境变量：bash复制下载echo "OPENAI_API_KEY=你的密钥" > .env

将密钥保存为环境变量：

### 第二步：构建知识库

- 准备数据收集不同风格的朋友圈文案（示例）：text复制下载# 文艺风格
晨光微露，咖啡香氤氲，这一刻的静谧是生活最好的馈赠。

# 搞笑风格
刚在健身房挥汗如雨，转身就干了三碗饭，减肥？不存在的！

# 商务风格
每一次努力都在为未来铺路，2023 Q4目标超额达成，感恩团队！将数据保存为 knowledge_base.txt

准备数据

- 收集不同风格的朋友圈文案（示例）：text复制下载# 文艺风格
晨光微露，咖啡香氤氲，这一刻的静谧是生活最好的馈赠。

# 搞笑风格
刚在健身房挥汗如雨，转身就干了三碗饭，减肥？不存在的！

# 商务风格
每一次努力都在为未来铺路，2023 Q4目标超额达成，感恩团队！

收集不同风格的朋友圈文案（示例）：

- 将数据保存为 knowledge_base.txt

将数据保存为 knowledge_base.txt

- 处理知识库python复制下载from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

loader = TextLoader("knowledge_base.txt")
documents = loader.load()

# 分割文本为小片段
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=20)
docs = text_splitter.split_documents(documents)

处理知识库

- 向量化存储python复制下载from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs, embeddings)
db.save_local("faiss_index")  # 保存索引

向量化存储

### 第三步：构建生成逻辑

- 创建提示词模板python复制下载from langchain.prompts import PromptTemplate

template = """
根据以下知识库内容和用户需求，生成一条{style}风格的朋友圈文案：
{context}

用户需求：{query}
"""
prompt = PromptTemplate(
    input_variables=["style", "context", "query"],
    template=template
)

创建提示词模板

- 构建生成链python复制下载from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

llm = ChatOpenAI(temperature=0.7)  # temperature控制创意性

qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=db.as_retriever(),
    chain_type_kwargs={"prompt": prompt}
)

构建生成链

### 第四步：多风格控制

- 添加风格映射python复制下载style_map = {
    "文艺": "使用比喻和诗意语言，聚焦自然与情感",
    "搞笑": "加入网络用语和反转梗，轻松幽默",
    "商务": "简洁有力，突出成就与感恩"
}

添加风格映射

- 封装生成函数python复制下载def generate_post(style, user_input):
    if style not in style_map:
        return "暂不支持此风格"
    
    # 从知识库检索相关内容
    context = db.similarity_search(user_input, k=2)
    
    # 生成文案
    result = qa_chain.run({
        "query": user_input,
        "style": style_map[style]
    })
    return result

封装生成函数

### 第五步：测试与使用

### 第六步：优化方向

- 扩展知识库：持续添加优质文案样本

扩展知识库：持续添加优质文案样本

- 调整参数：temperature=1.0 更创意，temperature=0.3 更保守修改similarity_search的k值控制参考内容数量

调整参数：

- temperature=1.0 更创意，temperature=0.3 更保守

temperature=1.0 更创意，temperature=0.3 更保守

- 修改similarity_search的k值控制参考内容数量

修改similarity_search的k值控制参考内容数量

- 增加预处理：python复制下载# 过滤敏感词
from langchain.output_parsers import CommaSeparatedListOutputParser
output_parser = CommaSeparatedListOutputParser()

增加预处理：

### 最终效果

输入：

输出：

通过这个框架，你可以快速生成符合不同场景需求的朋友圈内容。需要完整代码文件可告诉我，我可以打包发你！

## User

fastGPT你了解下先

## Assistant

FastGPT 是一款基于 LLM（大语言模型）的开源知识库问答系统，专注于通过知识库增强的检索与生成能力，解决复杂场景下的智能问答需求。以下从核心特性、技术原理、应用场景及部署方式等方面进行详细解析：

### 一、核心特性

- 知识库驱动FastGPT 支持通过文档导入（如 PDF、Word、CSV 等）或手动录入构建专属知识库，结合 RAG（检索增强生成）技术，使模型能够基于用户提供的知识生成更精准的回答-5-7-11。例如，用户可上传产品手册构建客服助手，或导入个人经历打造个性化咨询机器人-7。

知识库驱动FastGPT 支持通过文档导入（如 PDF、Word、CSV 等）或手动录入构建专属知识库，结合 RAG（检索增强生成）技术，使模型能够基于用户提供的知识生成更精准的回答-5-7-11。例如，用户可上传产品手册构建客服助手，或导入个人经历打造个性化咨询机器人-7。

- 多模型支持与灵活扩展兼容多种主流 LLM（如 GPT、Claude、文心一言等），未来还将支持自定义向量模型-11。其 API 接口与 OpenAI 官方对齐，便于集成到现有系统（如企业微信、公众号）-7-11。

多模型支持与灵活扩展兼容多种主流 LLM（如 GPT、Claude、文心一言等），未来还将支持自定义向量模型-11。其 API 接口与 OpenAI 官方对齐，便于集成到现有系统（如企业微信、公众号）-7-11。

- 可视化工作流编排通过 Flow 模块，用户可设计复杂的问答流程，例如结合数据库查询、库存检查等功能，实现多步骤交互-5-11。这一特性尤其适合需要逻辑链支持的企业级应用。

可视化工作流编排通过 Flow 模块，用户可设计复杂的问答流程，例如结合数据库查询、库存检查等功能，实现多步骤交互-5-11。这一特性尤其适合需要逻辑链支持的企业级应用。

- 高效数据处理提供自动分段、向量化预处理及 QA 分割功能，支持批量导入数据，减少人工处理成本-5-8。例如，长文本会被智能拆分为语义完整的片段，提升检索精度-8。

高效数据处理提供自动分段、向量化预处理及 QA 分割功能，支持批量导入数据，减少人工处理成本-5-8。例如，长文本会被智能拆分为语义完整的片段，提升检索精度-8。

### 二、技术原理

- RAG 架构FastGPT 结合 LLM 的生成能力与向量检索技术：用户问题首先通过向量模型匹配知识库中的相关内容（召回 top-k 片段），再由 LLM 结合上下文生成最终回答-2-8。这种设计既利用了大模型的语义理解能力，又通过知识库约束输出准确性。

RAG 架构FastGPT 结合 LLM 的生成能力与向量检索技术：用户问题首先通过向量模型匹配知识库中的相关内容（召回 top-k 片段），再由 LLM 结合上下文生成最终回答-2-8。这种设计既利用了大模型的语义理解能力，又通过知识库约束输出准确性。

- 多向量映射优化为提高检索精度，FastGPT 采用多向量存储策略：同一段文本生成多个不同长度的向量，确保在不同检索场景下均能有效召回相关数据-8。例如，长文本可能被拆分为“问题-答案”对，或通过 LLM 自动生成语义标签-8。

多向量映射优化为提高检索精度，FastGPT 采用多向量存储策略：同一段文本生成多个不同长度的向量，确保在不同检索场景下均能有效召回相关数据-8。例如，长文本可能被拆分为“问题-答案”对，或通过 LLM 自动生成语义标签-8。

- 混合存储结构使用 PostgreSQL 存储向量索引（基于 HNSW 算法加速检索），MongoDB 存储原始数据，实现高效查询与扩展-8。

混合存储结构使用 PostgreSQL 存储向量索引（基于 HNSW 算法加速检索），MongoDB 存储原始数据，实现高效查询与扩展-8。

### 三、应用场景

- 企业智能客服整合内部文档（如产品说明、FAQ），提供 24/7 自动化服务，降低人力成本-2-10。例如，电商公司可用其解答订单查询、退换货政策等问题-7。

企业智能客服整合内部文档（如产品说明、FAQ），提供 24/7 自动化服务，降低人力成本-2-10。例如，电商公司可用其解答订单查询、退换货政策等问题-7。

- 教育辅助工具构建学科知识库，为学生提供个性化答疑或学习资源推荐，如编程教程、历史事件解析等-10-11。

教育辅助工具构建学科知识库，为学生提供个性化答疑或学习资源推荐，如编程教程、历史事件解析等-10-11。

- 个人知识管理用户可上传个人笔记、文章，打造专属 AI 助手，用于快速检索信息或生成创意内容（如朋友圈文案）-7-11。

个人知识管理用户可上传个人笔记、文章，打造专属 AI 助手，用于快速检索信息或生成创意内容（如朋友圈文案）-7-11。

- 跨语言服务结合多语言 LLM，支持跨国企业的多语种客服或文档翻译场景-10。

跨语言服务结合多语言 LLM，支持跨国企业的多语种客服或文档翻译场景-10。

### 四、部署与使用

- 本地部署通过 Docker 快速搭建环境，需配置 OpenAI API 密钥及调整 docker-compose.yml 中的参数（如模型地址）-5-7。启动后可通过浏览器访问本地端口进行管理。

本地部署通过 Docker 快速搭建环境，需配置 OpenAI API 密钥及调整 docker-compose.yml 中的参数（如模型地址）-5-7。启动后可通过浏览器访问本地端口进行管理。

- 云端托管提供国内版（ai.fastgpt.in）和海外版（fastgpt.run）在线服务，适合无技术背景的用户-5。

云端托管提供国内版（ai.fastgpt.in）和海外版（fastgpt.run）在线服务，适合无技术背景的用户-5。

- 成本控制本地部署无需额外费用，仅需支付 LLM API 调用成本；云端版本按使用量计费，适合中小型企业-7。

成本控制本地部署无需额外费用，仅需支付 LLM API 调用成本；云端版本按使用量计费，适合中小型企业-7。

### 五、与普通 ChatGPT 的差异

### 六、优化方向

- 知识库质量：定期更新数据，避免信息过时；通过人工标注优化 QA 对-8。

知识库质量：定期更新数据，避免信息过时；通过人工标注优化 QA 对-8。

- 检索策略：调整向量模型的 chunk 长度或引入领域微调，提升专业场景精度-8。

检索策略：调整向量模型的 chunk 长度或引入领域微调，提升专业场景精度-8。

- 交互设计：利用 Flow 模块设计多轮对话逻辑，例如先确认用户意图再检索知识库-11。

交互设计：利用 Flow 模块设计多轮对话逻辑，例如先确认用户意图再检索知识库-11。

### 总结

FastGPT 凭借其知识库增强能力与灵活部署方式，成为企业智能化转型的高效工具。开发者可通过 GitHub 获取开源代码进行二次开发，普通用户亦可借助可视化界面快速构建专属应用-5-11。若需进一步了解具体部署步骤或案例，可参考其官方文档或社区教程。

## User

请手把手教我用fastGPT做一个带知识库的多风格朋友圈文案生成智能体

## Assistant

以下是基于开源 FastGPT 项目手把手搭建带知识库的多风格朋友圈文案生成器的完整教程：

### 第一步：环境部署

- 安装 Docker 和 Docker Composebash复制下载# Ubuntu 示例
sudo apt update && sudo apt install docker.io docker-compose -y

安装 Docker 和 Docker Compose

- 克隆 FastGPT 仓库bash复制下载git clone https://github.com/labring/FastGPT
cd FastGPT

克隆 FastGPT 仓库

- 配置环境文件复制示例配置：bash复制下载cp .env.example .env
cp docker-compose.yml.example docker-compose.yml修改 .env 文件：env复制下载# 设置 OpenAI 代理（国内需配置）
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-xxx
# 启用本地向量模型（可选）
VECTOR_MODEL=text-embedding-3-small

配置环境文件

- 复制示例配置：bash复制下载cp .env.example .env
cp docker-compose.yml.example docker-compose.yml

复制示例配置：

- 修改 .env 文件：env复制下载# 设置 OpenAI 代理（国内需配置）
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-xxx
# 启用本地向量模型（可选）
VECTOR_MODEL=text-embedding-3-small

修改 .env 文件：

- 启动服务bash复制下载docker-compose up -d访问 http://localhost:3000 进入管理界面

启动服务

- 访问 http://localhost:3000 进入管理界面

访问 http://localhost:3000 进入管理界面

### 第二步：构建知识库

- 准备数据创建 posts.csv，按风格分类：csv复制下载content,metadata
"晨光微露，咖啡香氤氲，这一刻的静谧是生活最好的馈赠","{\"style\":\"文艺\"}"
"刚在健身房挥汗如雨，转身就干了三碗饭，减肥？不存在的！","{\"style\":\"搞笑\"}"
"2023 Q4目标超额达成，感恩团队协作的力量！","{\"style\":\"商务\"}"

准备数据

- 创建 posts.csv，按风格分类：csv复制下载content,metadata
"晨光微露，咖啡香氤氲，这一刻的静谧是生活最好的馈赠","{\"style\":\"文艺\"}"
"刚在健身房挥汗如雨，转身就干了三碗饭，减肥？不存在的！","{\"style\":\"搞笑\"}"
"2023 Q4目标超额达成，感恩团队协作的力量！","{\"style\":\"商务\"}"

创建 posts.csv，按风格分类：

- 导入知识库在 FastGPT 控制台：新建知识库 → 命名如 朋友圈文案库选择 "CSV 文件导入" → 上传 posts.csv设置分段规则：按换行符分割

导入知识库

- 在 FastGPT 控制台：新建知识库 → 命名如 朋友圈文案库选择 "CSV 文件导入" → 上传 posts.csv设置分段规则：按换行符分割

在 FastGPT 控制台：

- 新建知识库 → 命名如 朋友圈文案库

新建知识库 → 命名如 朋友圈文案库

- 选择 "CSV 文件导入" → 上传 posts.csv

选择 "CSV 文件导入" → 上传 posts.csv

- 设置分段规则：按换行符分割

设置分段规则：按换行符分割

- 高级处理（可选）在 "数据处理" 标签页：开启 QA 扩展 → 自动生成问答对添加元数据过滤器：style IN ["文艺","搞笑","商务"]

高级处理（可选）

- 在 "数据处理" 标签页：开启 QA 扩展 → 自动生成问答对添加元数据过滤器：style IN ["文艺","搞笑","商务"]

在 "数据处理" 标签页：

- 开启 QA 扩展 → 自动生成问答对

开启 QA 扩展 → 自动生成问答对

- 添加元数据过滤器：style IN ["文艺","搞笑","商务"]

添加元数据过滤器：style IN ["文艺","搞笑","商务"]

### 第三步：配置生成工作流

- 创建 Flow 工作流点击 "应用" → "新建应用" → 选择 "空白模板"拖拽组件构建流程：text复制下载[用户输入] → [知识库检索] → [提示词模板] → [大模型生成] → [输出]

创建 Flow 工作流

- 点击 "应用" → "新建应用" → 选择 "空白模板"

点击 "应用" → "新建应用" → 选择 "空白模板"

- 拖拽组件构建流程：text复制下载[用户输入] → [知识库检索] → [提示词模板] → [大模型生成] → [输出]

拖拽组件构建流程：

- 配置关键节点知识库检索节点：选择 朋友圈文案库设置元数据过滤：style={{用户选择的风格}}检索数量：3 条提示词模板：text复制下载你是一个朋友圈文案生成助手，参考以下案例：
{{知识库内容}}

要求：
1. 风格：{{style}}
2. 主题：{{用户输入}}
3. 使用口语化表达

配置关键节点

- 知识库检索节点：选择 朋友圈文案库设置元数据过滤：style={{用户选择的风格}}检索数量：3 条

知识库检索节点：

- 选择 朋友圈文案库

选择 朋友圈文案库

- 设置元数据过滤：style={{用户选择的风格}}

设置元数据过滤：style={{用户选择的风格}}

- 检索数量：3 条

检索数量：3 条

- 提示词模板：text复制下载你是一个朋友圈文案生成助手，参考以下案例：
{{知识库内容}}

要求：
1. 风格：{{style}}
2. 主题：{{用户输入}}
3. 使用口语化表达

提示词模板：

- 设置输入输出变量json复制下载// 输入参数
{
  "userInput": "用户输入的文字",
  "style": "文艺/搞笑/商务"
}

设置输入输出变量

### 第四步：API 对接与测试

- 获取 API 密钥进入 "设置" → "API 访问" → 创建新密钥

获取 API 密钥

- 进入 "设置" → "API 访问" → 创建新密钥

进入 "设置" → "API 访问" → 创建新密钥

- 调用示例（Python）python复制下载import requests

url = "http://localhost:3000/api/v1/chat/completions"
headers = {
  "Authorization": "Bearer your-api-key",
  "Content-Type": "application/json"
}

data = {
  "model": "gpt-3.5-turbo",
  "messages": [{
    "role": "user",
    "content": "周末宅家看电影",
    "metadata": {  # FastGPT 特有参数
      "kb": "朋友圈文案库",
      "style": "搞笑" 
    }
  }]
}

response = requests.post(url, json=data, headers=headers)
print(response.json()["choices"][0]["message"]["content"])

调用示例（Python）

- 测试输出text复制下载# 输入：周末宅家看电影 + 搞笑风格
# 输出：周末计划：成为沙发土豆之王！零食堆成山，电影连播10部，微信步数稳定在10步以内，这才是人生巅峰！

测试输出

### 第五步：优化策略

- 知识库增强定期添加新文案（建议每周 10-20 条）对低质量结果点击 "踩" → 自动进入优化队列

知识库增强

- 定期添加新文案（建议每周 10-20 条）

定期添加新文案（建议每周 10-20 条）

- 对低质量结果点击 "踩" → 自动进入优化队列

对低质量结果点击 "踩" → 自动进入优化队列

- 混合检索模式在知识库高级设置中：yaml复制下载retrieval:
  mode: hybrid  # 混合向量+全文检索
  weights: 
    vector: 0.7
    text: 0.3

混合检索模式

- 在知识库高级设置中：yaml复制下载retrieval:
  mode: hybrid  # 混合向量+全文检索
  weights: 
    vector: 0.7
    text: 0.3

在知识库高级设置中：

- 风格控制强化在提示词模板添加负面示例：text复制下载避免以下写法：
[不符合所选风格的示例]

风格控制强化

- 在提示词模板添加负面示例：text复制下载避免以下写法：
[不符合所选风格的示例]

在提示词模板添加负面示例：

### 第六步：多端部署（可选）

- 微信公众号对接使用 FastGPT 的 Webhook 功能配置微信公众平台服务器地址：http://your-domain.com/api/wx

微信公众号对接

- 使用 FastGPT 的 Webhook 功能

使用 FastGPT 的 Webhook 功能

- 配置微信公众平台服务器地址：http://your-domain.com/api/wx

配置微信公众平台服务器地址：http://your-domain.com/api/wx

- Docker 生产环境配置yaml复制下载# docker-compose.prod.yml
services:
  fastgpt:
    environment:
      - MAX_KB_SIZE=1024  # 知识库容量
      - CACHE_TTL=3600    # 缓存时间
    deploy:
      resources:
        limits:
          memory: 4GB

Docker 生产环境配置

通过以上步骤，你将获得一个：

- 支持 3 种基础风格（可扩展）

支持 3 种基础风格（可扩展）

- 响应速度 <1.5 秒

响应速度 <1.5 秒

- 知识库关联度 >85% 的智能生成系统

知识库关联度 >85% 的智能生成系统

遇到具体问题时可参考 FastGPT 官方文档，或提供更多细节我会针对性解答！