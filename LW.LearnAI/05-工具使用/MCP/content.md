# Model Context Protocol (MCP) | 模型上下文协议 (MCP)

> Source: https://docs.anthropic.com/en/docs/agents-and-tools/mcp

---

MCP is an open protocol that standardizes how applications provide context to LLMs. Think of MCP like a **USB-C port for AI applications**. Just as USB-C provides a standardized way to connect your devices to various peripherals and accessories, MCP provides a standardized way to connect AI models to different data sources and tools.

**MCP 是一个开放协议，标准化了应用程序向 LLM 提供上下文的方式。把 MCP 想象成**AI 应用的 USB-C 端口**。就像 USB-C 提供了一种标准化的方式将设备连接到各种外设和配件，MCP 提供了一种标准化的方式将 AI 模型连接到不同的数据源和工具。**

---

## Key Components | 关键组件

### MCP Connector | MCP 连接器

Connect to remote MCP servers directly from the Messages API without building an MCP client. This feature provides seamless integration with MCP-compatible tools and services.

**直接从 Messages API 连接到远程 MCP 服务器，无需构建 MCP 客户端。此功能提供与 MCP 兼容工具和服务的无缝集成。**

### Local MCP | 本地 MCP

Use MCP locally with Claude for Desktop to extend Claude's capabilities on your machine.

**在 Claude Desktop 中本地使用 MCP，扩展 Claude 在你机器上的能力。**

---

## MCP Architecture | MCP 架构

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Claude.ai     │────▶│  MCP Connector  │────▶│  MCP Server     │
│   Claude Code   │     │  (API)          │     │  (Your Service) │
│   API           │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Why MCP? | 为什么选择 MCP？

| Benefit | Description |
|---------|-------------|
| **Standardization** | Single protocol for all AI-data connections |
| **Portability** | Build once, use with any MCP-compatible AI |
| **Security** | Controlled access to data and tools |
| **Flexibility** | Connect to any data source or tool |

| 优势 | 描述 |
|------|------|
| **标准化** | 所有 AI-数据连接的单一协议 |
| **可移植性** | 一次构建，与任何 MCP 兼容的 AI 一起使用 |
| **安全性** | 对数据和工具的受控访问 |
| **灵活性** | 连接到任何数据源或工具 |

---

## MCP Server Types | MCP 服务器类型

1. **Resource Servers** - Provide data (files, databases, APIs)
2. **资源服务器** - 提供数据（文件、数据库、API）

3. **Tool Servers** - Provide actions (execute code, send messages)
4. **工具服务器** - 提供操作（执行代码、发送消息）

5. **Prompt Servers** - Provide templates and prompts
6. **提示服务器** - 提供模板和提示词

---

## Using MCP with Claude | 在 Claude 中使用 MCP

### Claude Desktop

Configure MCP servers in Claude Desktop settings:

**在 Claude Desktop 设置中配置 MCP 服务器：**

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    }
  }
}
```

### Claude Code

```bash
claude mcp add my-server --command "node server.js"
```

### API (MCP Connector) | API (MCP 连接器)

```python
response = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=1024,
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.example.com/sse",
        "name": "my-mcp-server"
    }],
    messages=[...]
)
```

---

## Building MCP Servers | 构建 MCP 服务器

### Basic Structure | 基本结构

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-mcp-server",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

// Define tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "my_tool",
    description: "Tool description",
    inputSchema: {
      type: "object",
      properties: {
        param: { type: "string" }
      }
    }
  }]
}));

// Handle tool execution
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  // Execute tool logic
  return { content: [{ type: "text", text: "Result" }] };
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

---

## Popular MCP Servers | 常用 MCP 服务器

| Server | Description |
|--------|-------------|
| **filesystem** | File system access |
| **postgres** | PostgreSQL database |
| **github** | GitHub API |
| **slack** | Slack integration |
| **google-drive** | Google Drive access |

| 服务器 | 描述 |
|--------|------|
| **filesystem** | 文件系统访问 |
| **postgres** | PostgreSQL 数据库 |
| **github** | GitHub API |
| **slack** | Slack 集成 |
| **google-drive** | Google Drive 访问 |

---

## MCP + Skills

Skills provide the **knowledge layer** on top of MCP's **connectivity layer**:

**Skills 在 MCP 的**连接层**之上提供**知识层**：**

- **MCP**: Connects Claude to your services (Notion, Asana, Linear, etc.)
- **MCP**：将 Claude 连接到你的服务（Notion、Asana、Linear 等）

- **Skills**: Teaches Claude how to use your services effectively
- **Skills**：教导 Claude 如何有效地使用你的服务

Together, they enable users to accomplish complex tasks without figuring out every step.

**两者结合，使用户能够完成复杂任务，而无需弄清楚每一步。**

---

## Resources | 资源

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [Anthropic MCP Guide](https://docs.anthropic.com/en/docs/agents-and-tools/mcp)
- [MCP Connector API](https://docs.anthropic.com/en/docs/agents-and-tools/mcp-connector)
