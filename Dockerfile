FROM crpi-ylw7gpcmxpqjz8c6.cn-wulanchabu.personal.cr.aliyuncs.com/myvote/python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip install -r requirements.txt
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
