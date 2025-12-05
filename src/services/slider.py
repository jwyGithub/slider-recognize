"""
滑块识别服务

提供滑块验证码识别的业务逻辑封装。
"""

from typing import Optional

from src.core import recognize_by_ocr, recognize_by_opencv
from src.exceptions import RecognitionError
from src.logger import get_logger
from src.schemas import SliderRequest, RecognitionMethod


logger = get_logger(__name__)


class SliderService:
    """
    滑块识别服务类
    
    封装滑块验证码识别的业务逻辑，提供统一的识别接口。
    
    使用示例:
        >>> service = SliderService()
        >>> request = SliderRequest(
        ...     background_url="https://example.com/bg.jpg",
        ...     slider_url="https://example.com/slider.png"
        ... )
        >>> distance = service.calculate_distance(request)
        >>> print(f"滑块距离: {distance}")
    """
    
    def __init__(self) -> None:
        """初始化滑块识别服务"""
        logger.debug("SliderService 初始化")
    
    def calculate_distance(self, request: SliderRequest) -> int:
        """
        计算滑块距离
        
        根据请求参数选择合适的识别算法，计算滑块需要移动的距离。
        
        Args:
            request: 滑块识别请求对象
        
        Returns:
            滑块需要移动的像素距离（已应用偏移量校正）
        
        Raises:
            RecognitionError: 识别失败时
        
        处理流程:
            1. 记录请求参数
            2. 根据 method 选择识别算法
            3. 执行识别并获取原始距离
            4. 应用偏移量校正
            5. 返回最终距离
        """
        logger.info(
            f"开始计算滑块距离 | 方法: {request.method.value} | "
            f"偏移量: {request.offset}"
        )
        
        try:
            # 根据方法选择识别算法
            if request.method == RecognitionMethod.OPENCV:
                raw_distance = self._recognize_opencv(request)
            else:
                raw_distance = self._recognize_ocr(request)
            
            # 应用偏移量校正
            final_distance = raw_distance - request.offset
            
            # 确保距离不为负数
            if final_distance < 0:
                logger.warning(
                    f"计算结果为负数，已调整为 0 | "
                    f"原始: {raw_distance}, 偏移: {request.offset}"
                )
                final_distance = 0
            
            logger.info(
                f"滑块距离计算完成 | 原始: {raw_distance} | "
                f"偏移: {request.offset} | 最终: {final_distance}"
            )
            
            return final_distance
            
        except RecognitionError:
            # 重新抛出已知的识别异常
            raise
        except Exception as e:
            logger.error(f"计算滑块距离时发生未知错误: {e}")
            raise RecognitionError(
                message="计算滑块距离失败",
                details=str(e),
            )
    
    def _recognize_ocr(self, request: SliderRequest) -> int:
        """
        使用 OCR 方法识别
        
        Args:
            request: 滑块识别请求
        
        Returns:
            原始识别距离
        """
        logger.debug("使用 OCR 方法进行识别")
        
        return recognize_by_ocr(
            background_input=request.background_url,
            slider_input=request.slider_url,
            big_width=request.big_image_width,
            small_width=request.small_image_width,
            simple_target=True,
        )
    
    def _recognize_opencv(self, request: SliderRequest) -> int:
        """
        使用 OpenCV 方法识别
        
        Args:
            request: 滑块识别请求
        
        Returns:
            原始识别距离
        """
        logger.debug("使用 OpenCV 方法进行识别")
        
        return recognize_by_opencv(
            background_input=request.background_url,
            slider_input=request.slider_url,
            big_width=request.big_image_width,
            small_width=request.small_image_width,
        )
    
    @staticmethod
    def get_recommended_sizes() -> dict:
        """
        获取推荐的图片尺寸
        
        Returns:
            包含推荐尺寸的字典
        """
        from src.config import settings
        
        return {
            "big_image_width": settings.image.recommended_big_width,
            "small_image_width": settings.image.recommended_small_width,
        }

