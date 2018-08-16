

import redis

# REDIS_KEY要和spiders/zhaopin.py下的redis_key一致
REDIS_KEY = 'zhaopin:start_urls'
r = redis.StrictRedis(host='192.168.52.105',port=6379)
# 由于不知道总页数，所以暂时获取500页
for i in range(1,501):
    url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=100&cityId=489&lastUrlQuery={%22p%22:'+str(i)+',%22jl%22:%22489%22}'
    r.rpush(REDIS_KEY,url)
