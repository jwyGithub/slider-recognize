"""
健康检查路由

提供服务健康状态检查接口。
"""

from fastapi import APIRouter

from src.logger import get_logger
from src.schemas import create_response, create_service_info


logger = get_logger(__name__)

# 创建路由器
router = APIRouter()


@router.get(
    "/",
    summary="服务信息",
    description="获取服务基本信息和可用接口列表",
    response_description="服务信息",
)
async def root():
    """
    获取服务信息
    
    返回服务的基本信息，包括：
    - 服务名称和版本
    - 可用的 API 端点
    - 支持的功能特性
    
    Returns:
        服务信息响应
    """
    logger.debug("收到根路径请求")
    return create_service_info()


@router.get(
    "/health",
    summary="健康检查",
    description="检查服务是否正常运行",
    response_description="健康状态",
)
async def health_check():
    """
    健康检查接口
    
    用于监控服务的运行状态，适用于负载均衡器或
    容器编排系统的健康检查。
    
    Returns:
        健康状态响应
    """
    logger.debug("收到健康检查请求")
    
    return create_response(
        code=200,
        data={"status": "healthy"},
        description="服务正常运行",
    )

