FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# uv 用于根据 pyproject.toml + uv.lock 安装依赖
RUN pip install --no-cache-dir uv

# 先复制依赖定义以便缓存层复用
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 再复制源码与运行所需目录
COPY src ./src
RUN mkdir -p /app/sandbox_storage

EXPOSE 8000 9000

CMD ["python", "-m", "app.run_all"]
