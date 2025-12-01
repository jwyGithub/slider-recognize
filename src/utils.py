import re


def is_base64(s: str) -> bool:
    """
    判断字符串是否为 base64 格式
    支持带有 data:image/... 前缀的 base64 字符串
    """
    # 检查是否是 data URI 格式
    if s.startswith('data:'):
        return True
    
    # 检查是否是纯 base64 字符串（去除可能的空白字符）
    s = s.strip()
    
    # base64 字符串长度应该是 4 的倍数
    if len(s) % 4 != 0:
        return False
    
    # 检查是否只包含 base64 字符
    base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
    return bool(base64_pattern.match(s))


def is_url(s: str) -> bool:
    """判断字符串是否为 URL"""
    return s.startswith(('http://', 'https://'))

