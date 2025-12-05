"""
验证器工具

提供各种数据格式的验证函数。
"""

import re
from typing import Pattern

from src.logger import get_logger


logger = get_logger(__name__)

# Base64 字符串正则表达式（预编译以提高性能）
_BASE64_PATTERN: Pattern = re.compile(r"^[A-Za-z0-9+/]*={0,2}$")


def is_url(value: str) -> bool:
    """
    判断字符串是否为 URL
    
    检查字符串是否以 http:// 或 https:// 开头。
    
    Args:
        value: 待检查的字符串
    
    Returns:
        如果是 URL 返回 True，否则返回 False
    
    使用示例:
        >>> is_url("https://example.com/image.jpg")
        True
        >>> is_url("data:image/png;base64,iVBORw0KGgo...")
        False
    """
    if not value:
        return False
    
    result = value.startswith(("http://", "https://"))
    logger.debug(f"URL 检查: '{value[:50]}...' -> {result}")
    return result


def is_base64(value: str) -> bool:
    """
    判断字符串是否为 Base64 格式
    
    支持检测以下格式：
    - Data URI 格式: data:image/png;base64,iVBORw0KGgo...
    - 纯 Base64 字符串: iVBORw0KGgo...
    
    Args:
        value: 待检查的字符串
    
    Returns:
        如果是 Base64 格式返回 True，否则返回 False
    
    使用示例:
        >>> is_base64("data:image/png;base64,iVBORw0KGgo...")
        True
        >>> is_base64("iVBORw0KGgoAAAANSUhEUgAAAAEAAAAB")
        True
        >>> is_base64("https://example.com/image.jpg")
        False
    """
    if not value:
        return False
    
    # 检查是否是 Data URI 格式
    if value.startswith("data:"):
        logger.debug("检测到 Data URI 格式")
        return True
    
    # 检查纯 Base64 字符串
    value = value.strip()
    
    # Base64 字符串长度应该是 4 的倍数
    if len(value) % 4 != 0:
        logger.debug(f"Base64 检查失败: 长度 {len(value)} 不是 4 的倍数")
        return False
    
    # 检查是否只包含 Base64 字符
    result = bool(_BASE64_PATTERN.match(value))
    logger.debug(f"Base64 检查: 长度={len(value)}, 结果={result}")
    return result


def get_input_type(value: str) -> str:
    """
    获取输入类型
    
    判断输入是 URL、Base64 还是未知格式。
    
    Args:
        value: 输入值
    
    Returns:
        输入类型: "url", "base64", 或 "unknown"
    
    使用示例:
        >>> get_input_type("https://example.com/image.jpg")
        'url'
        >>> get_input_type("data:image/png;base64,...")
        'base64'
    """
    if is_url(value):
        return "url"
    elif is_base64(value):
        return "base64"
    else:
        return "unknown"

