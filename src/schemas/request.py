"""
请求数据模型

定义 API 请求的数据结构和验证规则。
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RecognitionMethod(str, Enum):
    """
    识别方法枚举
    
    定义支持的滑块识别算法类型。
    
    Attributes:
        OCR: 使用 ddddocr 进行 OCR 识别
        OPENCV: 使用 OpenCV 进行模板匹配
    """
    
    OCR = "ocr"
    OPENCV = "opencv"


class ArithmeticRequest(BaseModel):
    """
    算术验证码识别请求模型
    
    定义算术验证码识别接口的请求参数。
    
    Attributes:
        img: 验证码图片（支持 URL 或 Base64 格式）
    
    使用示例:
        >>> request = ArithmeticRequest(
        ...     img="https://example.com/captcha.jpg"
        ... )
    """
    
    img: str = Field(
        ...,
        description="验证码图片，支持 URL 或 Base64 格式",
        examples=["https://example.com/captcha.jpg", "data:image/png;base64,iVBORw0KGgo..."],
    )
    
    @field_validator("img")
    @classmethod
    def validate_image_input(cls, value: str) -> str:
        """验证图片输入不为空"""
        if not value or not value.strip():
            raise ValueError("图片输入不能为空")
        return value.strip()
    
    class Config:
        """Pydantic 模型配置"""
        json_schema_extra = {
            "example": {
                "img": "https://example.com/captcha.jpg"
            }
        }


class SliderRequest(BaseModel):
    """
    滑块识别请求模型
    
    定义滑块验证码识别接口的请求参数。
    
    Attributes:
        background_url: 背景图片（支持 URL 或 Base64 格式）
        slider_url: 滑块图片（支持 URL 或 Base64 格式）
        method: 识别方法，默认为 OCR
        offset: 偏移量校正值，计算结果会减去此值
        big_image_width: 背景图缩放宽度（像素），None 表示不缩放
        small_image_width: 滑块图缩放宽度（像素），None 表示不缩放
    
    使用示例:
        >>> request = SliderRequest(
        ...     background_url="https://example.com/bg.jpg",
        ...     slider_url="https://example.com/slider.png",
        ...     method="ocr",
        ...     offset=0
        ... )
    """
    
    background_url: str = Field(
        ...,
        description="背景图片，支持 URL 或 Base64 格式",
        examples=["https://example.com/background.jpg", "data:image/png;base64,iVBORw0KGgo..."],
    )
    
    slider_url: str = Field(
        ...,
        description="滑块图片，支持 URL 或 Base64 格式",
        examples=["https://example.com/slider.png", "data:image/png;base64,iVBORw0KGgo..."],
    )
    
    method: RecognitionMethod = Field(
        default=RecognitionMethod.OCR,
        description="识别方法: 'ocr' (推荐) 或 'opencv'",
    )
    
    offset: int = Field(
        default=0,
        ge=0,
        description="偏移量校正值，计算结果会减去此值",
    )
    
    big_image_width: Optional[int] = Field(
        default=None,
        gt=0,
        le=2000,
        description="背景图缩放宽度（像素），推荐值: 340",
    )
    
    small_image_width: Optional[int] = Field(
        default=None,
        gt=0,
        le=500,
        description="滑块图缩放宽度（像素），推荐值: 68",
    )
    
    @field_validator("background_url", "slider_url")
    @classmethod
    def validate_image_input(cls, value: str) -> str:
        """
        验证图片输入
        
        确保图片输入不为空。
        
        Args:
            value: 图片输入值
        
        Returns:
            验证后的值
        
        Raises:
            ValueError: 当输入为空时
        """
        if not value or not value.strip():
            raise ValueError("图片输入不能为空")
        return value.strip()
    
    class Config:
        """Pydantic 模型配置"""
        
        # 生成 JSON Schema 时使用的标题
        json_schema_extra = {
            "example": {
                "background_url": "https://example.com/background.jpg",
                "slider_url": "https://example.com/slider.png",
                "method": "ocr",
                "offset": 0,
                "big_image_width": 340,
                "small_image_width": 68,
            }
        }

