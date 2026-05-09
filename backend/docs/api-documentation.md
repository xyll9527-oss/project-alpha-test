# Ticket管理系统 - 后端API接口文档

## 文档说明

本文档详细描述了Ticket管理系统的所有后端API接口，包括接口路径、HTTP方法、请求参数、响应格式、请求示例和响应示例。

---

## 基础信息

| 项目 | 说明 |
| :--- | :--- |
| **API版本** | 1.0.0 |
| **基础URL** | `http://localhost:8000/api` |
| **认证方式** | 无（无需用户系统） |
| **数据格式** | JSON |

---

## 接口列表

### 一、工单（Ticket）相关接口

#### 1. 获取工单列表

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets` |
| **方法** | GET |
| **描述** | 获取工单列表，支持搜索、标签筛选和分页 |

**请求参数（Query Parameters）：**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `search` | string | 否 | - | 搜索关键词，模糊匹配工单名称 |
| `tag_id` | integer | 否 | - | 标签ID，筛选关联了该标签的工单 |
| `page` | integer | 否 | 1 | 页码，从1开始 |
| `page_size` | integer | 否 | 10 | 每页大小，可选10/20/30 |

**请求示例：**
```bash
GET /api/tickets?search=修复&tag_id=2&page=1&page_size=10
```

**成功响应（200 OK）：**
```json
{
    "data": [
        {
            "name": "修复登录页面验证码显示问题",
            "description": "用户反馈登录页面验证码无法正常显示",
            "status": "pending",
            "id": 1,
            "created_at": "2024-01-01T09:00:00",
            "updated_at": "2024-01-01T09:00:00",
            "tags": [
                {
                    "name": "重要",
                    "color": "#fd7e14",
                    "id": 2
                },
                {
                    "name": "Bug修复",
                    "color": "#dc3545",
                    "id": 6
                }
            ]
        }
    ],
    "total": 15,
    "page": 1,
    "page_size": 10
}
```

---

#### 2. 获取单个工单

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}` |
| **方法** | GET |
| **描述** | 根据ID获取单个工单的详细信息 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |

**请求示例：**
```bash
GET /api/tickets/1
```

**成功响应（200 OK）：**
```json
{
    "name": "修复登录页面验证码显示问题",
    "description": "用户反馈登录页面验证码无法正常显示，需要排查前端渲染问题",
    "status": "pending",
    "id": 1,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-01T09:00:00",
    "tags": [
        {
            "name": "重要",
            "color": "#fd7e14",
            "id": 2
        },
        {
            "name": "Bug修复",
            "color": "#dc3545",
            "id": 6
        }
    ]
}
```

**失败响应（404 Not Found）：**
```json
{
    "detail": "Ticket not found"
}
```

---

#### 3. 创建工单

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets` |
| **方法** | POST |
| **描述** | 创建新工单 |

**请求体（JSON）：**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | string | 是 | - | 工单名称 |
| `description` | string | 否 | - | 工单描述 |
| `status` | string | 否 | pending | 工单状态，可选值：pending/completed |
| `tag_ids` | array[integer] | 否 | [] | 关联的标签ID列表 |

**请求示例：**
```bash
POST /api/tickets
Content-Type: application/json

{
    "name": "实现用户导出功能",
    "description": "用户需要能够导出自己的数据",
    "status": "pending",
    "tag_ids": [1, 5]
}
```

**成功响应（201 Created）：**
```json
{
    "name": "实现用户导出功能",
    "description": "用户需要能够导出自己的数据",
    "status": "pending",
    "id": 51,
    "created_at": "2024-01-11T10:00:00",
    "updated_at": "2024-01-11T10:00:00",
    "tags": [
        {
            "name": "紧急",
            "color": "#dc3545",
            "id": 1
        },
        {
            "name": "功能需求",
            "color": "#28a745",
            "id": 5
        }
    ]
}
```

---

#### 4. 更新工单

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}` |
| **方法** | PUT |
| **描述** | 更新工单信息 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |

**请求体（JSON）：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `name` | string | 否 | 工单名称 |
| `description` | string | 否 | 工单描述 |
| `status` | string | 否 | 工单状态 |

**请求示例：**
```bash
PUT /api/tickets/1
Content-Type: application/json

{
    "name": "修复登录页面验证码显示问题（已确认）",
    "description": "用户反馈登录页面验证码无法正常显示，已确认是前端渲染问题"
}
```

**成功响应（200 OK）：**
```json
{
    "name": "修复登录页面验证码显示问题（已确认）",
    "description": "用户反馈登录页面验证码无法正常显示，已确认是前端渲染问题",
    "status": "pending",
    "id": 1,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-11T10:30:00",
    "tags": [...]
}
```

**失败响应（404 Not Found）：**
```json
{
    "detail": "Ticket not found"
}
```

---

#### 5. 删除工单

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}` |
| **方法** | DELETE |
| **描述** | 删除工单 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |

**请求示例：**
```bash
DELETE /api/tickets/1
```

**成功响应（204 No Content）：**
无响应体

**失败响应（404 Not Found）：**
```json
{
    "detail": "Ticket not found"
}
```

---

#### 6. 更新工单状态

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}/status` |
| **方法** | PATCH |
| **描述** | 更新工单状态（完成/取消完成） |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |

**请求体（JSON）：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `status` | string | 是 | 新状态，值为'pending'或'completed' |

**请求示例：**
```bash
PATCH /api/tickets/1/status
Content-Type: application/json

{
    "status": "completed"
}
```

**成功响应（200 OK）：**
```json
{
    "name": "修复登录页面验证码显示问题",
    "description": "用户反馈登录页面验证码无法正常显示",
    "status": "completed",
    "id": 1,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-11T11:00:00",
    "tags": [...]
}
```

**失败响应（400 Bad Request）：**
```json
{
    "detail": "Invalid status. Must be 'pending' or 'completed'"
}
```

---

#### 7. 为工单添加标签

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}/tags/{tag_id}` |
| **方法** | POST |
| **描述** | 为指定工单添加标签 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |
| `tag_id` | integer | 是 | 标签ID |

**请求示例：**
```bash
POST /api/tickets/1/tags/3
```

**成功响应（200 OK）：**
```json
{
    "name": "修复登录页面验证码显示问题",
    "description": "用户反馈登录页面验证码无法正常显示",
    "status": "pending",
    "id": 1,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-11T11:30:00",
    "tags": [
        {"id": 2, "name": "重要", "color": "#fd7e14"},
        {"id": 6, "name": "Bug修复", "color": "#dc3545"},
        {"id": 3, "name": "普通", "color": "#1f77b4"}
    ]
}
```

**失败响应（404 Not Found）：**
```json
{
    "detail": "Ticket or Tag not found"
}
```

---

#### 8. 从工单移除标签

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tickets/{ticket_id}/tags/{tag_id}` |
| **方法** | DELETE |
| **描述** | 从指定工单移除标签 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `ticket_id` | integer | 是 | 工单ID |
| `tag_id` | integer | 是 | 标签ID |

**请求示例：**
```bash
DELETE /api/tickets/1/tags/3
```

**成功响应（200 OK）：**
```json
{
    "name": "修复登录页面验证码显示问题",
    "description": "用户反馈登录页面验证码无法正常显示",
    "status": "pending",
    "id": 1,
    "created_at": "2024-01-01T09:00:00",
    "updated_at": "2024-01-11T12:00:00",
    "tags": [
        {"id": 2, "name": "重要", "color": "#fd7e14"},
        {"id": 6, "name": "Bug修复", "color": "#dc3545"}
    ]
}
```

**失败响应（404 Not Found）：**
```json
{
    "detail": "Ticket or Tag not found"
}
```

---

### 二、标签（Tag）相关接口

#### 1. 获取所有标签

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tags` |
| **方法** | GET |
| **描述** | 获取所有标签列表 |

**请求示例：**
```bash
GET /api/tags
```

**成功响应（200 OK）：**
```json
[
    {
        "name": "紧急",
        "color": "#dc3545",
        "id": 1
    },
    {
        "name": "重要",
        "color": "#fd7e14",
        "id": 2
    },
    {
        "name": "普通",
        "color": "#1f77b4",
        "id": 3
    },
    {
        "name": "低优先级",
        "color": "#6c757d",
        "id": 4
    },
    {
        "name": "功能需求",
        "color": "#28a745",
        "id": 5
    },
    {
        "name": "Bug修复",
        "color": "#dc3545",
        "id": 6
    },
    {
        "name": "技术债务",
        "color": "#6610f2",
        "id": 7
    },
    {
        "name": "文档",
        "color": "#17a2b8",
        "id": 8
    },
    {
        "name": "测试",
        "color": "#20c997",
        "id": 9
    },
    {
        "name": "优化",
        "color": "#ffc107",
        "id": 10
    }
]
```

---

#### 2. 创建标签

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tags` |
| **方法** | POST |
| **描述** | 创建新标签 |

**请求体（JSON）：**

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
| :--- | :--- | :--- | :--- | :--- |
| `name` | string | 是 | - | 标签名称 |
| `color` | string | 否 | #1f77b4 | 标签颜色，十六进制格式 |

**请求示例：**
```bash
POST /api/tags
Content-Type: application/json

{
    "name": "安全问题",
    "color": "#dc3545"
}
```

**成功响应（201 Created）：**
```json
{
    "name": "安全问题",
    "color": "#dc3545",
    "id": 11
}
```

---

#### 3. 删除标签

| 属性 | 值 |
| :--- | :--- |
| **路径** | `/tags/{tag_id}` |
| **方法** | DELETE |
| **描述** | 删除标签 |

**路径参数：**

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `tag_id` | integer | 是 | 标签ID |

**请求示例：**
```bash
DELETE /api/tags/11
```

**成功响应（204 No Content）：**
无响应体

**失败响应（404 Not Found）：**
```json
{
    "detail": "Tag not found"
}
```

---

## 错误响应格式

所有错误响应均遵循以下格式：

```json
{
    "detail": "错误描述信息"
}
```

**HTTP状态码说明：**

| 状态码 | 说明 |
| :--- | :--- |
| 200 OK | 请求成功 |
| 201 Created | 资源创建成功 |
| 204 No Content | 请求成功，无响应体 |
| 400 Bad Request | 请求参数错误 |
| 404 Not Found | 资源不存在 |
| 500 Internal Server Error | 服务器内部错误 |

---

## 状态值说明

工单状态（status）字段的可选值：

| 值 | 说明 |
| :--- | :--- |
| `pending` | 待办状态 |
| `completed` | 已完成状态 |

---

## 数据模型

### Tag（标签）

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | integer | 标签唯一标识 |
| `name` | string | 标签名称 |
| `color` | string | 标签颜色（十六进制） |

### Ticket（工单）

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `id` | integer | 工单唯一标识 |
| `name` | string | 工单名称 |
| `description` | string | 工单描述（可选） |
| `status` | string | 工单状态 |
| `created_at` | datetime | 创建时间 |
| `updated_at` | datetime | 更新时间 |
| `tags` | array[Tag] | 关联的标签列表 |

### PageResponse（分页响应）

| 字段名 | 类型 | 说明 |
| :--- | :--- | :--- |
| `data` | array[Ticket] | 当前页的数据列表 |
| `total` | integer | 总记录数 |
| `page` | integer | 当前页码 |
| `page_size` | integer | 每页大小 |
