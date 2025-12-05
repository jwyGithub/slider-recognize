"""
API 路由模块

提供 HTTP API 路由定义和处理。
"""

from src.api.router import api_router
from src.api.deps import get_slider_service

__all__ = [
    "api_router",
    "get_slider_service",
]
