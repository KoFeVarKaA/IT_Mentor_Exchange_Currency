FROM python:3.12-slim

RUN pip install uv
RUN uv venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

WORKDIR /app
COPY . .

RUN uv sync
CMD ["python", "main.py"]