# 项目Alpha - 编码规范与开发标准

## 目录

1. [Java项目规范](#1-java项目规范)
2. [注释规范](#2-注释规范)
3. [接口文档规范](#3-接口文档规范)
4. [数据库规范](#4-数据库规范)

---

## 1. Java项目规范

### 1.1 版本要求
- **Java版本**: 使用 Java 8 (JDK 1.8)

### 1.2 命名规范
- **类名**: 使用 PascalCase（大驼峰命名法）
  - 示例: `UserService`, `TicketRepository`
- **方法名**: 使用 camelCase（小驼峰命名法）
  - 示例: `createTicket()`, `findById()`
- **变量名**: 使用 camelCase
  - 示例: `ticketName`, `currentPage`
- **常量**: 全大写，单词间用下划线分隔
  - 示例: `MAX_PAGE_SIZE`, `DEFAULT_TIMEOUT`

### 1.3 代码风格
- **不可变性**: 优先使用不可变对象和 `final` 关键字
  - 使用 `final class` 声明不可变类
  - 使用 `final` 修饰字段和方法参数
- **Lombok**: 使用 Lombok 注解自动生成 getter/setter/构造函数
  - `@Data`: 生成所有字段的 getter/setter、toString、equals、hashCode
  - `@Builder`: 生成构建器模式
  - `@AllArgsConstructor`: 生成全参构造函数
  - `@NoArgsConstructor`: 生成无参构造函数

### 1.4 异常处理
- **异常具体化**: 避免捕获通用 `Exception`，使用具体的异常类型
- **异常信息**: 抛出或记录有意义的异常信息，便于问题定位
- **日志记录**: 使用 SLF4J 进行日志记录，禁止使用 `System.out`

### 1.5 依赖注入
- **框架**: 使用 Spring Framework 进行依赖注入
- **注入方式**: 偏好构造器注入（Constructor Injection），避免字段注入
  - 推荐: `@Autowired` + 构造函数
  - 避免: 字段上直接使用 `@Autowired`

### 1.6 单元测试
- **测试框架**: 使用 JUnit 5 + Mockito
- **测试覆盖率**: 每个业务类都应有对应的测试类
- **测试命名**: 测试方法名应清晰描述测试场景
  - 示例: `testCreateTicket_Success()`, `testFindById_NotFound()`

---

## 2. 注释规范

### 2.1 注释要求
- **语言**: 所有注释使用中文
- **完整性**: 所有 `public` 方法必须包含完整的 Javadoc 注释
- **Javadoc 结构**:
  - `@param`: 描述方法参数
  - `@return`: 描述返回值
  - `@throws`: 描述抛出的异常

### 2.2 注释示例
```java
/**
 * 创建工单
 * 
 * @param ticketCreate 工单创建请求对象
 * @return 创建成功的工单实体
 * @throws IllegalArgumentException 当工单名称为空时抛出
 * @throws DataAccessException 当数据库操作失败时抛出
 */
public Ticket createTicket(TicketCreate ticketCreate) {
    // 实现代码
}
```

### 2.3 特殊注释
- **TODO**: 使用 `// TODO: 待实现` 标记待完成的功能
- **FIXME**: 使用 `// FIXME: 需要修复` 标记需要修复的问题
- **NOTE**: 使用 `// NOTE: 说明` 标记重要的业务说明

---

## 3. 接口文档规范

### 3.1 文档格式
- **输出格式**: 同时输出 Markdown (.md) 和 Word (.docx) 两种格式
- **存储位置**: 所有接口文档存放在 `docs/` 目录下

### 3.2 文档内容要求
每个接口必须包含以下内容：

| 内容项 | 说明 |
| :--- | :--- |
| **接口路径** | API 的完整路径 |
| **HTTP方法** | GET/POST/PUT/DELETE/PATCH |
| **功能描述** | 接口的业务功能说明 |
| **请求参数** | 参数名、类型、是否必填、说明 |
| **请求示例** | 完整的请求体示例（JSON格式） |
| **成功响应** | 响应状态码、响应体示例 |
| **失败响应** | 错误状态码、错误信息示例 |

### 3.3 文档结构
```
docs/
├── api-documentation.md          # API接口文档（Markdown格式）
├── api-documentation.docx        # API接口文档（Word格式）
└── swagger/                      # Swagger/OpenAPI 相关文件（可选）
```

---

## 4. 数据库规范

### 4.1 DDL脚本
- **存储位置**: `sql/schema.sql`
- **内容**: 包含所有表的创建语句（CREATE TABLE）
- **格式**: 每个表定义前添加注释说明表用途

### 4.2 初始数据脚本
- **存储位置**: `sql/data.sql`
- **内容**: 包含有意义的初始测试数据（INSERT语句）
- **数量**: 至少生成 50 条工单数据

### 4.3 表设计原则
- **命名**: 表名使用小写字母，单词间用下划线分隔
  - 示例: `tickets`, `tags`, `ticket_tags`
- **主键**: 使用自增主键（SERIAL/BIGSERIAL）
- **外键**: 建立适当的外键约束，设置级联删除策略
- **索引**: 为常用查询字段创建索引，提升查询性能

### 4.4 SQL脚本示例

**schema.sql**:
```sql
-- 工单表 - 存储工单信息
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引: 提高名称搜索性能
CREATE INDEX idx_tickets_name ON tickets(name);
```

**data.sql**:
```sql
-- 插入测试工单数据
INSERT INTO tickets (name, description, status) VALUES 
('修复登录页面验证码问题', '用户反馈验证码无法正常显示', 'pending'),
('优化首页加载速度', '首页加载时间超过3秒', 'pending');
```

---

## 附录：目录结构规范

```
project-alpha/
├── backend/                      # 后端代码
│   ├── src/
│   │   └── main/
│   │       ├── java/             # Java源码
│   │       └── resources/        # 配置文件
│   ├── test/                     # 测试代码
│   └── pom.xml                   # Maven配置
├── frontend/                     # 前端代码
├── docs/                         # 文档目录
│   └── api-documentation.md      # API文档
├── sql/                          # SQL脚本
│   ├── schema.sql                # 表结构DDL
│   └── data.sql                  # 初始数据
└── README.md                     # 项目说明
```

---

**版本**: 1.0  
**创建日期**: 2024-01-01  
**适用项目**: Project Alpha - Ticket标签分类和管理工具
