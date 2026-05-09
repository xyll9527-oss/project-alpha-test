"""
CRUD操作模块

该模块封装了所有数据库操作，提供对工单和标签的增删改查功能。
"""

from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


def get_tags(db: Session):
    """
    获取所有标签列表
    
    Args:
        db: 数据库会话对象
    
    Returns:
        List[models.Tag]: 所有标签对象列表
    """
    return db.query(models.Tag).all()


def get_tag(db: Session, tag_id: int):
    """
    根据ID获取单个标签
    
    Args:
        db: 数据库会话对象
        tag_id: 标签ID
    
    Returns:
        models.Tag: 标签对象，如果不存在返回None
    """
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


def create_tag(db: Session, tag: schemas.TagCreate):
    """
    创建新标签
    
    Args:
        db: 数据库会话对象
        tag: 标签创建请求数据
    
    Returns:
        models.Tag: 创建成功的标签对象
    """
    db_tag = models.Tag(name=tag.name, color=tag.color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int):
    """
    删除标签
    
    Args:
        db: 数据库会话对象
        tag_id: 标签ID
    
    Returns:
        bool: 删除成功返回True，否则返回False
    """
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if tag:
        db.delete(tag)
        db.commit()
        return True
    return False


def get_tickets(
    db: Session,
    search: str = None,
    tag_id: int = None,
    status: str = None,
    page: int = 1,
    page_size: int = 10
):
    """
    获取工单列表（支持搜索、筛选和分页）
    
    Args:
        db: 数据库会话对象
        search: 搜索关键词，匹配工单名称（可选）
        tag_id: 标签ID，按标签筛选（可选）
        status: 状态筛选，pending 或 completed（可选）
        page: 页码，默认为1
        page_size: 每页大小，默认为10
    
    Returns:
        dict: 包含数据列表和分页信息的字典
    """
    query = db.query(models.Ticket)
    
    # 按名称搜索
    if search:
        query = query.filter(models.Ticket.name.contains(search))
    
    # 按标签筛选
    if tag_id:
        query = query.join(models.TicketTag).filter(models.TicketTag.tag_id == tag_id)
    
    # 按状态筛选
    if status:
        query = query.filter(models.Ticket.status == status)
    
    # 计算总数和分页
    total = query.count()
    tickets = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {"data": tickets, "total": total, "page": page, "page_size": page_size}


def get_ticket(db: Session, ticket_id: int):
    """
    根据ID获取单个工单
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
    
    Returns:
        models.Ticket: 工单对象，如果不存在返回None
    """
    return db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()


def create_ticket(db: Session, ticket: schemas.TicketCreate):
    """
    创建新工单
    
    Args:
        db: 数据库会话对象
        ticket: 工单创建请求数据
    
    Returns:
        models.Ticket: 创建成功的工单对象
    """
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


def update_ticket(db: Session, ticket_id: int, ticket_update: schemas.TicketUpdate):
    """
    更新工单信息
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
        ticket_update: 工单更新请求数据
    
    Returns:
        models.Ticket: 更新后的工单对象，如果不存在返回None
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        if ticket_update.name is not None:
            db_ticket.name = ticket_update.name
        if ticket_update.description is not None:
            db_ticket.description = ticket_update.description
        if ticket_update.status is not None:
            db_ticket.status = ticket_update.status
        db_ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_ticket)
    return db_ticket


def update_ticket_status(db: Session, ticket_id: int, status: str):
    """
    更新工单状态
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
        status: 新状态，值为'pending'或'completed'
    
    Returns:
        models.Ticket: 更新后的工单对象，如果不存在返回None
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db_ticket.status = status
        db_ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_ticket)
    return db_ticket


def delete_ticket(db: Session, ticket_id: int):
    """
    删除工单
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
    
    Returns:
        bool: 删除成功返回True，否则返回False
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if db_ticket:
        db.delete(db_ticket)
        db.commit()
        return True
    return False


def add_tag_to_ticket(db: Session, ticket_id: int, tag_id: int):
    """
    为工单添加标签
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
        tag_id: 标签ID
    
    Returns:
        models.Ticket: 更新后的工单对象，如果工单或标签不存在返回None
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    
    if db_ticket and db_tag:
        if db_tag not in db_ticket.tags:
            db_ticket.tags.append(db_tag)
            db.commit()
            db.refresh(db_ticket)
        return db_ticket
    return None


def remove_tag_from_ticket(db: Session, ticket_id: int, tag_id: int):
    """
    从工单移除标签
    
    Args:
        db: 数据库会话对象
        ticket_id: 工单ID
        tag_id: 标签ID
    
    Returns:
        models.Ticket: 更新后的工单对象，如果工单或标签不存在返回None
    """
    db_ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    
    if db_ticket and db_tag:
        if db_tag in db_ticket.tags:
            db_ticket.tags.remove(db_tag)
            db.commit()
            db.refresh(db_ticket)
        return db_ticket
    return None


def get_tickets_stats(db: Session):
    """
    获取工单统计信息
    
    Args:
        db: 数据库会话对象
    
    Returns:
        dict: 包含各状态数量的统计信息
    """
    total = db.query(models.Ticket).count()
    pending = db.query(models.Ticket).filter(models.Ticket.status == "pending").count()
    completed = db.query(models.Ticket).filter(models.Ticket.status == "completed").count()
    
    return {
        "total": total,
        "pending": pending,
        "completed": completed
    }
