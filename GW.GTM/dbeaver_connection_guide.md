# DBeaver连接GTM数据库指南

## 连接信息
- **Host**: localhost
- **Port**: 5432
- **Database**: gtm_assistant  ⭐ 重要：不是postgres
- **Username**: comdir
- **Password**: (留空)

## 步骤说明

### 方法1：修改现有连接
1. 在DBeaver左侧连接列表中，右键点击你的PostgreSQL连接
2. 选择"编辑连接"
3. 在"主要"标签页中，找到"数据库"字段
4. 将数据库名从"postgres"改为"gtm_assistant"
5. 点击"测试连接"按钮验证
6. 点击"确定"保存

### 方法2：新建连接
1. 点击DBeaver工具栏的"新建连接"按钮
2. 选择PostgreSQL
3. 填写连接信息：
   - 服务器主机：localhost
   - 端口：5432
   - 数据库：gtm_assistant
   - 用户名：comdir
   - 密码：(留空)
4. 测试连接并保存

## 连接成功后你应该看到：

### 数据库结构：
```
gtm_assistant/
├── Schemas/
│   └── public/
│       ├── Tables/
│       │   ├── users                    (用户表)
│       │   ├── gtm_projects            (GTM项目表)
│       │   ├── gtm_sheets              (GTM工作表)
│       │   ├── sheet_templates         (表格模板)
│       │   ├── sheet_history           (操作历史)
│       │   ├── gtm_action_plans        (行动方案)
│       │   └── project_collaborators   (项目协作者)
│       └── Indexes/
│           ├── idx_gtm_sheets_project
│           ├── idx_gtm_sheets_data
│           └── ...
```

### 示例数据查询：
```sql
-- 查看所有GTM项目
SELECT * FROM gtm_projects;

-- 查看GTM工作表数据
SELECT name, data FROM gtm_sheets;

-- JSON数据查询示例
SELECT data->>'客户群体' as 客户群体 FROM gtm_sheets;
```

## 常见问题

### Q: 连接后看不到gtm_assistant数据库？
A: 确保数据库名字段填写的是"gtm_assistant"而不是"postgres"

### Q: 连接失败？
A: 确认PostgreSQL服务是否启动：
```bash
brew services list | grep postgresql
```

### Q: 权限问题？
A: 使用你的系统用户名(comdir)作为数据库用户名

## 验证连接成功
连接成功后运行这个查询：
```sql
SELECT 'GTM数据库连接成功!' as status, version() as db_version;
```