"""
算术验证码识别路由

提供算术验证码识别的 API 接口。
"""

from fastapi import APIRouter, Depends

from src.api.deps import get_arithmetic_service
from src.logger import get_logger
from src.schemas import ArithmeticRequest, create_success_response
from src.services import ArithmeticService


logger = get_logger(__name__)

# 创建路由器
router = APIRouter()


@router.post(
    "/calc",
    summary="识别算术验证码",
    description="识别算术验证码图片并计算结果，支持 URL 和 Base64 格式图片输入",
    response_description="算术计算结果",
)
async def calculate_arithmetic(
    request: ArithmeticRequest,
    service: ArithmeticService = Depends(get_arithmetic_service),
):
    """
    识别算术验证码并计算结果
    
    根据提供的验证码图片，识别其中的算术表达式并计算结果。
    
    Args:
        request: 算术识别请求，包含以下参数：
            - img: 验证码图片（URL 或 Base64）
        service: 算术识别服务实例（依赖注入）
    
    Returns:
        标准响应，data 字段为计算结果（整数）
    
    支持的图片格式:
        - URL: https://example.com/captcha.jpg
        - Data URI: data:image/png;base64,iVBORw0KGgo...
        - 纯 Base64: iVBORw0KGgo...
    
    支持的运算:
        - 加法: 1+2, 1＋2
        - 减法: 5-3, 5－3
        - 乘法: 3*4, 3×4, 3x4
        - 除法: 8/2, 8÷2
    
    示例请求:
        ```json
        {
            "img": "https://example.com/captcha.jpg"
        }
        ```
    
    示例响应:
        ```json
        {
            "code": 200,
            "data": 18,
            "description": "识别成功",
            "valid": true
        }
        ```
    """
    logger.info(f"收到算术验证码识别请求")
    
    # 调用服务识别并计算
    result = service.recognize_and_calculate(request.img)
    
    # 返回成功响应
    return create_success_response(
        data=result,
        description="识别成功",
    )

