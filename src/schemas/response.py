"""
响应数据模型

定义 API 响应的数据结构和工厂函数。
"""

from typing import Any, Optional, TypeVar, Generic

from pydantic import BaseModel, Field

from src.config import settings


# 泛型类型变量
T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    """
    基础响应模型
    
    所有 API 响应的基类，定义统一的响应结构。
    
    Attributes:
        code: HTTP 状态码
        data: 响应数据
        description: 响应描述
        msg: 消息（可选）
        showTime: 前端显示时长（毫秒）
        valid: 请求是否有效
    """
    
    code: int = Field(
        default=200,
        description="HTTP 状态码",
    )
    
    data: Optional[T] = Field(
        default=None,
        description="响应数据",
    )
    
    description: str = Field(
        default="",
        description="响应描述",
    )
    
    msg: Optional[str] = Field(
        default=None,
        description="消息",
    )
    
    showTime: int = Field(
        default=2000,
        description="前端显示时长（毫秒）",
    )
    
    valid: bool = Field(
        default=True,
        description="请求是否有效",
    )


class SliderResponse(BaseResponse[str]):
    """
    滑块识别响应模型
    
    滑块识别接口的响应数据结构。
    """
    pass


class HealthData(BaseModel):
    """健康检查数据"""
    
    status: str = Field(
        default="healthy",
        description="服务状态",
    )


class HealthResponse(BaseResponse[HealthData]):
    """
    健康检查响应模型
    
    健康检查接口的响应数据结构。
    """
    pass


class EndpointInfo(BaseModel):
    """API 端点信息"""
    
    path: str = Field(description="端点路径")
    method: str = Field(description="HTTP 方法")
    description: str = Field(description="端点描述")


class ServiceInfo(BaseModel):
    """服务信息数据"""
    
    service: str = Field(description="服务名称")
    version: str = Field(description="服务版本")
    endpoints: list[EndpointInfo] = Field(description="可用端点列表")
    features: list[str] = Field(description="功能特性列表")


class ServiceInfoResponse(BaseResponse[ServiceInfo]):
    """
    服务信息响应模型
    
    根路径接口的响应数据结构。
    """
    pass


# ============================================================
# 响应工厂函数
# ============================================================

def create_response(
    code: int = 200,
    data: Any = None,
    description: str = "",
    msg: Optional[str] = None,
    show_time: int = 2000,
    valid: bool = True,
) -> dict:
    """
    创建标准响应字典
    
    工厂函数，用于创建符合标准格式的响应数据。
    
    Args:
        code: HTTP 状态码
        data: 响应数据
        description: 响应描述
        msg: 消息
        show_time: 前端显示时长（毫秒）
        valid: 请求是否有效
    
    Returns:
        标准格式的响应字典
    
    使用示例:
        >>> response = create_response(
        ...     code=200,
        ...     data={"result": "success"},
        ...     description="操作成功"
        ... )
    """
    return {
        "code": code,
        "data": data,
        "description": description,
        "msg": msg,
        "showTime": show_time,
        "valid": valid,
    }


def create_success_response(
    data: Any = None,
    description: str = "操作成功",
) -> dict:
    """
    创建成功响应
    
    快捷函数，用于创建成功状态的响应。
    
    Args:
        data: 响应数据
        description: 响应描述
    
    Returns:
        成功状态的响应字典
    
    使用示例:
        >>> response = create_success_response(
        ...     data="125",
        ...     description="计算成功"
        ... )
    """
    return create_response(
        code=200,
        data=data,
        description=description,
        valid=True,
    )


def create_error_response(
    code: int = 500,
    description: str = "服务器内部错误",
    msg: Optional[str] = None,
) -> dict:
    """
    创建错误响应
    
    快捷函数，用于创建错误状态的响应。
    
    Args:
        code: HTTP 状态码
        description: 错误描述
        msg: 额外的错误信息
    
    Returns:
        错误状态的响应字典
    
    使用示例:
        >>> response = create_error_response(
        ...     code=400,
        ...     description="参数错误: 图片 URL 无效"
        ... )
    """
    return create_response(
        code=code,
        data=None,
        description=description,
        msg=msg,
        valid=False,
    )


def create_service_info() -> dict:
    """
    创建服务信息响应
    
    生成包含服务基本信息的响应数据。
    
    Returns:
        服务信息响应字典
    """
    return create_response(
        code=200,
        data={
            "service": settings.app.name,
            "version": settings.app.version,
            "endpoints": [
                {
                    "path": "/api/slider/calc",
                    "method": "POST",
                    "description": "计算滑块距离（支持 URL 和 Base64）",
                },
                {
                    "path": "/api/arithmetic/calc",
                    "method": "POST",
                    "description": "识别算术验证码并计算结果",
                },
            ],
            "features": [
                "支持 URL 格式图片输入",
                "支持 Base64 格式图片输入",
                "支持 OCR 和 OpenCV 两种计算方法",
                "支持图片尺寸自适应缩放",
                "支持算术验证码识别与计算",
            ],
        },
        description="服务运行正常",
    )

