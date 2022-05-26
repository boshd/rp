import logging, redis
from redis import Redis

class RedisClient():

    def __init__(self, redis_host = 'localhost', redis_port = 6379, redis_db = 0):
        self.r = Redis(host=redis_host, port=redis_port, db=redis_db)

    def add(self, k, v):
        try:
            return self.r.set(k, v)
        except redis.RedisError as e:
            logging.error('something went wrong // ', e)
            return

    def get(self, k):
        try:
            value = self.r.get(str(k))
        except redis.RedisError as e:
            logging.error('something went wrong // ', e)
            return -1
        return value if value else -1
