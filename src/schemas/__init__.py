"""
数据模型模块

定义 API 请求和响应的数据模型（Schema）。
"""

from src.schemas.request import SliderRequest, RecognitionMethod
from src.schemas.response import (
    BaseResponse,
    SliderResponse,
    HealthResponse,
    ServiceInfoResponse,
    create_response,
    create_success_response,
    create_error_response,
    create_service_info,
)

__all__ = [
    # 请求模型
    "SliderRequest",
    "RecognitionMethod",
    # 响应模型
    "BaseResponse",
    "SliderResponse",
    "HealthResponse",
    "ServiceInfoResponse",
    # 响应工厂函数
    "create_response",
    "create_success_response",
    "create_error_response",
    "create_service_info",
]
