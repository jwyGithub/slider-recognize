"""
API 路由注册

汇总所有子路由并创建主路由。
"""

from fastapi import APIRouter

from src.api.routes import health, slider


# 创建主 API 路由
api_router = APIRouter()

# 注册子路由
api_router.include_router(
    health.router,
    tags=["健康检查"],
)

api_router.include_router(
    slider.router,
    prefix="/slider",
    tags=["滑块识别"],
)

