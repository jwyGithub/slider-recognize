
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import tempfile
import os
from typing import Optional

from src.core import get_dis_x_ocr, get_dis_x_opencv
from src.image import get_image_content

app = FastAPI(title="滑块验证码距离计算服务")

# 请求模型
class SliderRequest(BaseModel):
    background_url: str  # 支持 URL 或 base64 格式
    slider_url: str      # 支持 URL 或 base64 格式
    method: Optional[str] = "ocr"  # 可选: "ocr" 或 "opencv"
    offset: Optional[int] = 0  # 偏移量，默认为 0
    big_image_width: Optional[int] = None  # 背景图缩放宽度，None表示不缩放
    small_image_width: Optional[int] = None  # 滑块图缩放宽度，None表示不缩放

# 响应模型
def create_response(code: int, data=None, description: str = "", msg=None, show_time: int = 2000, valid: bool = True):
    """创建标准响应格式"""
    return {
        "code": code,
        "data": data,
        "description": description,
        "msg": msg,
        "showTime": show_time,
        "valid": valid
    }

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return create_response(
        code=200,
        data={
            "service": "滑块验证码距离计算服务",
            "version": "1.1.0",
            "endpoints": [
                {"path": "/api/calc", "method": "POST", "description": "计算滑块距离（支持 URL 和 Base64）"}
            ],
            "features": [
                "支持 URL 格式图片输入",
                "支持 Base64 格式图片输入",
                "支持 OCR 和 OpenCV 两种计算方法"
            ]
        },
        description="服务运行正常"
    )


@app.post("/api/calc")
async def calculate_distance(request: SliderRequest):
    """
    计算滑块验证码的距离
    
    参数:
        background_url: 背景图片（支持 URL 或 base64 格式）
        slider_url: 滑块图片（支持 URL 或 base64 格式）
        method: 计算方法，可选 "ocr" 或 "opencv"，默认 "ocr"
        offset: 偏移量，计算结果会减去此值，默认 0
        big_image_width: 背景图缩放宽度（像素），None表示不缩放
        small_image_width: 滑块图缩放宽度（像素），None表示不缩放
    
    支持的格式:
        - URL: http://example.com/image.jpg
        - Base64: data:image/png;base64,iVBORw0KGgo...
        - Base64 (纯文本): iVBORw0KGgo...
    
    优化建议:
        - 如果识别率低，尝试调整图片尺寸
        - 推荐 big_image_width=340, small_image_width=68
        - 或根据实际验证码调整比例
    """
    try:
        if request.method == "opencv":
            # 获取图片内容
            bg_content = get_image_content(request.background_url)
            slider_content = get_image_content(request.slider_url)
            
            # 保存到临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as bg_temp:
                bg_temp.write(bg_content)
                bg_path = bg_temp.name
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as slider_temp:
                slider_temp.write(slider_content)
                slider_path = slider_temp.name
            
            try:
                result = get_dis_x_opencv(bg_path, slider_path)
            finally:
                # 清理临时文件
                os.unlink(bg_path)
                os.unlink(slider_path)
        else:
            # 默认使用OCR方法（优化版）
            result = get_dis_x_ocr(
                request.background_url, 
                request.slider_url,
                big_width=request.big_image_width,
                small_width=request.small_image_width,
                simple_target=True  # 使用 simple_target=True 提高识别率
            )
        
        print(f"result: {result}")
        print(f"request.offset: {request.offset}")
        # 减去偏移量并转换为字符串
        final_result = str(result - request.offset)
        
        return create_response(
            code=200,
            data=final_result,
            description="计算成功"
        )
    
    except ValueError as e:
        return create_response(
            code=400,
            data=None,
            description=f"参数错误: {str(e)}",
            valid=False
        )
    except Exception as e:
        return create_response(
            code=500,
            data=None,
            description=f"计算失败: {str(e)}",
            valid=False
        )

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return create_response(
        code=200,
        data={"status": "healthy"},
        description="服务正常运行"
    )


def main():
    """启动HTTP服务"""
    print("启动滑块验证码距离计算服务...")
    print("API文档: http://127.0.0.1:8000/docs")
    print("服务地址: http://127.0.0.1:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()

