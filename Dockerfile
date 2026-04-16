FROM python:3.9-slim AS builder

WORKDIR /app
COPY requirements.txt .

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install --user -r requirements.txt

FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY app.py .

EXPOSE 5000
CMD ["python", "app.py"]
