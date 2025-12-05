"""
图片处理工具

提供图片下载、解码和处理功能。
"""

import base64
import io
from typing import Optional

import requests
from PIL import Image

from src.config import settings
from src.exceptions import ImageDownloadError, ImageDecodeError, ImageProcessError
from src.logger import get_logger
from src.utils.validators import is_url


logger = get_logger(__name__)


def get_image_content(image_input: str) -> bytes:
    """
    获取图片内容
    
    支持从 URL 下载或从 Base64 解码获取图片字节内容。
    
    Args:
        image_input: 图片输入，支持以下格式：
            - URL: https://example.com/image.jpg
            - Data URI: data:image/png;base64,iVBORw0KGgo...
            - 纯 Base64: iVBORw0KGgo...
    
    Returns:
        图片的字节内容
    
    Raises:
        ImageDownloadError: URL 下载失败时
        ImageDecodeError: Base64 解码失败时
    
    使用示例:
        >>> content = get_image_content("https://example.com/image.jpg")
        >>> print(len(content))
        12345
    """
    if is_url(image_input):
        return _download_image(image_input)
    else:
        return _decode_base64_image(image_input)


def _download_image(url: str) -> bytes:
    """
    从 URL 下载图片
    
    Args:
        url: 图片 URL
    
    Returns:
        图片字节内容
    
    Raises:
        ImageDownloadError: 下载失败时
    """
    logger.info(f"开始下载图片: {url[:100]}...")
    
    try:
        response = requests.get(
            url,
            timeout=settings.image.download_timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
        )
        response.raise_for_status()
        
        content = response.content
        logger.info(f"图片下载成功: 大小={len(content)} 字节")
        return content
        
    except requests.Timeout as e:
        logger.error(f"图片下载超时: {url}")
        raise ImageDownloadError(
            message="图片下载超时",
            url=url,
            details=str(e),
        )
    except requests.RequestException as e:
        logger.error(f"图片下载失败: {url}, 错误: {e}")
        raise ImageDownloadError(
            message="图片下载失败",
            url=url,
            details=str(e),
        )


def _decode_base64_image(image_input: str) -> bytes:
    """
    解码 Base64 图片
    
    Args:
        image_input: Base64 编码的图片
    
    Returns:
        图片字节内容
    
    Raises:
        ImageDecodeError: 解码失败时
    """
    logger.debug("开始解码 Base64 图片")
    
    try:
        # 处理 Data URI 格式 (data:image/png;base64,xxxxx)
        if image_input.startswith("data:"):
            # 提取 Base64 部分
            if "," in image_input:
                base64_data = image_input.split(",", 1)[1]
            else:
                base64_data = image_input
            logger.debug("已提取 Data URI 中的 Base64 数据")
        else:
            base64_data = image_input
        
        # 解码 Base64
        content = base64.b64decode(base64_data)
        logger.info(f"Base64 解码成功: 大小={len(content)} 字节")
        return content
        
    except Exception as e:
        logger.error(f"Base64 解码失败: {e}")
        raise ImageDecodeError(
            message="无效的 Base64 格式",
            details=str(e),
        )


def resize_image(image_bytes: bytes, target_width: Optional[int]) -> bytes:
    """
    调整图片宽度
    
    保持宽高比调整图片到指定宽度。
    
    Args:
        image_bytes: 原始图片字节内容
        target_width: 目标宽度（像素），None 表示不调整
    
    Returns:
        调整后的图片字节内容
    
    Raises:
        ImageProcessError: 处理失败时
    
    使用示例:
        >>> resized = resize_image(original_bytes, target_width=340)
    """
    if target_width is None:
        return image_bytes
    
    logger.debug(f"开始调整图片尺寸: 目标宽度={target_width}px")
    
    try:
        # 打开图片
        img = Image.open(io.BytesIO(image_bytes))
        original_width, original_height = img.size
        
        # 如果宽度已经匹配，直接返回
        if original_width == target_width:
            logger.debug(f"图片宽度已匹配，无需调整")
            return image_bytes
        
        # 计算新的高度，保持宽高比
        aspect_ratio = original_height / original_width
        new_height = int(target_width * aspect_ratio)
        
        # 调整大小
        img_resized = img.resize((target_width, new_height), Image.LANCZOS)
        
        # 转换回字节
        output = io.BytesIO()
        img_format = img.format if img.format else "PNG"
        img_resized.save(output, format=img_format)
        result = output.getvalue()
        
        logger.info(
            f"图片尺寸调整完成: {original_width}x{original_height} -> "
            f"{target_width}x{new_height}, 大小: {len(result)} 字节"
        )
        return result
        
    except Exception as e:
        logger.error(f"图片尺寸调整失败: {e}")
        raise ImageProcessError(
            message="图片尺寸调整失败",
            operation="resize",
            details=str(e),
        )

