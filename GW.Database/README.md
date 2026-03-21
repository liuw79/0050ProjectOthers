# GW.Database - 数据库结构查看器

## 项目简介

GW.Database 是一个基于 FastAPI 构建的轻量级 Web 服务，旨在帮助您快速查看和理解远程 SQL Server 数据库的结构。通过自动内省数据库模式，并提供交互式的 API 文档，本工具极大地简化了数据库结构的可视化和查询过程，为后续项目开发提供清晰的参考。

## 主要功能

-   **数据库模式内省**: 自动连接到 SQL Server 数据库，并提取所有表及其列的详细信息（名称、类型、是否可空、主键等）。
-   **交互式 API 文档**: 通过 Swagger UI 自动生成 API 文档，您可以在浏览器中直接测试 API 端点，查询数据库结构。
-   **易于部署**: 基于 Python 和 FastAPI，部署简单快捷。

## 快速启动

1.  **确保已安装 FreeTDS ODBC 驱动**:
    本工具依赖 FreeTDS ODBC 驱动来连接 SQL Server。请确保您的 macOS 系统已正确安装并配置了 FreeTDS。
    *   **安装 FreeTDS**: 如果尚未安装，请通过 Homebrew 安装：
        ```bash
        brew install freetds
        ```
    *   **配置 odbcinst.ini**: 确保 `/usr/local/etc/odbcinst.ini` 文件中包含 FreeTDS 的正确配置，并且驱动路径指向您当前安装的 FreeTDS 版本（例如 `/usr/local/Cellar/freetds/1.5.4/lib/libtdsodbc.so`）。

2.  **克隆项目**:
    ```bash
    git clone <项目仓库地址> # 替换为实际的项目仓库地址
    cd GW.Database
    ```

3.  **创建并激活 Python 虚拟环境**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4.  **安装依赖**:
    ```bash
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
    ```
    （注意：`requirements.txt` 文件将在后续步骤中创建）

5.  **配置数据库连接**:
    编辑 `main.py` 文件，更新以下数据库连接信息：
    ```python
    DB_HOST = "您的数据库主机IP或域名"
    DB_PORT = "您的数据库端口"
    DB_USER = "您的数据库用户名"
    DB_PASSWORD = "您的数据库密码"
    DB_NAME = "您要连接的数据库名称"
    ```
    同时，确保 `DB_DRIVER_PATH` 指向正确的 FreeTDS 驱动路径。

6.  **启动服务**:
    ```bash
    source .venv/bin/activate
    python main.py
    ```
    服务将在 `http://127.0.0.1:8001` 启动。

7.  **访问 API 文档**:
    在浏览器中打开 `http://127.0.0.1:8001/docs`，即可查看交互式 API 文档。

## API 端点

-   **GET /**: 检查 API 和数据库连接状态。
-   **GET /schema**: 获取数据库中所有表的列表。
-   **GET /tables/{table_name}**: 获取指定表的详细结构（包括列名、类型、是否可空、主键等）。

## 贡献

欢迎对本项目进行贡献。如果您有任何建议或发现 Bug，请提交 Issue 或 Pull Request。

## 许可证

本项目采用 MIT 许可证。
