"""
滑块识别路由

提供滑块验证码识别的 API 接口。
"""

from fastapi import APIRouter, Depends

from src.api.deps import get_slider_service
from src.logger import get_logger
from src.schemas import SliderRequest, create_success_response, create_error_response
from src.services import SliderService


logger = get_logger(__name__)

# 创建路由器
router = APIRouter()


@router.post(
    "/calc",
    summary="计算滑块距离",
    description="计算滑块验证码的距离，支持 URL 和 Base64 格式图片输入",
    response_description="滑块距离（像素）",
)
async def calculate_distance(
    request: SliderRequest,
    service: SliderService = Depends(get_slider_service),
):
    """
    计算滑块验证码的距离
    
    根据提供的背景图和滑块图，计算滑块需要移动的像素距离。
    
    Args:
        request: 滑块识别请求，包含以下参数：
            - background_url: 背景图片（URL 或 Base64）
            - slider_url: 滑块图片（URL 或 Base64）
            - method: 识别方法，'ocr'（推荐）或 'opencv'
            - offset: 偏移量校正值，默认 0
            - big_image_width: 背景图缩放宽度（可选）
            - small_image_width: 滑块图缩放宽度（可选）
        service: 滑块识别服务实例（依赖注入）
    
    Returns:
        标准响应，data 字段为计算出的距离（字符串格式）
    
    支持的图片格式:
        - URL: https://example.com/image.jpg
        - Data URI: data:image/png;base64,iVBORw0KGgo...
        - 纯 Base64: iVBORw0KGgo...
    
    优化建议:
        - 如果识别率低，尝试调整图片尺寸
        - 推荐 big_image_width=340, small_image_width=68
        - 或根据实际验证码调整比例
    
    示例请求:
        ```json
        {
            "background_url": "https://example.com/bg.jpg",
            "slider_url": "https://example.com/slider.png",
            "method": "ocr",
            "offset": 0,
            "big_image_width": 340,
            "small_image_width": 68
        }
        ```
    """
    logger.info(
        f"收到滑块识别请求 | 方法: {request.method.value} | "
        f"偏移: {request.offset}"
    )
    
    # 调用服务计算距离
    distance = service.calculate_distance(request)
    
    # 返回成功响应（距离转换为字符串格式）
    return create_success_response(
        data=str(distance),
        description="计算成功",
    )


@router.get(
    "/recommended-sizes",
    summary="获取推荐尺寸",
    description="获取推荐的图片缩放尺寸配置",
    response_description="推荐的图片尺寸配置",
)
async def get_recommended_sizes(
    service: SliderService = Depends(get_slider_service),
):
    """
    获取推荐的图片尺寸配置
    
    返回针对滑块识别优化的推荐图片尺寸参数。
    
    Returns:
        推荐的图片尺寸配置
    """
    logger.debug("收到获取推荐尺寸请求")
    
    sizes = service.get_recommended_sizes()
    
    return create_success_response(
        data=sizes,
        description="获取推荐尺寸成功",
    )

