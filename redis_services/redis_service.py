import redis
from utils.logger import log
from common.configs import REDIS_DB, REDIS_HOST, REDIS_PORT, REDIS_PASSWORD
from common.constants import REDIS_TWITTER_USER_NAME_ID_CACHE

# 连接到本地的 Redis 服务器，默认端口 6379
client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, password=REDIS_PASSWORD)

def put_cache(k, v):
    client.set(k, v)

def get_cache(k):
    v = client.get(k)
    return v.decode("utf-8") if v else None


def test():
    # 测试连接
    if client.ping():
        log("成功连接到 Redis!")
        put_cache("k1", "20250201")
        log(get_cache("k1"))
        log(get_cache("k2"))
        log(get_cache(REDIS_TWITTER_USER_NAME_ID_CACHE + "Abelwang20242"))
        log("finish")
    else:
        log("连接失败!")


if __name__ == '__main__':
    test()

