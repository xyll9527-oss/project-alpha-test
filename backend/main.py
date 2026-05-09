"""
Ticket Management API - 主入口文件

该文件是FastAPI应用的入口，负责初始化应用、配置中间件和注册路由。
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import tickets, tags

# 创建FastAPI应用实例
# title: API标题
# version: API版本
app = FastAPI(title="Ticket Management API", version="1.0.0")

# 配置CORS中间件
# 允许跨域请求，便于前端开发
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有来源（生产环境应限制具体域名）
    allow_credentials=True,        # 允许携带凭证
    allow_methods=["*"],           # 允许所有HTTP方法
    allow_headers=["*"],           # 允许所有请求头
)

# 注册API路由
# prefix: 路由前缀，所有API端点都以/api开头
# tags: 用于API文档分组
app.include_router(tickets.router, prefix="/api", tags=["tickets"])
app.include_router(tags.router, prefix="/api", tags=["tags"])


@app.get("/", tags=["root"])
def read_root():
    """
    根路径健康检查
    
    返回欢迎信息，用于验证API是否正常运行。
    
    Returns:
        dict: 包含欢迎消息的字典
    """
    return {"message": "Welcome to Ticket Management API"}


def main():
    """
    主函数 - 启动FastAPI应用
    
    使用uvicorn启动服务，监听0.0.0.0:8000端口，开启自动重载。
    可直接运行 python main.py 启动服务。
    
    Example:
        $ python main.py
        INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
    """
    print("[INFO] 正在启动 Ticket Management API...")
    print("[INFO] 服务地址: http://localhost:8000")
    print("[INFO] API文档: http://localhost:8000/docs")
    print("[INFO] 自动重载已开启，代码修改后会自动重启")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
