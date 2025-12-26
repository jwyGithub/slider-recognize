"""
依赖注入模块

提供 FastAPI 路由的依赖注入函数。
"""

from typing import Generator

from src.services import SliderService, ArithmeticService


def get_slider_service() -> Generator[SliderService, None, None]:
    """
    获取滑块识别服务实例

    FastAPI 依赖注入函数，用于在路由处理函数中注入服务实例。

    Yields:
        SliderService 实例

    使用示例:
        >>> from fastapi import Depends
        >>> from src.api.deps import get_slider_service
        >>> from src.services import SliderService
        >>>
        >>> @router.post("/calc")
        >>> async def calculate(service: SliderService = Depends(get_slider_service)):
        ...     return service.calculate_distance(...)
    """
    service = SliderService()
    try:
        yield service
    finally:
        # 清理资源（如果需要）
        pass


def get_arithmetic_service() -> Generator[ArithmeticService, None, None]:
    """
    获取算术识别服务实例

    FastAPI 依赖注入函数，用于在路由处理函数中注入服务实例。

    Yields:
        ArithmeticService 实例

    使用示例:
        >>> from fastapi import Depends
        >>> from src.api.deps import get_arithmetic_service
        >>> from src.services import ArithmeticService
        >>>
        >>> @router.post("/calc")
        >>> async def calculate(service: ArithmeticService = Depends(get_arithmetic_service)):
        ...     return service.recognize_and_calculate(...)
    """
    service = ArithmeticService()
    try:
        yield service
    finally:
        # 清理资源（如果需要）
        pass

