# 1. Use a lightweight Python image
FROM python:3.11-slim

# 2. Install uv directly from the official binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Set the working directory
WORKDIR /app

# 4. Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# 5. Copy only the configuration files first
# This allows Docker to cache your "install" layer
COPY ./app .

# 6. Install dependencies
# --frozen: ensures uv.lock is not updated
# --no-cache: keeps the image size small
RUN uv sync --frozen --no-cache

# 8. Set environment variables
# This adds the uv-created virtualenv to the PATH
ENV PATH="/app/.venv/bin:$PATH"
ENV FLASK_APP=app.py
# Expose the default Flask port
EXPOSE 5000

# Run the Flask dev server
# --app specifies your file, --debug enables auto-reload
CMD ["uv", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]