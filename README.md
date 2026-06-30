# FastAPI-Basic 通用后端API脚手架

基于FastAPI + SQLAlchemy2.0 + Alembic 搭建的标准化基础开发框架，采用src标准目录结构，内置统一返回、全局异常、JWT鉴权、日志、数据库迁移能力，可快速复用开发后台接口服务。

fastapi_basic/
├── src/ # 源码根目录
│ └── app/
│ ├── main.py # 项目启动入口
│ ├── api/ # 接口路由层
│ │ └── v1/ # v1 版本接口
│ ├── core/ # 核心配置、异常、鉴权、中间件
│ ├── crud/ # 数据库操作层
│ ├── db/ # 数据库连接会话
│ ├── models/ # ORM 数据表模型
│ ├── schemas/ # 请求 / 响应序列化模型
│ └── utils/ # 通用工具、统一返回、日志
├── migrations/ # Alembic 数据库 DDL 迁移文件
├── tests/ # 单元测试目录
├── .env # 本地环境配置（git 忽略）
├── .env.example # 环境变量模板（提交仓库）
├── pyproject.toml # Poetry 依赖管理配置
├── .gitignore # git 忽略文件
└── README.md # 项目说明文档

## 技术栈

- Python 3.14
- Web框架：FastAPI
- ASGI服务：Uvicorn
- 依赖管理：Poetry
- ORM：SQLAlchemy 2.0
- 数据库迁移：Alembic
- 配置管理：pydantic-settings
- 加密鉴权：JWT + passlib(bcrypt)
- 日志：Loguru
- 代码规范：ruff + black + isort
- 单元测试：pytest

## 环境安装

### 1. 初始化虚拟环境

```bash
    创建对应Python版本虚拟环境
    poetry env use python3.14

    安装全部依赖
    poetry install

    cp .env.example .env

    poetry run uvicorn app.main:app --reload --app-dir src --host 0.0.0.0 --port 8000
```

### 2. 创建migration

```bash
创建好model模型之后
详细用户，请参考sqlalchemy的数据迁移
在命令行下执行：
poetry run alembic revision --autogenerate -m "create 数据表名 table"
poetry run alembic upgrade head 执行数据迁移
```
