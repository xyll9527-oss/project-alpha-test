"""
数据验证模型模块

该模块使用Pydantic定义数据验证模型，用于API请求和响应的数据校验。
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    """
    标签基础模型
    
    包含标签的基本字段，用于创建和响应。
    
    Attributes:
        name: 标签名称
        color: 标签颜色，默认为蓝色
    """
    name: str
    color: str = '#1f77b4'


class TagCreate(TagBase):
    """
    创建标签模型
    
    继承TagBase，用于接收创建标签的请求数据。
    """
    pass


class Tag(TagBase):
    """
    标签响应模型
    
    用于返回标签详细信息，包含ID字段。
    
    Attributes:
        id: 标签唯一标识
    """
    id: int
    
    class Config:
        # 允许从ORM模型直接转换为Pydantic模型
        from_attributes = True


class TicketBase(BaseModel):
    """
    工单基础模型
    
    包含工单的基本字段。
    
    Attributes:
        name: 工单名称
        description: 工单描述（可选）
        status: 工单状态，默认为'pending'
    """
    name: str
    description: Optional[str] = None
    status: str = 'pending'


class TicketCreate(TicketBase):
    """
    创建工单模型
    
    继承TicketBase，增加标签ID列表字段。
    
    Attributes:
        tag_ids: 关联的标签ID列表（可选）
    """
    tag_ids: Optional[List[int]] = []


class TicketUpdate(BaseModel):
    """
    更新工单模型
    
    所有字段均为可选，用于部分更新工单信息。
    
    Attributes:
        name: 工单名称（可选）
        description: 工单描述（可选）
        status: 工单状态（可选）
    """
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TicketStatusUpdate(BaseModel):
    """
    更新工单状态模型
    
    专门用于更新工单状态的请求。
    
    Attributes:
        status: 工单状态，值为'pending'或'completed'
    """
    status: str


class Ticket(TicketBase):
    """
    工单响应模型
    
    用于返回工单详细信息，包含ID、时间戳和关联标签。
    
    Attributes:
        id: 工单唯一标识
        created_at: 创建时间
        updated_at: 更新时间
        tags: 关联的标签列表
    """
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []
    
    class Config:
        from_attributes = True


class PageResponse(BaseModel):
    """
    分页响应模型
    
    用于返回分页数据。
    
    Attributes:
        data: 当前页的数据列表
        total: 总记录数
        page: 当前页码
        page_size: 每页大小
    """
    data: List[Ticket]
    total: int
    page: int
    page_size: int
