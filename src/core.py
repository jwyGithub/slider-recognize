import cv2
import ddddocr
import numpy as np
from src.image import get_image_content, resize_image


def get_dis_x_opencv(bg_img_path, puzzle_image_path):
    """使用OpenCV计算滑块距离"""
    img = cv2.imdecode(np.fromfile(bg_img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    tpl = cv2.imdecode(np.fromfile(puzzle_image_path, dtype=np.uint8), cv2.IMREAD_COLOR)

    img_gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bw = cv2.threshold(img_gry, 127, 255, cv2.THRESH_BINARY)

    tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    for row in range(tpl.shape[0]):
        for col in range(tpl.shape[1]):
            if tpl[row, col] == 0:
                tpl[row, col] = 96
    lower = np.array([96])
    upper = np.array([96])
    mask = cv2.inRange(tpl, lower, upper)
    tpl[mask == 0] = 0
    tpl[mask == 0] = 255

    result = cv2.matchTemplate(img_bw, tpl, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(result)
    distance = int(max_loc[0])

    return distance




def get_dis_x_ocr(background_input, slice_input, big_width=None, small_width=None, simple_target=True):
    """
    使用ddddocr计算滑块距离（优化版）
    
    参数:
        background_input: 背景图片（URL 或 base64）
        slice_input: 滑块图片（URL 或 base64）
        big_width: 背景图目标宽度，None表示不调整
        small_width: 滑块图目标宽度，None表示不调整
        simple_target: 是否为简单目标，True通常适用于标准滑块验证码
    """
    slide = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    
    # 获取图片内容（自动处理 URL 和 base64）
    slice_image = get_image_content(slice_input)
    bg_image = get_image_content(background_input)
    
    # 调整图片尺寸（如果指定了尺寸）
    if big_width is not None:
        bg_image = resize_image(bg_image, big_width)
        print(f"背景图已调整宽度至: {big_width}px")
    
    if small_width is not None:
        slice_image = resize_image(slice_image, small_width)
        print(f"滑块图已调整宽度至: {small_width}px")
    
    # 使用优化的参数进行匹配
    # simple_target=True 适用于大多数标准滑块验证码
    result = slide.slide_match(slice_image, bg_image, simple_target=simple_target)
    
    print(f"OCR识别结果: {result}")
    
    return result['target'][0]
