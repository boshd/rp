import pytest, os, time
from redis_client import RedisClient

@pytest.fixture()
def resource():
    print('\n**************** Redis test ****************\n')
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    print(f'Initializing redis @ host: {redis_host} and port: {redis_port}')
    resource = RedisClient(redis_host, redis_port, 0)
    yield resource
    time.sleep(2)

class TestRedis():

    def test_simple_get_key(self, resource):
        print('\n**************** Testing simple get operation ****************')
        resource.add(1099, 122)
        print(f'-> Inserting (1099, 122) into redis...')
        print(f'-> Getting key 1099 from redis...')
        v = resource.get(1099)
        assert v.decode() == '122'

    def test_simple_put(self, resource):
        print('\n**************** Testing simple put operation ****************')
        k, v = 55, 599
        v = resource.add(k, v)
        assert v == True

    def test_get_key_not_in_redis(self, resource):
        print('\n**************** Testing get item not in redis ****************')
        v = resource.get(5094)
        print(f'-> Getting key 5094 from redis. Result: {v}')
        assert v == -1