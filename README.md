# Slider Recognize

<div align="center">

**滑块验证码距离计算 HTTP 服务**

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0+-green.svg)](https://fastapi.tiangolo.com/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

## 📖 项目简介

Slider Recognize 是一个基于 FastAPI 的高性能滑块验证码识别服务，专门用于计算滑块验证码的距离。该项目提供了两种成熟的识别算法（OCR 和 OpenCV），支持多种图片输入格式，具有高精度和高可用性。

### ✨ 核心特性

-   🚀 **双算法支持**: 集成 ddddocr (OCR) 和 OpenCV 两种识别方法
-   🖼️ **多格式输入**: 支持 URL 和 Base64 两种图片格式
-   📏 **智能缩放**: 支持图片尺寸调整以提高识别准确率
-   ⚙️ **偏移量校正**: 支持自定义偏移量进行结果微调
-   🔌 **RESTful API**: 标准化的 HTTP 接口，易于集成
-   📚 **自动文档**: 内置 Swagger UI 和 ReDoc 文档
-   🏥 **健康检查**: 提供服务健康监控接口

## 🛠️ 技术栈

| 技术    | 版本     | 用途         |
| ------- | -------- | ------------ |
| Python  | 3.13+    | 编程语言     |
| FastAPI | 0.115.0+ | Web 框架     |
| ddddocr | 1.5.6+   | OCR 识别引擎 |
| OpenCV  | 4.11.0+  | 图像处理     |
| Pillow  | 12.0.0+  | 图像操作     |
| NumPy   | 2.3.5+   | 数值计算     |
| Uvicorn | 0.32.0+  | ASGI 服务器  |

## 📦 安装部署

### 环境要求

-   Python 3.13 或更高版本
-   pip 或 uv 包管理器

### 快速安装

#### 方式一：使用 uv（推荐）

```bash
# 克隆项目
git clone https://github.com/yourusername/slider-recognize.git
cd slider-recognize

# 安装 uv（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 同步依赖
uv sync

# 运行服务
uv run python main.py
```

#### 方式二：使用 pip

```bash
# 克隆项目
git clone https://github.com/yourusername/slider-recognize.git
cd slider-recognize

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -e .

# 运行服务
python main.py
```

### 服务启动

启动成功后，服务将运行在 `http://0.0.0.0:8000`

访问以下地址：

-   **API 文档**: http://127.0.0.1:8000/docs
-   **ReDoc 文档**: http://127.0.0.1:8000/redoc
-   **服务信息**: http://127.0.0.1:8000

## 📡 API 文档

### 1. 获取服务信息

```http
GET /
```

**响应示例**：

```json
{
    "code": 200,
    "data": {
        "service": "滑块验证码距离计算服务",
        "version": "1.2.0",
        "endpoints": [
            {
                "path": "/api/slider/calc",
                "method": "POST",
                "description": "计算滑块距离（支持 URL 和 Base64）"
            }
        ],
        "features": [
            "支持 URL 格式图片输入",
            "支持 Base64 格式图片输入",
            "支持 OCR 和 OpenCV 两种计算方法",
            "支持图片尺寸自适应缩放"
        ]
    },
    "description": "服务运行正常"
}
```

### 2. 计算滑块距离

```http
POST /api/slider/calc
```

**请求参数**：

| 参数              | 类型    | 必填 | 默认值 | 说明                        |
| ----------------- | ------- | ---- | ------ | --------------------------- |
| background_url    | string  | 是   | -      | 背景图片（URL 或 Base64）   |
| slider_url        | string  | 是   | -      | 滑块图片（URL 或 Base64）   |
| method            | string  | 否   | "ocr"  | 计算方法：`ocr` 或 `opencv` |
| offset            | integer | 否   | 0      | 偏移量，结果会减去此值      |
| big_image_width   | integer | 否   | null   | 背景图缩放宽度（像素）      |
| small_image_width | integer | 否   | null   | 滑块图缩放宽度（像素）      |

**请求示例**：

```json
{
    "background_url": "https://example.com/background.jpg",
    "slider_url": "https://example.com/slider.png",
    "method": "ocr",
    "offset": 0,
    "big_image_width": 340,
    "small_image_width": 68
}
```

**Base64 格式示例**：

```json
{
    "background_url": "data:image/png;base64,iVBORw0KGgo...",
    "slider_url": "data:image/png;base64,iVBORw0KGgo...",
    "method": "ocr"
}
```

**响应示例**：

```json
{
    "code": 200,
    "data": "125",
    "description": "计算成功",
    "msg": null,
    "showTime": 2000,
    "valid": true
}
```

### 3. 获取推荐尺寸

```http
GET /api/slider/recommended-sizes
```

**响应示例**：

```json
{
    "code": 200,
    "data": {
        "big_image_width": 340,
        "small_image_width": 68
    },
    "description": "获取推荐尺寸成功"
}
```

### 4. 健康检查

```http
GET /api/health
```

**响应示例**：

```json
{
    "code": 200,
    "data": {
        "status": "healthy"
    },
    "description": "服务正常运行"
}
```

## 💡 使用示例

### Python 调用示例

```python
import requests

# API 端点
url = "http://127.0.0.1:8000/api/slider/calc"

# 请求数据（使用 URL 格式）
payload = {
    "background_url": "https://example.com/background.jpg",
    "slider_url": "https://example.com/slider.png",
    "method": "ocr",
    "offset": 0,
    "big_image_width": 340,
    "small_image_width": 68
}

# 发送请求
response = requests.post(url, json=payload)
result = response.json()

print(f"滑块距离: {result['data']} 像素")
```

### cURL 调用示例

```bash
curl -X POST "http://127.0.0.1:8000/api/slider/calc" \
  -H "Content-Type: application/json" \
  -d '{
    "background_url": "https://example.com/background.jpg",
    "slider_url": "https://example.com/slider.png",
    "method": "ocr",
    "offset": 0,
    "big_image_width": 340,
    "small_image_width": 68
  }'
```

### JavaScript 调用示例

```javascript
// 使用 Fetch API
fetch('http://127.0.0.1:8000/api/slider/calc', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        background_url: 'https://example.com/background.jpg',
        slider_url: 'https://example.com/slider.png',
        method: 'ocr',
        offset: 0,
        big_image_width: 340,
        small_image_width: 68
    })
})
    .then(response => response.json())
    .then(data => {
        console.log('滑块距离:', data.data);
    })
    .catch(error => console.error('Error:', error));
```

## ⚙️ 配置说明

### 识别方法选择

项目支持两种识别方法：

#### 1. OCR 方法（推荐）

-   **优点**: 识别率高，适用范围广
-   **适用场景**: 标准滑块验证码
-   **参数**: `method: "ocr"`
-   **优化建议**:
    -   推荐图片尺寸：`big_image_width=340`, `small_image_width=68`
    -   使用 `simple_target=True`（默认）提高识别率

#### 2. OpenCV 方法

-   **优点**: 速度快，无需额外训练
-   **适用场景**: 图片对比度高的验证码
-   **参数**: `method: "opencv"`
-   **注意**: 需要提供本地文件路径或临时文件

### 图片尺寸优化

如果识别率不理想，建议调整图片尺寸：

```json
{
    "big_image_width": 340, // 背景图宽度
    "small_image_width": 68 // 滑块图宽度
}
```

### 偏移量校正

某些验证码存在像素偏差，可通过 `offset` 参数校正：

```json
{
    "offset": 5 // 最终结果会减去 5 像素
}
```

## 📂 项目结构

```
slider-recognize/
├── main.py                     # 服务启动入口
├── pyproject.toml              # 项目配置和依赖
├── uv.lock                     # 依赖锁定文件
├── README.md                   # 项目文档
├── LICENSE                     # 许可证
├── .python-version             # Python 版本
├── .gitignore                  # Git 忽略配置
└── src/                        # 源代码目录
    ├── __init__.py             # 包初始化和版本信息
    ├── app.py                  # FastAPI 应用工厂
    │
    ├── api/                    # HTTP API 模块
    │   ├── __init__.py
    │   ├── deps.py             # 依赖注入
    │   ├── router.py           # 路由注册
    │   └── routes/             # 路由定义
    │       ├── __init__.py
    │       ├── health.py       # 健康检查路由
    │       └── slider.py       # 滑块识别路由
    │
    ├── config/                 # 配置管理模块
    │   ├── __init__.py
    │   └── settings.py         # 配置定义
    │
    ├── core/                   # 核心算法模块
    │   ├── __init__.py
    │   ├── ocr.py              # OCR 识别算法
    │   └── opencv.py           # OpenCV 识别算法
    │
    ├── exceptions/             # 异常处理模块
    │   ├── __init__.py
    │   ├── base.py             # 异常基类定义
    │   └── handlers.py         # 全局异常处理器
    │
    ├── logger/                 # 日志管理模块
    │   ├── __init__.py
    │   └── setup.py            # 日志配置
    │
    ├── schemas/                # 数据模型模块
    │   ├── __init__.py
    │   ├── request.py          # 请求模型
    │   └── response.py         # 响应模型
    │
    ├── services/               # 业务服务模块
    │   ├── __init__.py
    │   └── slider.py           # 滑块识别服务
    │
    └── utils/                  # 工具函数模块
        ├── __init__.py
        ├── image.py            # 图片处理工具
        └── validators.py       # 数据验证工具
```

## 🌐 环境变量

| 变量名                    | 说明               | 默认值      |
| ------------------------- | ------------------ | ----------- |
| SERVER_HOST               | 服务器主机地址     | 0.0.0.0     |
| SERVER_PORT               | 服务器端口         | 8000        |
| SERVER_DEBUG              | 调试模式           | false       |
| SERVER_WORKERS            | 工作进程数         | 1           |
| LOG_LEVEL                 | 日志级别           | INFO        |
| LOG_FILE_OUTPUT           | 是否输出到文件     | false       |
| LOG_FILE_PATH             | 日志文件路径       | logs/app.log|
| IMAGE_DOWNLOAD_TIMEOUT    | 图片下载超时（秒） | 10          |
| IMAGE_DEFAULT_BIG_WIDTH   | 默认背景图宽度     | None        |
| IMAGE_DEFAULT_SMALL_WIDTH | 默认滑块图宽度     | None        |

## 🔧 开发指南

### 本地开发

```bash
# 安装开发依赖
uv sync

# 运行服务（开发模式，支持热重载）
uv run uvicorn src.app:app --reload --host 0.0.0.0 --port 8000

# 或使用 main.py 启动
uv run python main.py

# 访问 API 文档
open http://127.0.0.1:8000/docs
```

### 调试模式

```bash
# 启用调试模式
export SERVER_DEBUG=true
export LOG_LEVEL=DEBUG
uv run python main.py
```

### 运行测试

```bash
# TODO: 添加测试用例
pytest
```

## 🐛 常见问题

### Q1: 识别率不高怎么办？

**解决方案**：

1. 尝试调整图片尺寸，推荐 `big_image_width=340`, `small_image_width=68`
2. 切换识别方法：从 `ocr` 切换到 `opencv` 或反向
3. 调整 `offset` 参数进行微调

### Q2: Base64 格式报错？

**解决方案**：

-   确保 Base64 字符串完整
-   支持两种格式：
    -   带前缀：`data:image/png;base64,iVBORw0KGgo...`
    -   纯文本：`iVBORw0KGgo...`

### Q3: URL 下载失败？

**解决方案**：

-   检查网络连接
-   确认 URL 可访问
-   检查图片服务器是否设置了防盗链
-   设置超时时间（默认 10 秒）

### Q4: 服务启动失败？

**解决方案**：

1. 检查 Python 版本：`python --version`（需要 3.13+）
2. 确认依赖已安装：`uv sync` 或 `pip install -e .`
3. 检查端口占用：`lsof -i:8000`

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 📮 联系方式

如有问题或建议，欢迎提交 [Issue](https://github.com/yourusername/slider-recognize/issues)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个星标支持！**

</div>

