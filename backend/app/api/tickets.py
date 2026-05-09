"""
工单API路由模块

该模块定义了所有与工单相关的API端点，包括CRUD操作、状态更新和标签关联。
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from .. import crud, schemas, database

# 创建API路由器
router = APIRouter()


@router.get("/tickets", response_model=schemas.PageResponse, summary="获取工单列表")
def get_tickets(
    search: Optional[str] = Query(None, description="搜索关键词，匹配工单名称"),
    tag_id: Optional[int] = Query(None, description="标签ID，按标签筛选"),
    status: Optional[str] = Query(None, description="状态筛选，pending 或 completed"),
    page: int = Query(1, ge=1, description="页码，默认为1"),
    page_size: int = Query(10, ge=1, le=30, description="每页大小，可选10/20/30，默认为10"),
    db: Session = Depends(database.get_db)
):
    """
    获取工单列表（支持搜索、筛选和分页）
    
    Args:
        search: 搜索关键词，模糊匹配工单名称
        tag_id: 标签ID，筛选关联了该标签的工单
        status: 状态筛选，pending 或 completed
        page: 页码，从1开始
        page_size: 每页数量，最大30
    
    Returns:
        PageResponse: 包含工单列表和分页信息的响应
    """
    return crud.get_tickets(db, search, tag_id, status, page, page_size)


@router.get("/tickets/{ticket_id}", response_model=schemas.Ticket, summary="获取单个工单")
def get_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    """
    根据ID获取单个工单的详细信息
    
    Args:
        ticket_id: 工单ID
    
    Returns:
        Ticket: 工单详细信息
    
    Raises:
        HTTPException: 工单不存在时返回404
    """
    db_ticket = crud.get_ticket(db, ticket_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.post("/tickets", response_model=schemas.Ticket, status_code=201, summary="创建工单")
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(database.get_db)):
    """
    创建新工单
    
    Args:
        ticket: 工单创建请求数据，包含名称、描述、状态和标签ID列表
    
    Returns:
        Ticket: 创建成功的工单信息
    """
    return crud.create_ticket(db, ticket)


@router.put("/tickets/{ticket_id}", response_model=schemas.Ticket, summary="更新工单")
def update_ticket(
    ticket_id: int,
    ticket_update: schemas.TicketUpdate,
    db: Session = Depends(database.get_db)
):
    """
    更新工单信息
    
    Args:
        ticket_id: 工单ID
        ticket_update: 工单更新数据，字段均为可选
    
    Returns:
        Ticket: 更新后的工单信息
    
    Raises:
        HTTPException: 工单不存在时返回404
    """
    db_ticket = crud.update_ticket(db, ticket_id, ticket_update)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.delete("/tickets/{ticket_id}", status_code=204, summary="删除工单")
def delete_ticket(ticket_id: int, db: Session = Depends(database.get_db)):
    """
    删除工单
    
    Args:
        ticket_id: 工单ID
    
    Returns:
        204 No Content: 删除成功无响应体
    
    Raises:
        HTTPException: 工单不存在时返回404
    """
    success = crud.delete_ticket(db, ticket_id)
    if not success:
        raise HTTPException(status_code=404, detail="Ticket not found")


@router.patch("/tickets/{ticket_id}/status", response_model=schemas.Ticket, summary="更新工单状态")
def update_ticket_status(
    ticket_id: int,
    status_update: schemas.TicketStatusUpdate,
    db: Session = Depends(database.get_db)
):
    """
    更新工单状态（完成/取消完成）
    
    Args:
        ticket_id: 工单ID
        status_update: 状态更新请求，status字段值为'pending'或'completed'
    
    Returns:
        Ticket: 更新后的工单信息
    
    Raises:
        HTTPException: 状态值无效时返回400，工单不存在时返回404
    """
    if status_update.status not in ["pending", "completed"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'pending' or 'completed'")
    db_ticket = crud.update_ticket_status(db, ticket_id, status_update.status)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return db_ticket


@router.post("/tickets/{ticket_id}/tags/{tag_id}", response_model=schemas.Ticket, summary="为工单添加标签")
def add_tag_to_ticket(ticket_id: int, tag_id: int, db: Session = Depends(database.get_db)):
    """
    为指定工单添加标签
    
    Args:
        ticket_id: 工单ID
        tag_id: 标签ID
    
    Returns:
        Ticket: 更新后的工单信息
    
    Raises:
        HTTPException: 工单或标签不存在时返回404
    """
    db_ticket = crud.add_tag_to_ticket(db, ticket_id, tag_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket or Tag not found")
    return db_ticket


@router.delete("/tickets/{ticket_id}/tags/{tag_id}", response_model=schemas.Ticket, summary="从工单移除标签")
def remove_tag_from_ticket(ticket_id: int, tag_id: int, db: Session = Depends(database.get_db)):
    """
    从指定工单移除标签
    
    Args:
        ticket_id: 工单ID
        tag_id: 标签ID
    
    Returns:
        Ticket: 更新后的工单信息
    
    Raises:
        HTTPException: 工单或标签不存在时返回404
    """
    db_ticket = crud.remove_tag_from_ticket(db, ticket_id, tag_id)
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket or Tag not found")
    return db_ticket


@router.get("/tickets/stats/count", summary="获取工单统计")
def get_tickets_stats(db: Session = Depends(database.get_db)):
    """
    获取各状态工单数量统计
    
    Returns:
        dict: 包含各状态数量的统计信息
    """
    return crud.get_tickets_stats(db)
