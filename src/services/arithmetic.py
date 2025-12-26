"""
算术验证码识别服务

提供算术验证码的 OCR 识别和计算功能。
"""

import re
from typing import Optional

import ddddocr

from src.exceptions import OCRRecognitionError
from src.logger import get_logger
from src.utils import get_image_content


logger = get_logger(__name__)

# 全局 OCR 实例（延迟初始化）
_arithmetic_ocr_instance: Optional[ddddocr.DdddOcr] = None


def _get_arithmetic_ocr_instance() -> ddddocr.DdddOcr:
    """
    获取算术识别 OCR 实例（单例模式）
    
    Returns:
        ddddocr.DdddOcr 实例（启用 OCR 功能）
    """
    global _arithmetic_ocr_instance
    
    if _arithmetic_ocr_instance is None:
        logger.info("初始化算术识别 OCR 引擎...")
        _arithmetic_ocr_instance = ddddocr.DdddOcr(show_ad=False)
        logger.info("算术识别 OCR 引擎初始化完成")
    
    return _arithmetic_ocr_instance


class ArithmeticService:
    """
    算术验证码识别服务
    
    提供算术验证码的识别和计算功能。
    
    使用示例:
        >>> service = ArithmeticService()
        >>> result = service.recognize_and_calculate("https://example.com/captcha.jpg")
        >>> print(result)  # 输出: 18
    """
    
    def __init__(self) -> None:
        """初始化服务"""
        self._ocr = _get_arithmetic_ocr_instance()
    
    def recognize_and_calculate(self, image_input: str) -> int:
        """
        识别算术验证码并计算结果
        
        Args:
            image_input: 图片输入（URL 或 Base64）
        
        Returns:
            计算结果（整数）
        
        Raises:
            OCRRecognitionError: 识别或计算失败时
        """
        logger.info("开始算术验证码识别...")
        
        try:
            # 获取图片内容
            image_bytes = get_image_content(image_input)
            
            # OCR 识别
            ocr_result = self._ocr.classification(image_bytes)
            logger.info(f"OCR 识别结果: {ocr_result}")
            
            # 解析并计算
            result = self._parse_and_calculate(ocr_result)
            logger.info(f"计算结果: {result}")
            
            return result
            
        except OCRRecognitionError:
            raise
        except Exception as e:
            logger.error(f"算术验证码识别失败: {e}")
            raise OCRRecognitionError(
                message="算术验证码识别失败",
                details=str(e),
            )
    
    def _parse_and_calculate(self, expression: str) -> int:
        """
        解析算术表达式并计算结果
        
        支持的运算符: +, -, *, x, ×, ÷, /
        
        Args:
            expression: OCR 识别的算术表达式字符串
        
        Returns:
            计算结果
        
        Raises:
            OCRRecognitionError: 解析或计算失败时
        """
        logger.debug(f"解析表达式: {expression}")
        
        # 清理表达式
        expr = expression.strip()
        
        # 移除等号及其后面的内容
        expr = re.split(r'[=＝]', expr)[0].strip()
        
        # 标准化运算符
        expr = expr.replace('×', '*').replace('x', '*').replace('X', '*')
        expr = expr.replace('÷', '/').replace('/', '/')
        expr = expr.replace('－', '-').replace('—', '-')
        expr = expr.replace('＋', '+')
        
        # 移除空格
        expr = expr.replace(' ', '')
        
        # 提取数字和运算符
        # 匹配: 数字 运算符 数字
        match = re.match(r'^(\d+)\s*([+\-*/])\s*(\d+)$', expr)
        
        if not match:
            logger.error(f"无法解析表达式: {expression} -> {expr}")
            raise OCRRecognitionError(
                message="无法解析算术表达式",
                details=f"原始: {expression}, 处理后: {expr}",
            )
        
        num1 = int(match.group(1))
        operator = match.group(2)
        num2 = int(match.group(3))
        
        logger.debug(f"解析结果: {num1} {operator} {num2}")
        
        # 计算
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise OCRRecognitionError(
                    message="除数不能为零",
                    details=f"{num1} / {num2}",
                )
            result = num1 // num2  # 整数除法
        else:
            raise OCRRecognitionError(
                message="不支持的运算符",
                details=f"运算符: {operator}",
            )
        
        return result

