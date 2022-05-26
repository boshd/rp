from redis_client.redis_client import RedisClient
from lru_cache.cache import LRUCache

class Proxy():
    def __init__(self, redis_host, redis_port, record_capacity, record_expiry):
        self.lru_cache = LRUCache(record_capacity, record_expiry)
        self.redis = RedisClient(redis_host, redis_port)

    def get(self, parsed_url):
        k = parsed_url.path.split('/')[2]

        v = self.lru_cache.get(k)
        if v != -1:
            print(f'retrieving value for key {k} from local cache. {v}')
            return v[0], True, b"cache"

        v = self.redis.get(k)
        if v != -1:
            print(f'retrieving value for key {k} from redis.')
            self.lru_cache.put(k, v)
            return v, True, b"redis"
        else:
            print('key not stored in cache or redis.')
            return '', False, None

    def put(self, k, v):
        self.redis.add(k, v)
        self.lru_cache.put(k, v)
        print(f'{k} - {v} added to cache and redis; updated cache size: {len(self.lru_cache.dict)} - {self.lru_cache.dict}')


