# DataEase SQLBot AI智能问数测试指南

## 测试环境信息
- **系统地址**: http://localhost:8080
- **数据库**: GW_Course (PostgreSQL)
- **AI模型**: Kimi K2 (kimi-k2-0711-preview)
- **API提供商**: 月之暗面 (Moonshot AI)

## 测试用例

### 1. 基础查询测试
测试AI是否能理解简单的自然语言查询：

**测试输入**:
```
显示所有课程信息
```

**期望SQL**:
```sql
SELECT * FROM courses;
```

### 2. 条件查询测试
测试AI是否能处理带条件的查询：

**测试输入**:
```
查找课程名称包含"数据"的课程
```

**期望SQL**:
```sql
SELECT * FROM courses WHERE course_name LIKE '%数据%';
```

### 3. 聚合查询测试
测试AI是否能处理统计类查询：

**测试输入**:
```
统计每个专业的课程数量
```

**期望SQL**:
```sql
SELECT major, COUNT(*) as course_count FROM courses GROUP BY major;
```

### 4. 关联查询测试
测试AI是否能处理多表关联：

**测试输入**:
```
显示学生选课信息，包括学生姓名和课程名称
```

**期望SQL**:
```sql
SELECT s.student_name, c.course_name 
FROM students s 
JOIN enrollments e ON s.student_id = e.student_id 
JOIN courses c ON e.course_id = c.course_id;
```

### 5. 复杂查询测试
测试AI处理复杂业务逻辑的能力：

**测试输入**:
```
查找选课人数超过50人的热门课程
```

**期望SQL**:
```sql
SELECT c.course_name, COUNT(e.student_id) as enrollment_count
FROM courses c
JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name
HAVING COUNT(e.student_id) > 50
ORDER BY enrollment_count DESC;
```

## 测试步骤

1. **访问系统**: 打开浏览器访问 http://localhost:8080
2. **登录系统**: 使用管理员账号登录
3. **进入问数模块**: 点击"智能问数"或相关功能入口
4. **输入测试查询**: 依次输入上述测试用例
5. **验证结果**: 检查生成的SQL是否正确，执行结果是否符合预期

## 验证要点

### AI模型配置验证
- [ ] 系统能正常调用Kimi K2 API
- [ ] API密钥配置正确
- [ ] 模型响应正常

### 查询生成验证
- [ ] 自然语言理解准确
- [ ] SQL语法正确
- [ ] 表名和字段名匹配数据库schema
- [ ] 查询逻辑符合业务需求

### 结果展示验证
- [ ] 查询结果正确显示
- [ ] 数据格式友好
- [ ] 错误处理得当

## 故障排除

### 常见问题
1. **AI不响应**: 检查API密钥和网络连接
2. **SQL语法错误**: 检查数据库schema配置
3. **查询结果为空**: 验证数据库中是否有测试数据
4. **性能问题**: 检查数据库连接和索引

### 日志查看
```bash
# 查看容器日志
docker logs dataease-sqlbot

# 查看详细日志
docker logs -f dataease-sqlbot
```

## 成功标准
- ✅ 所有测试用例都能正确生成SQL
- ✅ 查询结果准确无误
- ✅ 系统响应时间合理（<5秒）
- ✅ 错误处理机制正常工作