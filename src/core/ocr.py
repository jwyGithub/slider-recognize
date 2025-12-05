"""
OCR 识别算法

使用 ddddocr 库实现滑块验证码距离识别。
"""

from typing import Optional

import ddddocr

from src.exceptions import OCRRecognitionError
from src.logger import get_logger
from src.utils import get_image_content, resize_image


logger = get_logger(__name__)

# 全局 OCR 实例（延迟初始化，避免重复创建）
_ocr_instance: Optional[ddddocr.DdddOcr] = None


def _get_ocr_instance() -> ddddocr.DdddOcr:
    """
    获取 OCR 实例（单例模式）
    
    使用延迟初始化和单例模式，避免重复创建 OCR 实例。
    
    Returns:
        ddddocr.DdddOcr 实例
    """
    global _ocr_instance
    
    if _ocr_instance is None:
        logger.info("初始化 OCR 引擎...")
        _ocr_instance = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
        logger.info("OCR 引擎初始化完成")
    
    return _ocr_instance


def recognize_by_ocr(
    background_input: str,
    slider_input: str,
    big_width: Optional[int] = None,
    small_width: Optional[int] = None,
    simple_target: bool = True,
) -> int:
    """
    使用 OCR 算法识别滑块距离
    
    基于 ddddocr 库的 slide_match 功能，通过模板匹配
    计算滑块需要移动的像素距离。
    
    Args:
        background_input: 背景图片（URL 或 Base64）
        slider_input: 滑块图片（URL 或 Base64）
        big_width: 背景图目标宽度，None 表示不调整
        small_width: 滑块图目标宽度，None 表示不调整
        simple_target: 是否为简单目标，True 通常适用于标准滑块验证码
    
    Returns:
        滑块需要移动的像素距离
    
    Raises:
        OCRRecognitionError: OCR 识别失败时
    
    使用示例:
        >>> distance = recognize_by_ocr(
        ...     background_input="https://example.com/bg.jpg",
        ...     slider_input="https://example.com/slider.png",
        ...     big_width=340,
        ...     small_width=68
        ... )
        >>> print(f"滑块距离: {distance} 像素")
    
    算法说明:
        1. 获取并处理背景图和滑块图
        2. 根据需要调整图片尺寸
        3. 使用 ddddocr 的 slide_match 进行模板匹配
        4. 返回匹配位置的 X 坐标
    """
    logger.info("开始 OCR 识别...")
    logger.debug(f"参数: big_width={big_width}, small_width={small_width}, simple_target={simple_target}")
    
    try:
        # 获取 OCR 实例
        ocr = _get_ocr_instance()
        
        # 获取图片内容
        logger.debug("获取滑块图片内容...")
        slider_image = get_image_content(slider_input)
        
        logger.debug("获取背景图片内容...")
        background_image = get_image_content(background_input)
        
        # 调整图片尺寸
        if big_width is not None:
            background_image = resize_image(background_image, big_width)
            logger.info(f"背景图已调整宽度至: {big_width}px")
        
        if small_width is not None:
            slider_image = resize_image(slider_image, small_width)
            logger.info(f"滑块图已调整宽度至: {small_width}px")
        
        # 执行 OCR 识别
        logger.debug("执行 slide_match 匹配...")
        result = ocr.slide_match(slider_image, background_image, simple_target=simple_target)
        
        # 提取距离
        distance = result["target"][0]
        
        logger.info(f"OCR 识别完成: 原始结果={result}, 距离={distance}")
        return distance
        
    except Exception as e:
        logger.error(f"OCR 识别失败: {e}")
        raise OCRRecognitionError(
            message="OCR 识别失败",
            details=str(e),
        )

