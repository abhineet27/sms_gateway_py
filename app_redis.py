import redis

r = redis.Redis(
    host='localhost',
    port=6379)



def set(key, value, time):
        r.set(key,value,time)
