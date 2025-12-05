"""
异常处理模块

提供统一的异常定义和处理机制。
"""

from src.exceptions.base import (
    SliderRecognizeError,
    ImageError,
    ImageDownloadError,
    ImageDecodeError,
    ImageProcessError,
    RecognitionError,
    OCRRecognitionError,
    OpenCVRecognitionError,
    ValidationError,
    ConfigurationError,
)
from src.exceptions.handlers import (
    register_exception_handlers,
    handle_exception,
)

__all__ = [
    # 基础异常
    "SliderRecognizeError",
    # 图片相关异常
    "ImageError",
    "ImageDownloadError",
    "ImageDecodeError",
    "ImageProcessError",
    # 识别相关异常
    "RecognitionError",
    "OCRRecognitionError",
    "OpenCVRecognitionError",
    # 其他异常
    "ValidationError",
    "ConfigurationError",
    # 处理器
    "register_exception_handlers",
    "handle_exception",
]

