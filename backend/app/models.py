"""
数据库模型定义模块

该模块定义了数据库中的所有表结构，使用SQLAlchemy ORM进行映射。
包含三张表：tags（标签表）、tickets（工单表）、ticket_tags（关联表）
"""

from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Tag(Base):
    """
    标签模型类
    
    用于存储工单标签信息，支持颜色标识。
    
    Attributes:
        id: 标签唯一标识，主键
        name: 标签名称，唯一且不能为空
        color: 标签颜色，十六进制格式，默认为蓝色(#1f77b4)
        tickets: 关联的工单列表（多对多关系）
    """
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), default="#1f77b4")


class Ticket(Base):
    """
    工单模型类
    
    用于存储工单信息，支持与标签的多对多关联。
    
    Attributes:
        id: 工单唯一标识，主键
        name: 工单名称，不能为空
        description: 工单描述，可选
        status: 工单状态，可选值为'pending'（待办）或'completed'（已完成），默认为'pending'
        created_at: 创建时间，自动生成
        updated_at: 更新时间，自动生成
        tags: 关联的标签列表（多对多关系）
    """
    __tablename__ = "tickets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    
    # 与Tag的多对多关系，通过ticket_tags中间表关联
    tags = relationship("Tag", secondary="ticket_tags", back_populates="tickets")


class TicketTag(Base):
    """
    工单-标签关联模型类
    
    作为tickets表和tags表的中间表，实现多对多关系。
    
    Attributes:
        ticket_id: 工单ID，外键关联tickets表
        tag_id: 标签ID，外键关联tags表
    """
    __tablename__ = "ticket_tags"
    
    ticket_id = Column(Integer, ForeignKey("tickets.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)


# 建立Tag与Ticket的双向关系
Tag.tickets = relationship("Ticket", secondary="ticket_tags", back_populates="tags")
