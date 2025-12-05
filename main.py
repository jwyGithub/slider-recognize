#!/usr/bin/env python3
"""
滑块验证码距离计算服务 - 主入口

提供服务启动和命令行入口点。

使用方式:
    # 直接运行
    python main.py
    
    # 使用 uv 运行
    uv run python main.py
    
    # 使用 uvicorn 运行（支持热重载）
    uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

环境变量:
    SERVER_HOST: 服务器主机地址，默认 0.0.0.0
    SERVER_PORT: 服务器端口，默认 8000
    SERVER_DEBUG: 调试模式，默认 false
    LOG_LEVEL: 日志级别，默认 INFO
    LOG_FILE_OUTPUT: 是否输出到文件，默认 false
"""

import sys


def main() -> None:
    """
    服务启动入口
    
    初始化并启动 HTTP 服务器。
    
    处理流程:
        1. 初始化日志系统
        2. 设置信号处理器
        3. 创建应用实例
        4. 启动 uvicorn 服务器
    
    异常处理:
        - KeyboardInterrupt: 用户中断（Ctrl+C）
        - SystemExit: 系统退出信号
        - Exception: 其他未处理异常
    """
    import uvicorn
    
    from src.config import settings
    from src.exceptions.handlers import setup_signal_handlers
    from src.logger import setup_logging, get_logger
    
    # 初始化日志系统
    setup_logging()
    logger = get_logger(__name__)
    
    # 设置信号处理器（优雅退出）
    setup_signal_handlers(cleanup_callback=_cleanup_on_exit)
    
    try:
        logger.info("=" * 60)
        logger.info(f"启动 {settings.app.name}")
        logger.info(f"版本: {settings.app.version}")
        logger.info("=" * 60)
        
        # 启动服务器
        uvicorn.run(
            # 使用应用工厂模块中的 app 实例
            "src.app:app",
            host=settings.server.host,
            port=settings.server.port,
            reload=settings.server.debug,
            workers=settings.server.workers if not settings.server.debug else 1,
            # 日志配置（使用自定义日志系统）
            log_level="warning",  # 降低 uvicorn 日志级别，使用自定义日志
            access_log=settings.server.debug,
        )
        
    except KeyboardInterrupt:
        logger.info("收到键盘中断信号，正在退出...")
        sys.exit(0)
        
    except SystemExit as e:
        logger.info(f"收到系统退出信号: {e.code}")
        sys.exit(e.code)
        
    except Exception as e:
        logger.critical(f"服务启动失败: {e}", exc_info=True)
        sys.exit(1)


def _cleanup_on_exit() -> None:
    """
    退出时的清理回调
    
    在应用退出前执行必要的清理操作。
    """
    from src.logger import get_logger
    logger = get_logger(__name__)
    
    logger.info("执行退出清理...")
    
    # 清理临时文件
    try:
        import glob
        import os
        import tempfile
        
        temp_dir = tempfile.gettempdir()
        patterns = ["tmp*.jpg", "tmp*.png", "tmp*.jpeg"]
        
        for pattern in patterns:
            for file_path in glob.glob(os.path.join(temp_dir, pattern)):
                try:
                    os.remove(file_path)
                except Exception:
                    pass
    except Exception as e:
        logger.warning(f"清理临时文件时发生错误: {e}")
    
    logger.info("清理完成")


if __name__ == "__main__":
    main()
