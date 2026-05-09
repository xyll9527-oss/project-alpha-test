"""
数据库连接配置模块

该模块负责建立与PostgreSQL数据库的连接，提供数据库会话管理功能。
从环境变量中读取数据库连接配置。
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 加载环境变量配置
load_dotenv()

# 从环境变量获取数据库连接URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("环境变量 DATABASE_URL 未设置")

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建会话工厂
# autocommit=False: 手动控制事务提交
# autoflush=False: 禁用自动刷新
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建SQLAlchemy基础类
# 所有模型类都需要继承此类
Base = declarative_base()


def get_db():
    """
    获取数据库会话依赖函数
    
    该函数用于FastAPI的依赖注入，每次请求时创建一个新的数据库会话，
    请求结束后自动关闭会话，确保资源正确释放。
    
    Yields:
        Session: SQLAlchemy数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
