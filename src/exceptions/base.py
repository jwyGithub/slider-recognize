"""
基础异常定义

定义应用程序中使用的所有自定义异常类。
"""

from typing import Optional, Any


class SliderRecognizeError(Exception):
    """
    滑块识别服务基础异常
    
    所有自定义异常的基类，提供统一的异常结构。
    
    Attributes:
        message: 错误信息
        code: 错误代码
        details: 额外的错误详情
    """
    
    def __init__(
        self,
        message: str = "滑块识别服务发生错误",
        code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        """
        初始化异常
        
        Args:
            message: 错误信息
            code: HTTP 状态码
            details: 额外的错误详情
        """
        self.message = message
        self.code = code
        self.details = details
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """返回异常的字符串表示"""
        if self.details:
            return f"{self.message} (详情: {self.details})"
        return self.message
    
    def to_dict(self) -> dict:
        """
        将异常转换为字典格式
        
        Returns:
            包含异常信息的字典
        """
        result = {
            "error": self.__class__.__name__,
            "message": self.message,
            "code": self.code,
        }
        if self.details:
            result["details"] = self.details
        return result


# ============================================================
# 图片相关异常
# ============================================================

class ImageError(SliderRecognizeError):
    """
    图片处理基础异常
    
    所有图片相关异常的基类。
    """
    
    def __init__(
        self,
        message: str = "图片处理失败",
        code: int = 400,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, code, details)


class ImageDownloadError(ImageError):
    """
    图片下载异常
    
    当从 URL 下载图片失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "图片下载失败",
        url: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.url = url
        if url:
            message = f"{message}: {url}"
        super().__init__(message, 400, details)


class ImageDecodeError(ImageError):
    """
    图片解码异常
    
    当 Base64 或其他格式图片解码失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "图片解码失败",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, 400, details)


class ImageProcessError(ImageError):
    """
    图片处理异常
    
    当图片缩放、转换等处理操作失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "图片处理失败",
        operation: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.operation = operation
        if operation:
            message = f"{message} (操作: {operation})"
        super().__init__(message, 500, details)


# ============================================================
# 识别相关异常
# ============================================================

class RecognitionError(SliderRecognizeError):
    """
    识别基础异常
    
    所有识别相关异常的基类。
    """
    
    def __init__(
        self,
        message: str = "滑块识别失败",
        code: int = 500,
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, code, details)


class OCRRecognitionError(RecognitionError):
    """
    OCR 识别异常
    
    当使用 OCR 方法识别失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "OCR 识别失败",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, 500, details)


class OpenCVRecognitionError(RecognitionError):
    """
    OpenCV 识别异常
    
    当使用 OpenCV 方法识别失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "OpenCV 识别失败",
        details: Optional[Any] = None,
    ) -> None:
        super().__init__(message, 500, details)


# ============================================================
# 其他异常
# ============================================================

class ValidationError(SliderRecognizeError):
    """
    参数验证异常
    
    当请求参数验证失败时抛出。
    """
    
    def __init__(
        self,
        message: str = "参数验证失败",
        field: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.field = field
        if field:
            message = f"{message}: {field}"
        super().__init__(message, 400, details)


class ConfigurationError(SliderRecognizeError):
    """
    配置异常
    
    当配置错误或缺失时抛出。
    """
    
    def __init__(
        self,
        message: str = "配置错误",
        config_key: Optional[str] = None,
        details: Optional[Any] = None,
    ) -> None:
        self.config_key = config_key
        if config_key:
            message = f"{message}: {config_key}"
        super().__init__(message, 500, details)

