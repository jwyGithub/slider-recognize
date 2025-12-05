# 滑块验证码距离计算服务 Docker 镜像
# 优化体积版本 - 基于 Python 3.12 slim
# 注意: ddddocr 不支持 Python 3.13

# ============================
# 构建阶段
# ============================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装构建依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件
COPY pyproject.toml ./

# 创建虚拟环境并安装依赖
# 使用 opencv-python-headless 替代 opencv-python 减小体积
RUN python -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install \
        "ddddocr>=1.5.6" \
        "fastapi>=0.115.0" \
        "numpy>=2.0.0" \
        "opencv-python-headless>=4.8.0" \
        "pillow>=10.0.0" \
        "python-multipart>=0.0.17" \
        "requests>=2.31.0" \
        "uvicorn>=0.32.0" && \
    # 清理不必要的文件
    find /opt/venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type f -name "*.pyc" -delete && \
    find /opt/venv -type f -name "*.pyo" -delete && \
    find /opt/venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /opt/venv -type d -name "test" -exec rm -rf {} + 2>/dev/null || true && \
    rm -rf /opt/venv/lib/python3.12/site-packages/pip* && \
    rm -rf /opt/venv/lib/python3.12/site-packages/setuptools* && \
    rm -rf /opt/venv/lib/python3.12/site-packages/wheel*

# ============================
# 运行阶段
# ============================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    # 应用配置
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8000 \
    SERVER_DEBUG=false \
    SERVER_WORKERS=1 \
    LOG_LEVEL=INFO \
    LOG_FILE_OUTPUT=false

# 安装最小运行时依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && rm -rf /var/cache/apt/archives/*

# 从构建阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 创建非 root 用户
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash --create-home appuser

WORKDIR /app

# 只复制必要的应用代码
COPY --chown=appuser:appgroup main.py ./
COPY --chown=appuser:appgroup src ./src

USER appuser

EXPOSE 8000

# 使用 Python 进行健康检查（无需安装 curl）
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["python", "main.py"]
