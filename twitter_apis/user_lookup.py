# https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_bearer_token.py
# https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py

import requests
import json
from redis_services.redis_service import put_cache, get_cache
from utils.logger import log
from common.configs import TWITTER_BEARER_TOKEN
from common.constants import REDIS_TWITTER_USER_NAME_ID_CACHE
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class GetTwitterIdInput(BaseModel):
    usernames: list[str] = Field(description="twitter上的用户名列表")

@tool("get_twitter_id_by_username", args_schema=GetTwitterIdInput)
def get_twitter_id_with_cache(usernames: list[str]) -> dict[str, str]:
    '''
    用来通过twitter的用户名查询twitter_id，返回的数据格式为{'twitter用户名':'twitter_id'}
    '''
    cache = {x: get_cache(REDIS_TWITTER_USER_NAME_ID_CACHE+x) for x in usernames if get_cache(REDIS_TWITTER_USER_NAME_ID_CACHE+x) is not None}
    log(cache=cache)

    remain = usernames - cache.keys()
    if remain and len(remain) > 0:
        remain_cache = get_twitter_id(remain)
        if remain_cache and len(remain_cache) > 0:
            put_to_cache(remain_cache)
            cache.update(remain_cache)
        log(remain_cache=remain_cache)

    return cache

def put_to_cache(remain_cache):
    for k,v in remain_cache.items():
        put_cache(REDIS_TWITTER_USER_NAME_ID_CACHE+k, v)

def get_twitter_id(usernames):
    url = "https://api.x.com/2/users/by"
    querystring = {"usernames": str.join(",", usernames)}
    print(querystring)
    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    log(f'status_code:{response.status_code}, text:{response.text}')
    json_response = json.loads(response.text)
    return {x['username'] : x['id'] for x in json_response["data"]}

def test2():
    data = '''
        {
      "data": [
        {
          "created_at": "2013-12-14T04:35:55Z",
          "id": "22449949451",
          "name": "X Dev",
          "protected": false,
          "username": "TwitterDev1"
        },
        {
          "created_at": "2013-12-14T04:35:55Z",
          "id": "22449949452",
          "name": "X Dev",
          "protected": false,
          "username": "TwitterDev2"
        }
      ]
      }
    '''
    log(f'data:{data}')
    json_response = json.loads(data)
    result = {x['username']: x['id'] for x in json_response["data"]}
    print(result)

def test():
    get_twitter_id_with_cache(["aa", "bb", "cc"])

if __name__ == "__main__":
    # test()
    # test2()
    print(get_twitter_id_with_cache.name)
    print(get_twitter_id_with_cache.description)
    print(get_twitter_id_with_cache.args)