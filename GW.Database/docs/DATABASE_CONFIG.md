# GW.Database - 数据库配置指南

本项目通过 `main.py` 文件中的硬编码变量来配置数据库连接。在实际生产环境中，强烈建议使用环境变量或更安全的配置管理方案来管理敏感信息。

## 数据库连接参数

请在 `main.py` 文件中找到以下变量，并根据您的 SQL Server 数据库信息进行修改：

```python
# --- Database Configuration ---
DB_DRIVER_PATH = "/usr/local/opt/freetds/lib/libtdsodbc.so" # FreeTDS 驱动的完整路径
DB_HOST = "47.115.38.118"                                  # 数据库服务器的 IP 地址或域名
DB_PORT = "9024"                                           # 数据库服务器的端口 (SQL Server 默认 1433)
DB_USER = "gw_reader"                                      # 数据库用户名
DB_PASSWORD = "cZ1cM5nX5eX7"                               # 数据库密码
DB_NAME = "GW_Course"                                      # 要连接的数据库名称

os.environ['ODBCINSTINI'] = '/usr/local/etc/odbcinst.ini' # ODBC 驱动配置文件路径

# Connection string
DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST},{DB_PORT}/{DB_NAME}?driver={DB_DRIVER_PATH}"
```

### 变量说明

-   `DB_DRIVER_PATH`: FreeTDS ODBC 驱动的完整路径。请确保此路径指向您系统中实际安装的 `libtdsodbc.so` 文件。通常在 `/usr/local/opt/freetds/lib/` 目录下。
-   `DB_HOST`: 您的 SQL Server 数据库服务器的 IP 地址或域名。
-   `DB_PORT`: 您的 SQL Server 数据库服务器监听的端口。默认情况下是 `1433`，但您的配置是 `9024`。
-   `DB_USER`: 用于连接数据库的用户名。
-   `DB_PASSWORD`: 对应用户名的密码。
-   `DB_NAME`: 您希望连接并内省的数据库名称。
-   `os.environ['ODBCINSTINI']`: 指向 `odbcinst.ini` 文件的路径。这个文件告诉 `pyodbc` 哪里可以找到 ODBC 驱动的配置。我们已将其设置为 `/usr/local/etc/odbcinst.ini`。

## 安全提示

**请注意，将数据库凭据硬编码在代码中存在安全风险。** 对于生产环境或共享代码库，强烈建议使用以下方法来管理敏感信息：

-   **环境变量**: 将 `DB_USER`, `DB_PASSWORD` 等作为环境变量设置在您的操作系统或部署环境中。
-   **.env 文件**: 使用 `python-dotenv` 等库从 `.env` 文件中加载环境变量，并将 `.env` 文件添加到 `.gitignore` 中，避免其被提交到版本控制。
-   **密钥管理服务**: 对于更复杂的应用，可以考虑使用云服务提供商的密钥管理服务（如 AWS Secrets Manager, Azure Key Vault）。

本项目为了简化演示和快速启动，采用了硬编码方式。在您实际使用时，请务必根据您的安全要求进行调整。
