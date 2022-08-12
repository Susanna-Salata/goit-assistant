import redis
from redis_lru import RedisLRU
import time

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)


if __name__ == '__main__':
    start = time.time()
    fibonacci(100)
    print(f'First execution time: {time.time() - start} s.')
    # First execution time: 0.24353432655334473 s.

    start = time.time()
    fibonacci(100)
    print(f'Execution time with cache: {time.time() - start} s.')
    # Execution time with cache: 0.0009982585906982422 s.