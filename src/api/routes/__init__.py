"""
路由定义模块

包含所有 API 端点的路由定义。
"""

from src.api.routes import health, slider, arithmetic

__all__ = ["health", "slider", "arithmetic"]

