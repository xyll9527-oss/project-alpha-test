"""
标签API路由模块

该模块定义了所有与标签相关的API端点，包括获取标签列表、创建和删除标签。
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

# 创建API路由器
router = APIRouter()


@router.get("/tags", response_model=list[schemas.Tag], summary="获取所有标签")
def get_tags(db: Session = Depends(database.get_db)):
    """
    获取所有标签列表
    
    Returns:
        List[Tag]: 所有标签对象列表
    """
    return crud.get_tags(db)


@router.post("/tags", response_model=schemas.Tag, status_code=201, summary="创建标签")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(database.get_db)):
    """
    创建新标签
    
    Args:
        tag: 标签创建请求数据，包含名称和颜色（可选）
    
    Returns:
        Tag: 创建成功的标签信息
    """
    return crud.create_tag(db, tag)


@router.delete("/tags/{tag_id}", status_code=204, summary="删除标签")
def delete_tag(tag_id: int, db: Session = Depends(database.get_db)):
    """
    删除标签
    
    Args:
        tag_id: 标签ID
    
    Returns:
        204 No Content: 删除成功无响应体
    
    Raises:
        HTTPException: 标签不存在时返回404
    """
    success = crud.delete_tag(db, tag_id)
    if not success:
        raise HTTPException(status_code=404, detail="Tag not found")
