import base64
import io
from PIL import Image
import requests
from src.utils import is_url


def get_image_content(image_input: str) -> bytes:
    """
    获取图片内容（支持 URL 和 base64）
    
    参数:
        image_input: URL 或 base64 编码的图片
    
    返回:
        图片的字节内容
    """
    if is_url(image_input):
        # 如果是 URL，下载图片
        response = requests.get(image_input, timeout=10)
        response.raise_for_status()
        return response.content
    else:
        # 如果是 base64，解码
        # 处理 data URI 格式 (data:image/png;base64,xxxxx)
        if image_input.startswith('data:'):
            # 提取 base64 部分
            base64_data = image_input.split(',', 1)[1] if ',' in image_input else image_input
        else:
            base64_data = image_input
        
        # 解码 base64
        try:
            return base64.b64decode(base64_data)
        except Exception as e:
            raise ValueError(f"无效的 base64 格式: {str(e)}")




def resize_image(image_bytes, target_width):
    """
    调整图片宽度，保持宽高比
    
    参数:
        image_bytes: 图片字节内容
        target_width: 目标宽度
    
    返回:
        调整后的图片字节内容
    """
    if target_width is None:
        return image_bytes
    
    # 打开图片
    img = Image.open(io.BytesIO(image_bytes))
    
    # 计算新的高度，保持宽高比
    width, height = img.size
    if width == target_width:
        return image_bytes
    
    aspect_ratio = height / width
    new_height = int(target_width * aspect_ratio)
    
    # 调整大小
    img_resized = img.resize((target_width, new_height), Image.LANCZOS)
    
    # 转换回字节
    output = io.BytesIO()
    img_format = img.format if img.format else 'PNG'
    img_resized.save(output, format=img_format)
    return output.getvalue()
