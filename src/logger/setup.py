"""
日志配置设置

提供日志系统的初始化和配置功能。
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from src.config import settings


def setup_logging(
    level: Optional[str] = None,
    log_format: Optional[str] = None,
    date_format: Optional[str] = None,
) -> None:
    """
    设置日志系统
    
    初始化应用程序的日志配置，支持控制台和文件输出。
    
    Args:
        level: 日志级别，默认从配置读取
        log_format: 日志格式，默认从配置读取
        date_format: 日期格式，默认从配置读取
    
    使用示例:
        >>> from src.logger import setup_logging
        >>> setup_logging()
        >>> # 或自定义配置
        >>> setup_logging(level="DEBUG")
    """
    config = settings.log
    
    # 使用参数或默认配置
    log_level = getattr(logging, level or config.level, logging.INFO)
    fmt = log_format or config.format
    dfmt = date_format or config.date_format
    
    # 创建根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除现有处理器
    root_logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(fmt=fmt, datefmt=dfmt)
    
    # 添加控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # 如果启用文件输出，添加文件处理器
    if config.file_output:
        _add_file_handler(root_logger, formatter, log_level)
    
    # 设置第三方库的日志级别（避免过多输出）
    _configure_third_party_loggers()
    
    # 记录日志系统初始化完成
    logger = get_logger(__name__)
    logger.info("日志系统初始化完成")
    logger.debug(f"日志级别: {config.level}, 文件输出: {config.file_output}")


def _add_file_handler(
    logger: logging.Logger,
    formatter: logging.Formatter,
    level: int,
) -> None:
    """
    添加文件处理器
    
    Args:
        logger: 日志记录器
        formatter: 日志格式化器
        level: 日志级别
    """
    config = settings.log
    
    # 确保日志目录存在
    log_path = Path(config.file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 创建轮转文件处理器
    file_handler = RotatingFileHandler(
        filename=config.file_path,
        maxBytes=config.max_file_size * 1024 * 1024,  # 转换为字节
        backupCount=config.backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def _configure_third_party_loggers() -> None:
    """配置第三方库的日志级别"""
    # 降低 uvicorn 的日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    
    # 降低 httpx/httpcore 的日志级别
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # 降低 PIL 的日志级别
    logging.getLogger("PIL").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志记录器
    
    Args:
        name: 日志记录器名称，通常使用 __name__
    
    Returns:
        配置好的日志记录器实例
    
    使用示例:
        >>> from src.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("这是一条信息日志")
        >>> logger.error("这是一条错误日志")
    """
    return logging.getLogger(name)

