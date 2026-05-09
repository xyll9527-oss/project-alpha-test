# 项目Alpha - Ticket标签分类和管理工具 - 实现文档

## 1. 项目概述

本文档是根据 `project-alpha-design.md` 设计文档制定的详细实现计划，旨在指导开发团队完成整个项目的开发工作。

### 1.1 项目目标
- 构建一个基于 Vue3 + Element Plus 的前端界面
- 构建一个基于 FastAPI 的后端服务
- 使用 PostgreSQL 作为数据库存储
- 实现 Ticket 的 CRUD 操作
- 实现标签管理和筛选功能
- 实现搜索和分页功能

### 1.2 项目结构
```
project-alpha/
├── backend/                 # 后端代码
│   ├── app/                # 应用代码
│   ├── tests/              # 测试代码
│   ├── requirements.txt    # Python依赖
│   └── main.py             # 入口文件
├── frontend/               # 前端代码
│   ├── src/                # 源代码
│   ├── public/             # 静态资源
│   ├── package.json        # npm依赖
│   └── vite.config.ts      # Vite配置
└── docs/                   # 文档
```

---

## 2. 实现计划总览

| 阶段 | 任务 | 预计时间 | 负责人 |
| :--- | :--- | :--- | :--- |
| 第一阶段 | 环境准备与项目初始化 | 1天 | 后端开发 |
| 第二阶段 | 数据库设计与迁移 | 1天 | 后端开发 |
| 第三阶段 | 后端API实现 | 3天 | 后端开发 |
| 第四阶段 | 前端项目初始化 | 1天 | 前端开发 |
| 第五阶段 | 前端组件实现 | 3天 | 前端开发 |
| 第六阶段 | 联调测试 | 2天 | 前后端协作 |
| 第七阶段 | 部署上线 | 1天 | DevOps |

---

## 3. 后端实现计划

### 3.1 环境准备

**任务：**
- 安装 Python 3.10+
- 安装 PostgreSQL 15+
- 创建虚拟环境
- 安装依赖包

**文件清单：**
- `backend/requirements.txt`

**依赖列表：**
```
fastapi==0.100.0
uvicorn==0.23.2
sqlalchemy==2.0.20
pydantic==2.4.2
python-dotenv==1.0.0
alembic==1.12.1
psycopg2-binary==2.9.7
```

### 3.2 数据库设计与迁移

**任务：**
- 创建数据库表结构
- 配置 Alembic 迁移工具
- 生成初始迁移脚本

**文件清单：**
- `backend/app/models.py` - SQLAlchemy 模型定义
- `backend/alembic.ini` - Alembic 配置
- `backend/migrations/` - 迁移脚本目录

**模型定义要点：**
```python
# models.py
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), default="#1f77b4")

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    tags = relationship("Tag", secondary="ticket_tags", backref="tickets")

class TicketTag(Base):
    __tablename__ = "ticket_tags"
    ticket_id = Column(Integer, ForeignKey("tickets.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)
```

### 3.3 后端API实现

#### 3.3.1 目录结构
```
backend/app/
├── __init__.py
├── main.py          # FastAPI应用入口
├── models.py        # 数据库模型
├── schemas.py       # Pydantic模型
├── crud.py          # CRUD操作
├── api/             # API路由
│   ├── __init__.py
│   ├── tickets.py   # Ticket相关API
│   └── tags.py      # Tag相关API
└── database.py      # 数据库连接配置
```

#### 3.3.2 任务分解

| 任务 | 描述 | 预计时间 |
| :--- | :--- | :--- |
| 3.3.2.1 | 创建数据库连接配置 | 0.5天 |
| 3.3.2.2 | 定义Pydantic模型 | 0.5天 |
| 3.3.2.3 | 实现CRUD操作 | 1天 |
| 3.3.2.4 | 实现Ticket API | 1天 |
| 3.3.2.5 | 实现Tag API | 1天 |

#### 3.3.3 API实现详情

**Ticket API (`backend/app/api/tickets.py`)**

| API路径 | HTTP方法 | 功能描述 |
| :--- | :--- | :--- |
| /api/tickets | GET | 获取Ticket列表（支持搜索、筛选、分页） |
| /api/tickets/{id} | GET | 获取单个Ticket详情 |
| /api/tickets | POST | 创建新Ticket |
| /api/tickets/{id} | PUT | 更新Ticket信息 |
| /api/tickets/{id} | DELETE | 删除Ticket |
| /api/tickets/{id}/status | PATCH | 更新Ticket状态 |
| /api/tickets/{ticket_id}/tags/{tag_id} | POST | 为Ticket添加标签 |
| /api/tickets/{ticket_id}/tags/{tag_id} | DELETE | 从Ticket移除标签 |

**Tag API (`backend/app/api/tags.py`)**

| API路径 | HTTP方法 | 功能描述 |
| :--- | :--- | :--- |
| /api/tags | GET | 获取所有标签列表 |
| /api/tags | POST | 创建新标签 |
| /api/tags/{id} | DELETE | 删除标签 |

#### 3.3.4 CRUD操作实现要点

```python
# crud.py - Ticket CRUD示例
def get_tickets(db: Session, search: str = None, tag_id: int = None, page: int = 1, page_size: int = 10):
    query = db.query(Ticket)
    
    if search:
        query = query.filter(Ticket.name.contains(search))
    
    if tag_id:
        query = query.join(TicketTag).filter(TicketTag.tag_id == tag_id)
    
    total = query.count()
    tickets = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {"data": tickets, "total": total, "page": page, "page_size": page_size}

def create_ticket(db: Session, ticket: schemas.TicketCreate):
    db_ticket = models.Ticket(
        name=ticket.name,
        description=ticket.description,
        status=ticket.status
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    # 添加标签关联
    if ticket.tag_ids:
        for tag_id in ticket.tag_ids:
            tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
            if tag:
                db_ticket.tags.append(tag)
        db.commit()
    
    return db_ticket
```

---

## 4. 前端实现计划

### 4.1 项目初始化

**任务：**
- 使用 Vite 创建 Vue3 项目
- 安装 Element Plus 依赖
- 配置项目结构

**命令：**
```bash
npm create vite@6.5.0 . -- --template vue
npm install element-plus
npm install axios
```

**文件清单：**
- `frontend/package.json`
- `frontend/vite.config.ts`
- `frontend/src/main.ts`

### 4.2 组件实现

#### 4.2.1 目录结构
```
frontend/src/
├── main.ts           # 入口文件
├── App.vue           # 主组件
├── components/       # 组件目录
│   ├── TicketList.vue    # Ticket列表组件
│   ├── TicketForm.vue    # Ticket表单组件
│   ├── TagFilter.vue     # 标签筛选组件
│   └── TagManager.vue    # 标签管理弹窗
├── composables/      # 组合式函数
│   └── useApi.ts     # API调用封装
└── types/            # 类型定义
    └── index.ts      # TypeScript类型
```

#### 4.2.2 任务分解

| 任务 | 描述 | 预计时间 |
| :--- | :--- | :--- |
| 4.2.2.1 | 类型定义 | 0.5天 |
| 4.2.2.2 | API封装 | 0.5天 |
| 4.2.2.3 | TicketList组件 | 1天 |
| 4.2.2.4 | TicketForm组件 | 1天 |
| 4.2.2.5 | TagFilter组件 | 0.5天 |
| 4.2.2.6 | TagManager组件 | 0.5天 |
| 4.2.2.7 | 主页面整合 | 0.5天 |

#### 4.2.3 组件实现要点

**TypeScript类型定义 (`frontend/src/types/index.ts`)**
```typescript
export interface Tag {
  id: number;
  name: string;
  color: string;
}

export interface Ticket {
  id: number;
  name: string;
  description?: string;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface PageResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface TicketCreate {
  name: string;
  description?: string;
  status?: string;
  tag_ids?: number[];
}

export interface TicketUpdate {
  name?: string;
  description?: string;
  status?: string;
}
```

**API封装 (`frontend/src/composables/useApi.ts`)**
```typescript
import { ref } from 'vue';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api';

export function useApi() {
  const loading = ref(false);
  const error = ref<string | null>(null);

  const getTickets = async (params: {
    search?: string;
    tag_id?: number;
    page?: number;
    page_size?: number;
  }) => {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${API_BASE}/tickets`, { params });
      return response.data;
    } catch (e) {
      error.value = '获取Ticket失败';
      throw e;
    } finally {
      loading.value = false;
    }
  };

  // 其他API方法...
  
  return {
    loading,
    error,
    getTickets,
    // ...其他方法
  };
}
```

**TicketList组件功能：**
- 展示Ticket卡片列表
- 状态显示（待办/完成）
- 标签展示
- 操作按钮（编辑、删除、状态切换）

**TicketForm组件功能：**
- 支持创建和编辑模式
- 表单验证
- 标签多选选择器

**TagFilter组件功能：**
- 展示所有标签
- 支持单选筛选
- 管理标签入口

**TagManager组件功能：**
- 标签列表展示
- 创建新标签（名称、颜色）
- 删除标签

### 4.3 页面布局

主页面布局结构：
```vue
<!-- App.vue -->
<template>
  <div class="app-container">
    <!-- 头部 -->
    <header class="app-header">
      <h1>Ticket管理系统</h1>
      <div class="header-actions">
        <el-input v-model="searchQuery" placeholder="搜索Ticket..." />
        <el-button type="primary" @click="openCreateForm">新建</el-button>
      </div>
    </header>
    
    <!-- 标签筛选栏 -->
    <TagFilter :tags="tags" :selectedTag="selectedTag" @select="handleTagSelect" />
    
    <!-- Ticket列表 -->
    <TicketList 
      :tickets="ticketPage.data" 
      :loading="loading"
      @edit="openEditForm"
      @delete="handleDelete"
      @toggle-status="handleToggleStatus"
    />
    
    <!-- 分页组件 -->
    <el-pagination
      :current-page="ticketPage.page"
      :page-size="ticketPage.page_size"
      :total="ticketPage.total"
      :page-sizes="[10, 20, 30]"
      @size-change="handlePageSizeChange"
      @current-change="handlePageChange"
    />
    
    <!-- Ticket表单弹窗 -->
    <TicketForm 
      v-if="showForm" 
      :ticket="editingTicket"
      :tags="tags"
      @close="closeForm"
      @submit="handleFormSubmit"
    />
    
    <!-- 标签管理弹窗 -->
    <TagManager 
      v-if="showTagManager"
      :tags="tags"
      @close="showTagManager = false"
      @update="handleTagsUpdate"
    />
  </div>
</template>
```

---

## 5. 测试计划

### 5.1 后端测试

**测试类型：**
- 单元测试：测试CRUD操作
- 集成测试：测试API接口
- 边界测试：测试异常情况

**测试文件：**
- `backend/tests/test_crud.py`
- `backend/tests/test_api.py`

**测试要点：**
- Ticket CRUD操作测试
- Tag CRUD操作测试
- 搜索功能测试
- 分页功能测试
- 标签关联测试

### 5.2 前端测试

**测试类型：**
- 组件测试：测试各个Vue组件
- 端到端测试：测试用户流程

**测试工具：**
- Vitest：单元测试
- Cypress：端到端测试

**测试要点：**
- Ticket列表展示
- Ticket创建/编辑流程
- 标签筛选功能
- 搜索功能
- 分页功能

---

## 6. 部署计划

### 6.1 开发环境

**后端启动：**
```bash
cd backend
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**前端启动：**
```bash
cd frontend
npm install
npm run dev
```

### 6.2 生产环境

**前端构建：**
```bash
cd frontend
npm run build
```

**Docker部署（可选）：**
- 创建 Dockerfile
- 创建 docker-compose.yml
- 配置 Nginx 反向代理

---

## 7. 任务时间线

```
第1天：环境准备与项目初始化
  ├─ 后端：安装依赖、配置数据库连接
  └─ 前端：Vite项目初始化、安装Element Plus

第2天：数据库设计与迁移
  ├─ 创建SQLAlchemy模型
  ├─ 配置Alembic
  └─ 生成迁移脚本并执行

第3-5天：后端API实现
  ├─ 第3天：创建Pydantic模型、实现CRUD操作
  ├─ 第4天：实现Ticket API（列表、创建、详情）
  └─ 第5天：实现Ticket API（更新、删除、状态）、Tag API

第6天：前端项目初始化
  ├─ 配置Element Plus
  ├─ 创建类型定义
  └─ 封装API调用

第7-9天：前端组件实现
  ├─ 第7天：TicketList组件
  ├─ 第8天：TicketForm组件、TagFilter组件
  └─ 第9天：TagManager组件、主页面整合

第10-11天：联调测试
  ├─ 第10天：前后端联调
  └─ 第11天：功能测试、Bug修复

第12天：部署上线
  ├─ 前端构建
  └─ 服务部署
```

---

## 8. 技术要点

### 8.1 后端注意事项
- 使用 SQLAlchemy 2.0 的声明式语法
- Pydantic 模型与 SQLAlchemy 模型的转换
- CORS 配置以允许前端访问
- 分页参数校验（限制 page_size 在 1-30 之间）

### 8.2 前端注意事项
- 使用 Composition API
- Element Plus 组件的正确使用
- 响应式数据管理
- API 错误处理和加载状态显示

### 8.3 数据库注意事项
- PostgreSQL 的全文搜索优化
- 索引创建以提升查询性能
- 事务处理确保数据一致性

---

## 9. 交付物清单

| 交付物 | 描述 | 状态 |
| :--- | :--- | :--- |
| backend/ | 后端代码（FastAPI + SQLAlchemy） | 待开发 |
| frontend/ | 前端代码（Vue3 + Element Plus） | 待开发 |
| project-alpha-design.md | 需求和设计文档 | 已完成 |
| project-alpha-implementation.md | 实现计划文档 | 已完成 |
| tests/ | 测试代码 | 待开发 |
