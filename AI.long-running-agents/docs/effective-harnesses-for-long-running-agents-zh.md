# 长运行代理的有效管理框架

随着 AI 代理变得越来越强大，开发者越来越多地要求它们承担需要跨数小时甚至数天工作的复杂任务。然而，让代理在多个上下文窗口中持续取得进展仍然是一个未解决的问题。

长运行代理的核心挑战在于，它们必须以离散的会话形式工作，每个新会话开始时都没有之前的记忆。想象一个由轮班工程师组成的软件项目，每个新工程师到来时都没有关于上一班发生了什么的记忆。由于上下文窗口有限，而且大多数复杂项目无法在单个窗口内完成，代理需要一种方法来弥合编码会话之间的差距。

我们开发了一种双重解决方案，使 Claude Agent SDK 能够在多个上下文窗口中有效工作：一个**初始化代理**在首次运行时设置环境，一个**编码代理**在每个会话中负责取得增量进度，同时为下一个会话留下清晰的人工制品。你可以在配套的快速入门指南中找到代码示例。

## 长运行代理的问题

Claude Agent SDK 是一个强大、通用的代理管理框架，擅长编码以及其他需要模型使用工具来收集上下文、规划和执行的任务。它具有上下文管理功能，如压缩，使代理能够在不耗尽上下文窗口的情况下处理任务。理论上，有了这样的设置，代理应该能够持续进行有用的工作任意长时间。

然而，压缩是不够的。开箱即用，即使像 Opus 4.5 这样的前沿编码模型在 Claude Agent SDK 上跨多个上下文窗口循环运行，如果只给出一个高级提示，如"构建 claude.ai 的克隆"，也无法构建出生产质量的 Web 应用程序。

Claude 的失败表现为两种模式。首先，代理倾向于试图一次做太多——基本上是一次性完成应用程序。通常，这导致模型在实现过程中耗尽上下文，使下一个会话开始时功能半实现且未记录。然后，代理必须猜测发生了什么，并花费大量时间试图让基本应用程序重新工作。即使有压缩也会发生这种情况，因为压缩并不总是向下一个代理传递完美的清晰指令。

第二种失败模式通常发生在项目的后期。在已经构建了一些功能之后，后续的代理实例会环顾四周，看到已取得的进展，并宣布工作完成。

这将问题分解为两个部分。首先，我们需要设置一个初始环境，为给定提示要求的所有功能奠定基础，这使代理能够一步步、一个功能接一个功能地工作。其次，我们应该提示每个代理朝着其目标取得增量进度，同时在会话结束时保持环境处于清洁状态。所谓"清洁状态"，我们指的是适合合并到主分支的那种代码：没有重大错误，代码有序且有良好文档，总体上，开发者可以轻松地开始开发新功能，而不必先清理无关的混乱。

在内部实验中，我们使用两部分解决方案解决了这些问题：

1. 初始化代理：第一个代理会话使用一个专门的提示，要求模型设置初始环境：一个 `init.sh` 脚本、一个记录代理所做工作的 claude-progress.txt 文件，以及一个显示添加了哪些文件的初始 git commit。
2. 编码代理：每个后续会话要求模型取得增量进度，然后留下结构化更新。

这里的关键见解是找到一种方法，让代理在以新的上下文窗口开始时快速了解工作状态，这是通过 claude-progress.txt 文件连同 git 历史记录来实现的。这些实践的灵感来自于了解高效的软件工程师每天所做的工作。

## 环境管理

在更新的 Claude 4 提示指南中，我们分享了一些多上下文窗口工作流程的最佳实践，包括一个使用"在第一个上下文窗口使用不同的提示"的管理框架结构。这个"不同的提示"要求初始化代理设置环境，为未来的编码代理提供有效工作所需的所有必要上下文。在这里，我们深入探讨此类环境的一些关键组件。

### 功能列表

为了解决代理一次性完成应用程序或过早认为项目完成的问题，我们提示初始化代理编写一个全面的功能需求文件，扩展用户的初始提示。在 claude.ai 克隆示例中，这意味着超过 200 个功能，例如"用户可以打开新对话，输入查询，按回车键，并看到 AI 响应"。这些功能最初都标记为"失败"，以便后来的编码代理对完整功能的外观有清晰的概述。

```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
}
```

我们提示编码代理只通过更改 passes 字段的状态来编辑此文件，并且我们使用强力的指令，如"删除或编辑测试是不可接受的，因为这可能导致功能缺失或有错误"。经过一些实验，我们决定使用 JSON，因为模型比 Markdown 文件更不可能不适当地更改或覆盖 JSON 文件。

### 增量进度

有了这个初始环境框架，编码代理的下一个迭代被要求一次只处理一个功能。这种增量方法被证明是解决代理一次做太多问题的关键。

一旦进行增量工作，模型在代码更改后仍需要保持环境处于清洁状态是必不可少的。在我们的实验中，我们发现引发这种行为的最​​好方法是要求模型通过描述性的提交消息将进度提交到 git，并在进度文件中写入其进度的摘要。这使模型能够使用 git 撤销错误的代码更改并恢复代码库的工作状态。

这些方法还提高了效率，因为它们消除了代理必须猜测发生了什么并花费时间试图让基本应用程序重新工作的需要。

### 测试

我们观察到的最后一个主要失败模式是 Claude 倾向于在没有适当测试的情况下将功能标记为完成。在没有明确提示的情况下，Claude 倾向于进行代码更改，甚至使用单元测试或针对开发服务器的 `curl` 命令进行测试，但无法识别该功能没有端到端地工作。

在构建 Web 应用程序的情况下，一旦明确提示使用浏览器自动化工具并像人类用户那样进行所有测试，Claude 在端到端地验证功能方面做得很好。

[图片：Claude 通过 Puppeteer MCP 服务器测试 claude.ai 克隆时拍摄的屏幕截图。]

为 Claude 提供这些类型的测试工具显著提高了性能，因为代理能够识别和修复仅从代码中看不清楚的错误。

仍然存在一些问题，例如 Claude 的视觉能力和浏览器自动化工具的限制使得识别每种类型的错误变得困难。例如，Claude 无法通过 Puppeteer MCP 看到浏览器原生警报模态框，并且依赖这些模态框的功能往往会更错误。

## 了解情况

有了上述所有内容，每个编码代理都被提示通过一系列步骤来了解情况，有些非常基本但仍然有帮助：

1. _运行 `pwd` 查看你正在工作的目录。你只能编辑此目录中的文件。_
2. _阅读 git 日志和进度文件，以了解最近的工作。_
3. _阅读功能列表文件并选择尚未完成的最高优先级功能来处理。_

这种方法在每个会话中为 Claude 节省了一些令牌，因为它不必弄清楚如何测试代码。它还有助于要求初始化代理编写一个可以运行开发服务器的 init.sh 脚本，然后在实现新功能之前运行基本的端到端测试。

在 claude.ai 克隆的情况下，这意味着代理总是启动本地开发服务器并使用 Puppeteer MCP 开始新对话、发送消息和接收响应。这确保了 Claude 可以快速识别应用程序是否处于损坏状态，并立即修复任何现有错误。如果代理改为开始实现新功能，很可能会使问题变得更糟。

鉴于所有这些，典型的会话以以下助手消息开始：

```
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.
<Starts work on a new feature>
```

## 代理失败模式和解决方案

| __问题__ | __初始化代理行为__ | __编码代理行为__ |
| --- | --- | --- |
| Claude 过早宣布在整个项目上取得胜利。 | 设置功能列表文件：根据输入规范，设置一个包含端到端功能描述的结构化 JSON 文件。 | 在会话开始时阅读功能列表文件。选择一个功能开始工作。 |
| Claude 留下有错误或未记录进度的环境。 | 编写一个初始 git 仓库和进度记录文件。 | 在会话开始时阅读进度记录文件和 git 提交日志，并在开发服务器上运行基本测试以捕获任何未记录的错误。在会话结束时编写 git 提交和进度更新。 |
| Claude 过早将功能标记为完成。 | 设置功能列表文件。 | 自我验证所有功能。仅在仔细测试后将功能标记为"通过"。 |
| Claude 必须花时间弄清楚如何运行应用程序。 | 编写一个可以运行开发服务器的 `init.sh` 脚本。 | 在会话开始时阅读 `init.sh`。 |

## 未来工作

这项研究展示了一个在长运行代理管理框架中使模型能够在多个上下文窗口中取得增量进度的一组可能的解决方案。然而，仍然存在未解决的问题。

最值得注意的是，目前还不清楚单个、通用的编码代理是否在各种情况下表现最好，或者是否可以通过多代理架构实现更好的性能。似乎合理的专用代理，如测试代理、质量保证代理或代码清理代理，可以在软件开发生命周期的子任务中做得更好。

此外，此演示针对全栈 Web 应用程序开发进行了优化。未来的一个方向是将这些发现推广到其他领域。很可能可以将其中一些或所有教训应用于例如科学研究或金融建模所需的长运行代理任务。

### 致谢

由 Justin Young 撰写。特别感谢 David Hershey、Prithvi Rajasakeran、Jeremy Hadfield、Naia Bouscal、Michael Tingley、Jesse Mu、Jake Eaton、Marius Buleandara、Maggie Vo、Pedram Navid、Nadine Yasser 和 Alex Notov 的贡献。

这项工作反映了 Anthropic 多个团队的集体努力，他们使 Claude 能够安全地进行长视野自主软件工程，尤其是代码 RL 和 Claude Code 团队。有兴趣做出贡献的候选人欢迎申请 anthropic.com/careers。

### 脚注

1. 我们在这种情况下将它们称为单独的代理，只是因为它们有不同的初始用户提示。系统提示、工具集和整体代理管理框架在其他方面是相同的。
