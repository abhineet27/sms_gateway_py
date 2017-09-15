import redis

r = redis.Redis(
    host='localhost',
    port=6379)



def set(key, value, time):
        r.set(key,value,time)

def get(key):
    return r.get(key)

def update_cache(key):
    if None == r.get(key):
        r.set(key,1,24*60*60)
    else:
        r.incr(key,amount=1)
