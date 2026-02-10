FROM python:3.12-alpine

COPY . .
RUN python3 -m pip install --upgrade pip && pip install uv
RUN uv venv /app/.venv
ENV PATH=/app/.venv/bin:$PATH

WORKDIR /app


RUN uv sync
CMD ["python", "main.py"]