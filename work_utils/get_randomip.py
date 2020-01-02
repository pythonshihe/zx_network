# -*- coding: utf-8 -*-
import redis
import time
import random

# redis连接池
# 外网
pool = redis.ConnectionPool(host="******", port=6379, db=15)
# todo 从池子里面取除值
redis_client = redis.Redis(connection_pool=pool, decode_responses=True)


def get_proxy():
    """
    获取代理
    """
    proxy = redis_client.srandmember("proxies")
    ip_port = proxy.decode("utf-8")

    proxies = {
        "http": "http://{}".format(ip_port),
        "https": "https://{}".format(ip_port)
    }
    time.sleep(0.05)
    return proxies


# redis zset类型获取ip
REDIS_KEY = "freeproxies"


def get_proxy_from_redis():
    proxy_list = redis_client.zrevrange(REDIS_KEY, 0, 150)
    proxy = random.choice(proxy_list)
    proxies = {
        'http:': 'http://{}'.format(proxy.decode('utf-8')),
        'https:': 'https://{}'.format(proxy.decode('utf-8')),
    }
    return proxies


if __name__ == '__main__':
    a = get_proxy_from_redis()
    print(a)
