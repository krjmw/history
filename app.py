from flask import Flask, jsonify, request
import redis
import os
from prometheus_flask_exporter import PrometheusMetrics  # 新增

app = Flask(__name__)

# 初始化 Prometheus 监控，自动收集 HTTP 指标
metrics = PrometheusMetrics(app)
# 可选：添加静态信息
metrics.info("app_info", "History Service", version="1.0.0")

redis_host = os.getenv('REDIS_HOST', 'redis')
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)

@app.route('/history/<userId>', methods=['GET'])
def get_history(userId):
    items = r.lrange(f"user:{userId}:history", 0, 9)
    return jsonify({"userId": userId, "history": items})

@app.route('/history/<userId>/<itemId>', methods=['POST'])
def add_history(userId, itemId):
    r.lpush(f"user:{userId}:history", itemId)
    r.ltrim(f"user:{userId}:history", 0, 99)
    return jsonify({"status": "ok"}), 201

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "UP"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

