from flask import Flask, jsonify, request
import redis
import os

app = Flask(__name__)

# 从环境变量读取 Redis 地址，默认值为 'redis'，修改一下
redis_host = os.getenv('REDIS_HOST', 'redis')
r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)


@app.route('/history/<userId>', methods=['GET'])
def get_history(userId):
    """获取用户浏览历史（最多最近10条）"""
    items = r.lrange(f"user:{userId}:history", 0, 9)
    return jsonify({"userId": userId, "history": items})


@app.route('/history/<userId>/<itemId>', methods=['POST'])
def add_history(userId, itemId):
    """记录浏览，加到列表左边（最近浏览在第一个）"""
    r.lpush(f"user:{userId}:history", itemId)
    # 只保留最近100条
    r.ltrim(f"user:{userId}:history", 0, 99)
    return jsonify({"status": "ok"}), 201


@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    return jsonify({"status": "UP"})


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000)
