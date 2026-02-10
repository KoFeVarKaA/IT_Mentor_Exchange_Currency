FROM python:3.12-alpine

WORKDIR /app

COPY . .
RUN python3 -m pip install --upgrade pip && pip install uv
RUN uv venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

RUN uv sync
CMD ["python", "main.py"]