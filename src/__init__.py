"""
滑块验证码距离计算服务

基于 OCR 和 OpenCV 的滑块验证码距离计算 HTTP 服务。

模块结构:
    - api/: HTTP API 路由和处理
    - config/: 应用配置管理
    - core/: 核心识别算法
    - exceptions/: 异常定义和处理
    - logger/: 日志配置
    - schemas/: 数据模型定义
    - services/: 业务逻辑服务
    - utils/: 工具函数

使用示例:
    >>> from src.app import create_app
    >>> app = create_app()
"""

__version__ = "1.2.0"
__author__ = "slider-recognize"
__description__ = "滑块验证码距离计算 HTTP 服务"

# 导出核心组件
from src.config import settings
from src.core import recognize_by_ocr, recognize_by_opencv
from src.services import SliderService
from src.schemas import SliderRequest, RecognitionMethod

__all__ = [
    # 版本信息
    "__version__",
    "__author__",
    "__description__",
    # 配置
    "settings",
    # 核心功能
    "recognize_by_ocr",
    "recognize_by_opencv",
    # 服务
    "SliderService",
    # 数据模型
    "SliderRequest",
    "RecognitionMethod",
]
