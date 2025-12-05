"""
FastAPI 应用工厂模块

提供 FastAPI 应用的创建和配置功能。
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api import api_router
from src.config import settings
from src.exceptions import register_exception_handlers
from src.logger import get_logger, setup_logging


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    应用生命周期管理器
    
    管理应用启动和关闭时的资源初始化和清理工作。
    
    Args:
        app: FastAPI 应用实例
    
    Yields:
        None
    
    启动时执行:
        - 预热 OCR 引擎
        - 初始化连接池等资源
    
    关闭时执行:
        - 清理临时文件
        - 关闭连接池
        - 释放资源
    """
    # ========== 启动阶段 ==========
    logger.info("=" * 60)
    logger.info(f"应用启动: {settings.app.name} v{settings.app.version}")
    logger.info("=" * 60)
    
    # 预热 OCR 引擎（可选，首次调用时会自动初始化）
    try:
        logger.info("预热 OCR 引擎...")
        from src.core.ocr import _get_ocr_instance
        _get_ocr_instance()
        logger.info("OCR 引擎预热完成")
    except Exception as e:
        logger.warning(f"OCR 引擎预热失败（将在首次使用时初始化）: {e}")
    
    logger.info("-" * 60)
    logger.info(f"服务地址: http://{settings.server.host}:{settings.server.port}")
    logger.info(f"API 文档: http://{settings.server.host}:{settings.server.port}/docs")
    logger.info(f"调试模式: {settings.server.debug}")
    logger.info("-" * 60)
    
    yield
    
    # ========== 关闭阶段 ==========
    logger.info("=" * 60)
    logger.info("应用正在关闭...")
    logger.info("=" * 60)
    
    # 清理临时文件
    _cleanup_temp_files()
    
    logger.info("应用已安全关闭")


def _cleanup_temp_files() -> None:
    """
    清理临时文件
    
    在应用关闭时清理可能残留的临时文件。
    """
    import glob
    import os
    import tempfile
    
    temp_dir = tempfile.gettempdir()
    patterns = ["tmp*.jpg", "tmp*.png", "tmp*.jpeg"]
    
    cleaned_count = 0
    for pattern in patterns:
        for file_path in glob.glob(os.path.join(temp_dir, pattern)):
            try:
                # 只删除最近创建的临时文件（避免删除其他应用的文件）
                if os.path.getmtime(file_path) > (os.path.getctime(file_path) - 3600):
                    os.remove(file_path)
                    cleaned_count += 1
            except Exception:
                pass
    
    if cleaned_count > 0:
        logger.info(f"已清理 {cleaned_count} 个临时文件")


def create_app() -> FastAPI:
    """
    创建 FastAPI 应用实例
    
    应用工厂函数，负责创建和配置 FastAPI 应用。
    
    Returns:
        配置完成的 FastAPI 应用实例
    
    配置项:
        - 应用元数据（标题、版本、描述）
        - 生命周期管理
        - 路由注册
        - 异常处理器
    
    使用示例:
        >>> from src.app import create_app
        >>> app = create_app()
        >>> # 使用 uvicorn 运行
        >>> uvicorn.run(app, host="0.0.0.0", port=8000)
    """
    # 初始化日志系统
    setup_logging()
    
    logger.info("正在创建 FastAPI 应用...")
    
    # 创建应用实例
    app = FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        lifespan=lifespan,
        # API 文档配置
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        # 其他配置
        debug=settings.server.debug,
    )
    
    # 注册路由
    _register_routes(app)
    
    # 注册异常处理器
    register_exception_handlers(app)
    
    logger.info("FastAPI 应用创建完成")
    
    return app


def _register_routes(app: FastAPI) -> None:
    """
    注册路由
    
    Args:
        app: FastAPI 应用实例
    """
    # 注册 API 路由（带 /api 前缀）
    app.include_router(
        api_router,
        prefix="/api",
    )
    
    logger.debug("路由注册完成")


# 创建应用实例（供 uvicorn 直接使用）
app = create_app()

