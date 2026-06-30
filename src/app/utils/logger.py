import sys
from pathlib import Path
from loguru import logger
from app.core.config import settings

# 日志根目录
LOG_ROOT = Path("logs")
LOG_ROOT.mkdir(exist_ok=True)

# 日志格式
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "<level>{level: <8}</level> "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level>"
)

# 移除默认控制台输出
logger.remove()

# 1. 控制台输出（开发环境彩色）
logger.add(
    sink=sys.stderr,
    format=LOG_FORMAT,
    level="DEBUG" if settings.APP_ENV == "dev" else "INFO",
    colorize=True,
)

# 2. 全量日志文件：按天分割，保留7天
logger.add(
    sink=LOG_ROOT / "all_{time:YYYY-MM-DD}.log",
    format=LOG_FORMAT,
    rotation="00:00",  # 每日零点分割
    retention="7 days",
    encoding="utf-8",
    level="DEBUG",
    enqueue=True,  # 异步写入，避免接口阻塞
)

# 3. 错误日志单独文件（ERROR及以上级别）
logger.add(
    sink=LOG_ROOT / "error_{time:YYYY-MM-DD}.log",
    format=LOG_FORMAT,
    rotation="00:00",
    retention="30 days",
    encoding="utf-8",
    level="ERROR",
    enqueue=True,
)

# 对外导出日志对象
log = logger