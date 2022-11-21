import redis
import logging

redis_connection = redis.Redis(host='localhost', port=6379)
logging.basicConfig(filename='user_logs.log', encoding='utf-8', level=logging.DEBUG)


class RedisService:

    def getter(self, key):
        try:
            return redis_connection.get(key)
        except redis.exceptions.RedisError as e:
            logging.exception(e)

    def setter(self, key, value):
        try:
            return redis_connection.set(key, value)
        except redis.exceptions.RedisError as e:
            logging.exception(e)