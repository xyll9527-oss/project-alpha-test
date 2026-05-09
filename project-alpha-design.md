# 项目Alpha - Ticket标签分类和管理工具

## 1. 需求分析

### 1.1 项目背景
本项目旨在构建一个简单易用的Ticket标签分类和管理工具，帮助用户高效管理和追踪任务工单。系统采用前后端分离架构，无需用户认证系统，支持匿名操作。

### 1.2 功能需求清单

| 序号 | 功能模块 | 功能描述 | 需求来源 |
| :--- | :--- | :--- | :--- |
| 1 | Ticket管理 | 创建Ticket | 需求第6点 |
| 2 | Ticket管理 | 删除Ticket | 需求第6点 |
| 3 | Ticket管理 | 编辑Ticket | 需求第6点 |
| 4 | Ticket管理 | 完成Ticket | 需求第6点 |
| 5 | Ticket管理 | 取消完成Ticket | 需求第6点 |
| 6 | 标签管理 | 添加Ticket标签 | 需求第7点 |
| 7 | 标签管理 | 删除Ticket标签 | 需求第7点 |
| 8 | 筛选过滤 | 按标签过滤Ticket | 需求第8点 |
| 9 | 搜索功能 | 按名称搜索Ticket | 需求第9点 |
| 10 | 分页功能 | 支持分页显示，默认10条/页 | 需求第9点 |
| 11 | 分页配置 | 可调整pageSize（10/20/30条/页） | 需求第9点 |

### 1.3 非功能需求

| 类别 | 描述 |
| :--- | :--- |
| 技术栈 | 前端：Vue3 + Element Plus；后端：Python + FastAPI；数据库：PostgreSQL |
| 用户系统 | 无需用户认证系统，所有操作为匿名操作 |
| 性能要求 | 响应时间 < 200ms |
| 兼容性 | 支持主流浏览器（Chrome、Firefox、Safari） |

---

## 2. 技术架构设计

### 2.1 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      前端层 (Vue3 + Element Plus)           │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐   │
│  │ Ticket列表 │  │ Ticket表单 │  │ 标签筛选组件      │   │
│  └──────┬─────┘  └──────┬─────┘  └─────────┬──────────┘   │
│         │                │                  │               │
└─────────┼────────────────┼──────────────────┼───────────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      后端层 (FastAPI)                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐   │
│  │ Ticket API │  │ Tag  API   │  │ 搜索/筛选服务     │   │
│  └──────┬─────┘  └──────┬─────┘  └─────────┬──────────┘   │
│         │                │                  │               │
└─────────┼────────────────┼──────────────────┼───────────────┘
          │                │                  │
          ▼                ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    数据库层 (PostgreSQL)                    │
│              ┌───────────────────────────────┐             │
│              │     tickets  |  tags  | ticket_tags        │ │
│              └───────────────────────────────┘             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 技术选型

| 层次 | 技术 | 版本 | 选型理由 |
| :--- | :--- | :--- | :--- |
| 前端框架 | Vue.js | 3.x | 轻量级、响应式、生态成熟 |
| UI组件库 | Element Plus | 2.x | Vue3官方推荐，组件丰富 |
| 后端框架 | FastAPI | 0.100+ | 高性能、自动文档、类型安全 |
| 数据库 | PostgreSQL | 15+ | 支持复杂查询、JSON类型、全文搜索 |
| ORM | SQLAlchemy | 2.x | Python主流ORM，支持异步 |
| 前端构建 | Vite | 6.x | 快速构建、热更新 |

---

## 3. 数据库设计

### 3.1 实体关系图 (ERD)

```
┌─────────────┐       ┌──────────────────────┐       ┌─────────────┐
│   tickets   │       │    ticket_tags      │       │    tags     │
├─────────────┤       ├──────────────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ ticket_id (FK)      │──────►│ id (PK)     │
│ name        │       │ tag_id (FK)         │       │ name        │
│ description │       └──────────────────────┘       │ color       │
│ status      │                                      └─────────────┘
│ created_at  │
│ updated_at  │
└─────────────┘
```

### 3.2 表结构定义

#### 3.2.1 tickets 表

| 字段名 | 类型 | 约束 | 说明 |
| :--- | :--- | :--- | :--- |
| id | SERIAL | PRIMARY KEY | Ticket唯一标识 |
| name | VARCHAR(255) | NOT NULL | Ticket名称 |
| description | TEXT | NULL | Ticket描述 |
| status | VARCHAR(20) | NOT NULL DEFAULT 'pending' | 状态：pending/completed |
| created_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | NOT NULL DEFAULT CURRENT_TIMESTAMP | 更新时间 |

#### 3.2.2 tags 表

| 字段名 | 类型 | 约束 | 说明 |
| :--- | :--- | :--- | :--- |
| id | SERIAL | PRIMARY KEY | 标签唯一标识 |
| name | VARCHAR(50) | NOT NULL, UNIQUE | 标签名称 |
| color | VARCHAR(7) | NOT NULL DEFAULT '#1f77b4' | 标签颜色（十六进制） |

#### 3.2.3 ticket_tags 表 (关联表)

| 字段名 | 类型 | 约束 | 说明 |
| :--- | :--- | :--- | :--- |
| ticket_id | INTEGER | FOREIGN KEY → tickets(id) | Ticket ID |
| tag_id | INTEGER | FOREIGN KEY → tags(id) | 标签 ID |
| PRIMARY KEY (ticket_id, tag_id) | | | 复合主键 |

---

## 4. API接口设计

### 4.1 Ticket相关接口

| API路径 | HTTP方法 | Controller文件 | 功能描述 |
| :--- | :--- | :--- | :--- |
| /api/tickets | GET | ticket_controller.py | 获取Ticket列表（支持搜索、筛选、分页） |
| /api/tickets/{id} | GET | ticket_controller.py | 获取单个Ticket详情 |
| /api/tickets | POST | ticket_controller.py | 创建新Ticket |
| /api/tickets/{id} | PUT | ticket_controller.py | 更新Ticket信息 |
| /api/tickets/{id} | DELETE | ticket_controller.py | 删除Ticket |
| /api/tickets/{id}/status | PATCH | ticket_controller.py | 更新Ticket状态（完成/取消完成） |

#### 4.1.1 GET /api/tickets - 获取Ticket列表

**请求参数（Query Parameters）：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| search | STRING | 否 | 搜索关键词（匹配name字段） |
| tag_id | INTEGER | 否 | 标签ID（按标签筛选） |
| page | INTEGER | 否 | 页码，默认1 |
| page_size | INTEGER | 否 | 每页数量，默认10（可选10/20/30） |

**成功响应 (200 OK)：**
```json
{
  "data": [
    {
      "id": 1,
      "name": "完成项目文档",
      "description": "编写项目需求和设计文档",
      "status": "completed",
      "created_at": "2024-01-01T10:00:00",
      "updated_at": "2024-01-02T15:30:00",
      "tags": [
        {"id": 1, "name": "文档", "color": "#1f77b4"}
      ]
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 10
}
```

#### 4.1.2 POST /api/tickets - 创建Ticket

**请求体：**
```json
{
  "name": "string (必填，最大255字符)",
  "description": "string (选填)",
  "status": "string (选填，默认pending)",
  "tag_ids": "array[integer] (选填，关联的标签ID列表)"
}
```

**成功响应 (201 Created)：**
```json
{
  "id": 2,
  "name": "新Ticket",
  "description": "描述内容",
  "status": "pending",
  "created_at": "2024-01-03T09:00:00",
  "updated_at": "2024-01-03T09:00:00",
  "tags": []
}
```

#### 4.1.3 PUT /api/tickets/{id} - 更新Ticket

**请求体：**
```json
{
  "name": "string (选填)",
  "description": "string (选填)",
  "status": "string (选填)"
}
```

#### 4.1.4 DELETE /api/tickets/{id} - 删除Ticket

**成功响应 (204 No Content)：** 无响应体

#### 4.1.5 PATCH /api/tickets/{id}/status - 更新状态

**请求体：**
```json
{
  "status": "string (必填，值为 'completed' 或 'pending')"
}
```

### 4.2 Tag相关接口

| API路径 | HTTP方法 | Controller文件 | 功能描述 |
| :--- | :--- | :--- | :--- |
| /api/tags | GET | tag_controller.py | 获取所有标签列表 |
| /api/tags | POST | tag_controller.py | 创建新标签 |
| /api/tags/{id} | DELETE | tag_controller.py | 删除标签 |
| /api/tickets/{ticket_id}/tags/{tag_id} | POST | ticket_controller.py | 为Ticket添加标签 |
| /api/tickets/{ticket_id}/tags/{tag_id} | DELETE | ticket_controller.py | 从Ticket移除标签 |

#### 4.2.1 POST /api/tags - 创建标签

**请求体：**
```json
{
  "name": "string (必填，最大50字符，唯一)",
  "color": "string (选填，十六进制颜色，默认#1f77b4)"
}
```

**成功响应 (201 Created)：**
```json
{
  "id": 3,
  "name": "紧急",
  "color": "#ff4b5c"
}
```

---

## 5. 前端页面设计

### 5.1 页面结构

| 页面/组件 | 文件路径 | 功能描述 |
| :--- | :--- | :--- |
| 主页面 | src/App.vue | 整体布局容器 |
| Ticket列表 | src/components/TicketList.vue | 展示Ticket列表、搜索、分页 |
| Ticket表单 | src/components/TicketForm.vue | 创建/编辑Ticket表单 |
| 标签筛选 | src/components/TagFilter.vue | 标签选择器 |
| 标签管理 | src/components/TagManager.vue | 标签管理弹窗 |

### 5.2 页面布局图

```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────────┐  ┌────────────────────────────────────┐  │
│  │   Logo/标题  │  │        搜索框 + 新建按钮            │  │
│  └──────────────┘  └────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │              标签筛选栏（可多选）                    │  │
│  │  [全部] [文档] [开发] [测试] [紧急]  + [管理标签]    │  │
│  └─────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │                  Ticket列表区域                      │  │
│  │  ┌─────────────────────────────────────────────┐    │  │
│  │  │ [状态图标] 名称                                │    │  │
│  │  │ 描述内容                                      │    │  │
│  │  │ [标签1] [标签2]  · 创建时间                    │    │  │
│  │  │ [编辑] [删除] [完成/取消完成]                   │    │  │
│  │  └─────────────────────────────────────────────┘    │  │
│  └─────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐  │
│  │                    分页组件                         │  │
│  │  每页显示：[10] [20] [30] 条  ·  页码导航          │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### 5.3 组件功能说明

#### 5.3.1 TicketList.vue
- 展示Ticket卡片列表
- 支持状态显示（完成/待办）
- 显示关联标签
- 提供操作按钮（编辑、删除、状态切换）

#### 5.3.2 TicketForm.vue
- 支持创建和编辑模式
- 表单字段：名称、描述、状态
- 标签选择器（多选）
- 表单验证

#### 5.3.3 TagFilter.vue
- 展示所有标签
- 支持多选筛选
- 显示"全部"选项
- 管理标签入口

#### 5.3.4 TagManager.vue
- 标签列表展示
- 创建新标签（名称、颜色选择）
- 删除标签（有Ticket关联时提示）

---

## 6. 数据模型定义

### 6.1 后端数据模型 (Python Pydantic)

#### 6.1.1 Tag模型

```python
class TagBase(BaseModel):
    name: str
    color: str = '#1f77b4'

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True
```

#### 6.1.2 Ticket模型

```python
class TicketBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: str = 'pending'

class TicketCreate(TicketBase):
    tag_ids: Optional[List[int]] = []

class TicketUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Ticket(TicketBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []
    
    class Config:
        from_attributes = True
```

#### 6.1.3 分页响应模型

```python
class PageResponse(BaseModel):
    data: List[Ticket]
    total: int
    page: int
    page_size: int
```

### 6.2 前端数据模型 (TypeScript)

```typescript
interface Tag {
  id: number;
  name: string;
  color: string;
}

interface Ticket {
  id: number;
  name: string;
  description?: string;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

interface PageResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}
```

---

## 7. 业务流程

### 7.1 创建Ticket流程

```
用户点击"新建" → 打开表单弹窗 → 填写名称/描述 → 选择标签 → 提交
                                              │
                                              ▼
                                   后端验证数据 → 创建Ticket记录
                                              │
                                              ▼
                                   建立Ticket-Tag关联 → 返回成功
                                              │
                                              ▼
                                   前端刷新列表 → 关闭弹窗
```

### 7.2 搜索和筛选流程

```
用户输入搜索词/选择标签 → 触发查询 → 后端执行SQL查询
                                              │
                                              ▼
                                   返回分页数据 → 前端更新列表
```

### 7.3 状态切换流程

```
用户点击"完成"/"取消完成" → 发送PATCH请求 → 后端更新status字段
                                              │
                                              ▼
                                   返回更新后的Ticket → 前端更新显示
```

---

## 8. 部署与运行

### 8.1 环境要求

| 依赖 | 版本 |
| :--- | :--- |
| Python | 3.10+ |
| Node.js | 18+ |
| PostgreSQL | 15+ |

### 8.2 后端运行

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移
python -m alembic upgrade head

# 启动服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 8.3 前端运行

```bash
# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

---

## 9. 安全性考虑

| 安全事项 | 说明 |
| :--- | :--- |
| SQL注入 | 使用SQLAlchemy ORM，避免直接拼接SQL |
| 输入验证 | 使用Pydantic进行数据校验 |
| XSS防护 | 前端使用Vue模板自动转义 |
| CORS配置 | 配置允许前端域名访问 |
| 参数校验 | 分页参数限制范围（1-30） |
