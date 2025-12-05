"""
异常处理器

提供 FastAPI 应用的全局异常处理功能。
"""

import sys
import signal
import traceback
from typing import Callable, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.base import SliderRecognizeError
from src.logger import get_logger
from src.schemas.response import create_error_response


logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """
    注册全局异常处理器
    
    为 FastAPI 应用注册统一的异常处理器，确保所有异常
    都能返回标准格式的错误响应。
    
    Args:
        app: FastAPI 应用实例
    
    使用示例:
        >>> from fastapi import FastAPI
        >>> from src.exceptions import register_exception_handlers
        >>> app = FastAPI()
        >>> register_exception_handlers(app)
    """
    
    @app.exception_handler(SliderRecognizeError)
    async def slider_recognize_error_handler(
        request: Request,
        exc: SliderRecognizeError,
    ) -> JSONResponse:
        """
        处理自定义业务异常
        
        Args:
            request: 请求对象
            exc: 异常实例
        
        Returns:
            标准格式的 JSON 错误响应
        """
        logger.warning(
            f"业务异常 | 路径: {request.url.path} | "
            f"类型: {exc.__class__.__name__} | "
            f"信息: {exc.message}"
        )
        
        return JSONResponse(
            status_code=exc.code,
            content=create_error_response(
                code=exc.code,
                description=exc.message,
            ),
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request,
        exc: ValueError,
    ) -> JSONResponse:
        """
        处理值错误异常
        
        Args:
            request: 请求对象
            exc: 异常实例
        
        Returns:
            标准格式的 JSON 错误响应
        """
        logger.warning(
            f"参数错误 | 路径: {request.url.path} | 信息: {str(exc)}"
        )
        
        return JSONResponse(
            status_code=400,
            content=create_error_response(
                code=400,
                description=f"参数错误: {str(exc)}",
            ),
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """
        处理未捕获的通用异常
        
        Args:
            request: 请求对象
            exc: 异常实例
        
        Returns:
            标准格式的 JSON 错误响应
        """
        # 记录完整的异常堆栈
        logger.error(
            f"未处理异常 | 路径: {request.url.path} | "
            f"类型: {exc.__class__.__name__} | "
            f"信息: {str(exc)}\n"
            f"堆栈追踪:\n{traceback.format_exc()}"
        )
        
        return JSONResponse(
            status_code=500,
            content=create_error_response(
                code=500,
                description=f"服务器内部错误: {str(exc)}",
            ),
        )
    
    logger.debug("异常处理器注册完成")


def handle_exception(exc: Exception, context: Optional[str] = None) -> None:
    """
    通用异常处理函数
    
    用于在非 HTTP 请求上下文中处理异常。
    
    Args:
        exc: 异常实例
        context: 异常发生的上下文描述
    
    使用示例:
        >>> try:
        ...     risky_operation()
        ... except Exception as e:
        ...     handle_exception(e, "执行危险操作时")
    """
    context_msg = f" [{context}]" if context else ""
    logger.error(
        f"异常{context_msg} | 类型: {exc.__class__.__name__} | "
        f"信息: {str(exc)}\n"
        f"堆栈追踪:\n{traceback.format_exc()}"
    )


def setup_signal_handlers(cleanup_callback: Optional[Callable] = None) -> None:
    """
    设置进程信号处理器
    
    处理 SIGINT (Ctrl+C) 和 SIGTERM 信号，确保应用能够优雅退出。
    
    Args:
        cleanup_callback: 清理回调函数，在退出前调用
    
    使用示例:
        >>> def cleanup():
        ...     print("执行清理操作...")
        >>> setup_signal_handlers(cleanup_callback=cleanup)
    """
    
    def signal_handler(signum: int, frame) -> None:
        """
        信号处理函数
        
        Args:
            signum: 信号编号
            frame: 当前栈帧
        """
        signal_name = signal.Signals(signum).name
        logger.info(f"收到 {signal_name} 信号，正在优雅退出...")
        
        # 执行清理回调
        if cleanup_callback:
            try:
                cleanup_callback()
                logger.info("清理操作完成")
            except Exception as e:
                logger.error(f"清理操作失败: {e}")
        
        logger.info("应用已退出")
        sys.exit(0)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    logger.debug("信号处理器设置完成")

