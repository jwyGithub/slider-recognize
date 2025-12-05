"""
OpenCV 识别算法

使用 OpenCV 库实现滑块验证码距离识别。
"""

import os
import tempfile
from typing import Optional

import cv2
import numpy as np

from src.config import settings
from src.exceptions import OpenCVRecognitionError
from src.logger import get_logger
from src.utils import get_image_content, resize_image


logger = get_logger(__name__)


def recognize_by_opencv(
    background_input: str,
    slider_input: str,
    big_width: Optional[int] = None,
    small_width: Optional[int] = None,
) -> int:
    """
    使用 OpenCV 算法识别滑块距离
    
    基于 OpenCV 的模板匹配功能，通过图像处理和模板匹配
    计算滑块需要移动的像素距离。
    
    Args:
        background_input: 背景图片（URL 或 Base64）
        slider_input: 滑块图片（URL 或 Base64）
        big_width: 背景图目标宽度，None 表示不调整
        small_width: 滑块图目标宽度，None 表示不调整
    
    Returns:
        滑块需要移动的像素距离
    
    Raises:
        OpenCVRecognitionError: OpenCV 识别失败时
    
    使用示例:
        >>> distance = recognize_by_opencv(
        ...     background_input="https://example.com/bg.jpg",
        ...     slider_input="https://example.com/slider.png",
        ...     big_width=340,
        ...     small_width=68
        ... )
        >>> print(f"滑块距离: {distance} 像素")
    
    算法说明:
        1. 获取背景图和滑块图的字节内容
        2. 根据需要调整图片尺寸
        3. 将图片保存为临时文件（OpenCV 需要文件路径）
        4. 对背景图进行灰度转换和二值化处理
        5. 对滑块图进行预处理（透明区域处理）
        6. 使用模板匹配算法找到最佳匹配位置
        7. 返回匹配位置的 X 坐标
    """
    logger.info("开始 OpenCV 识别...")
    logger.debug(f"参数: big_width={big_width}, small_width={small_width}")
    
    bg_path: Optional[str] = None
    slider_path: Optional[str] = None
    
    try:
        # 获取图片内容
        logger.debug("获取背景图片内容...")
        bg_content = get_image_content(background_input)
        
        logger.debug("获取滑块图片内容...")
        slider_content = get_image_content(slider_input)
        
        # 调整图片尺寸（如果指定了尺寸）
        if big_width is not None:
            bg_content = resize_image(bg_content, big_width)
            logger.info(f"背景图已调整宽度至: {big_width}px")
        
        if small_width is not None:
            slider_content = resize_image(slider_content, small_width)
            logger.info(f"滑块图已调整宽度至: {small_width}px")
        
        # 保存到临时文件
        logger.debug("创建临时文件...")
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=settings.image.temp_bg_suffix,
        ) as bg_temp:
            bg_temp.write(bg_content)
            bg_path = bg_temp.name
        
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=settings.image.temp_slider_suffix,
        ) as slider_temp:
            slider_temp.write(slider_content)
            slider_path = slider_temp.name
        
        logger.debug(f"临时文件: bg={bg_path}, slider={slider_path}")
        
        # 执行 OpenCV 识别
        distance = _opencv_match(bg_path, slider_path)
        
        logger.info(f"OpenCV 识别完成: 距离={distance}")
        return distance
        
    except Exception as e:
        logger.error(f"OpenCV 识别失败: {e}")
        raise OpenCVRecognitionError(
            message="OpenCV 识别失败",
            details=str(e),
        )
    finally:
        # 清理临时文件
        _cleanup_temp_files(bg_path, slider_path)


def _opencv_match(bg_img_path: str, puzzle_image_path: str) -> int:
    """
    执行 OpenCV 模板匹配
    
    核心算法实现，不修改原有识别逻辑。
    
    Args:
        bg_img_path: 背景图片路径
        puzzle_image_path: 滑块图片路径
    
    Returns:
        匹配位置的 X 坐标
    """
    logger.debug("读取背景图片...")
    # 读取背景图片
    img = cv2.imdecode(
        np.fromfile(bg_img_path, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )
    
    logger.debug("读取滑块图片...")
    # 读取滑块图片
    tpl = cv2.imdecode(
        np.fromfile(puzzle_image_path, dtype=np.uint8),
        cv2.IMREAD_COLOR,
    )
    
    # 背景图灰度化和二值化
    logger.debug("处理背景图: 灰度化和二值化...")
    img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bw = cv2.threshold(img_gry, 127, 255, cv2.THRESH_BINARY)
    
    # 滑块图预处理
    logger.debug("处理滑块图: 透明区域处理...")
    tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    
    # 处理透明区域（将黑色像素替换为特定值）
    for row in range(tpl.shape[0]):
        for col in range(tpl.shape[1]):
            if tpl[row, col] == 0:
                tpl[row, col] = 96
    
    # 创建掩码并处理
    lower = np.array([96])
    upper = np.array([96])
    mask = cv2.inRange(tpl, lower, upper)
    tpl[mask == 0] = 0
    tpl[mask == 0] = 255
    
    # 模板匹配
    logger.debug("执行模板匹配...")
    result = cv2.matchTemplate(img_bw, tpl, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    
    distance = int(max_loc[0])
    logger.debug(f"模板匹配完成: max_loc={max_loc}, distance={distance}")
    
    return distance


def _cleanup_temp_files(*file_paths: Optional[str]) -> None:
    """
    清理临时文件
    
    Args:
        file_paths: 要清理的文件路径列表
    """
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
                logger.debug(f"已删除临时文件: {path}")
            except Exception as e:
                logger.warning(f"删除临时文件失败: {path}, 错误: {e}")
