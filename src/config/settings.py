"""
应用配置设置

定义应用程序的所有配置项，支持从环境变量读取配置。
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ServerConfig:
    """服务器配置"""
    
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    workers: int = 1
    
    def __post_init__(self) -> None:
        """从环境变量加载配置"""
        self.host = os.getenv("SERVER_HOST", self.host)
        self.port = int(os.getenv("SERVER_PORT", self.port))
        self.debug = os.getenv("SERVER_DEBUG", "false").lower() == "true"
        self.workers = int(os.getenv("SERVER_WORKERS", self.workers))


@dataclass
class ImageConfig:
    """图片处理配置"""
    
    # 默认背景图宽度（像素），None 表示不缩放
    default_big_width: Optional[int] = None
    # 默认滑块图宽度（像素），None 表示不缩放
    default_small_width: Optional[int] = None
    # 推荐的背景图宽度
    recommended_big_width: int = 340
    # 推荐的滑块图宽度
    recommended_small_width: int = 68
    # 图片下载超时时间（秒）
    download_timeout: int = 10
    # 临时文件后缀
    temp_bg_suffix: str = ".jpg"
    temp_slider_suffix: str = ".png"
    
    def __post_init__(self) -> None:
        """从环境变量加载配置"""
        big_width = os.getenv("IMAGE_DEFAULT_BIG_WIDTH")
        small_width = os.getenv("IMAGE_DEFAULT_SMALL_WIDTH")
        
        if big_width:
            self.default_big_width = int(big_width)
        if small_width:
            self.default_small_width = int(small_width)
        
        self.download_timeout = int(os.getenv("IMAGE_DOWNLOAD_TIMEOUT", self.download_timeout))


@dataclass
class LogConfig:
    """日志配置"""
    
    level: str = "INFO"
    format: str = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
    date_format: str = "%Y-%m-%d %H:%M:%S"
    # 是否输出到文件
    file_output: bool = False
    file_path: str = "logs/app.log"
    # 日志文件最大大小（MB）
    max_file_size: int = 10
    # 保留的日志文件数量
    backup_count: int = 5
    
    def __post_init__(self) -> None:
        """从环境变量加载配置"""
        self.level = os.getenv("LOG_LEVEL", self.level).upper()
        self.file_output = os.getenv("LOG_FILE_OUTPUT", "false").lower() == "true"
        self.file_path = os.getenv("LOG_FILE_PATH", self.file_path)


@dataclass
class AppConfig:
    """应用配置"""
    
    name: str = "滑块验证码距离计算服务"
    version: str = "1.2.0"
    description: str = "基于 OCR 和 OpenCV 的滑块验证码距离计算 HTTP 服务"
    
    def __post_init__(self) -> None:
        """从环境变量加载配置"""
        self.name = os.getenv("APP_NAME", self.name)
        self.version = os.getenv("APP_VERSION", self.version)


@dataclass
class Settings:
    """
    应用程序全局配置
    
    统一管理所有配置项，支持从环境变量读取配置。
    
    使用示例:
        >>> from src.config import settings
        >>> print(settings.server.port)
        8000
        >>> print(settings.app.version)
        '1.2.0'
    """
    
    app: AppConfig = field(default_factory=AppConfig)
    server: ServerConfig = field(default_factory=ServerConfig)
    image: ImageConfig = field(default_factory=ImageConfig)
    log: LogConfig = field(default_factory=LogConfig)


# 全局配置实例（单例模式）
settings = Settings()

