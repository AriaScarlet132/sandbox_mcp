FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# uv 用于根据 pyproject.toml + uv.lock 安装依赖
RUN pip install --no-cache-dir uv

# 先复制依赖定义以便缓存层复用
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
RUN /app/.venv/bin/python -c "import pydantic_settings; print('pydantic-settings OK')"

# 使用 uv 创建的虚拟环境运行，确保依赖可见
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# 再复制源码与运行所需目录
COPY src ./src
RUN mkdir -p /app/sandbox_storage

EXPOSE 8000 9000

CMD ["/app/.venv/bin/python", "-m", "app.run_all"]
