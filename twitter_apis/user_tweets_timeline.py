import requests
import json
from utils.logger import log
from common.configs import TWITTER_BEARER_TOKEN
from common.constants import REDIS_TWITTER_USER_LAST_POST_ID_CACHE
from redis_services.redis_service import get_cache, put_cache
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class GetPostsInput(BaseModel):
    twitter_id: str = Field(description="待查询的用户的twitter_id")
    start_time: str = Field(description="待查询的开始时间，不需要指定开始时间时可以不传")
    max_results: int = Field(description="每次查询最多可以查询的帖文数目，默认10个")

@tool("get_latest_posts_by_twitter_id", args_schema=GetPostsInput)
def get_latest_posts(twitter_id:str, start_time:str=None, max_results:int=10) -> dict[str: str]:
    '''
    用于查询指定twitter_id的用户在twitter上最近发出的帖文集合，其中可以通过传入start_time来指定查询该时间点
    之后发布的帖文，max_results可以指定每次查询最多可以查询的帖文数目。返回的数据格式为{'帖文id':'帖文内容'}
    '''
    url = 'https://api.x.com/2/users/{}/tweets'.format(twitter_id)

    querystring = {"tweet.fields": "text,id", "exclude": "replies,retweets"}
    if start_time:
        querystring["start_time"]=start_time
    if max_results:
        querystring["max_results"] = max_results

    log(user_id=twitter_id, querystring=querystring)

    headers = {"Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    log(user_id=twitter_id, status_code=response.status_code, text=response.text)

    if response.status_code != 200:
        log(f'{twitter_id} responseCode:{response.status_code}, skip this tern')
        return dict()

    json_response = json.loads(response.text)
    if json_response['meta']['result_count'] == 0:
        log(f'{twitter_id} result_count:{json_response['meta']['result_count']}, skip this tern')
        return dict()

    last_id = get_cache(REDIS_TWITTER_USER_LAST_POST_ID_CACHE + twitter_id)
    last_id = last_id if last_id else '0'
    result = {x['id']: x['text'] for x in json_response["data"] if x['id'] > last_id}
    log(user_id=twitter_id, last_id=last_id, result=result)

    if result:
        new_last_id = max(result.keys())
        if new_last_id and new_last_id > last_id:
            put_cache(REDIS_TWITTER_USER_LAST_POST_ID_CACHE + twitter_id, new_last_id)
            log(user_id=twitter_id, new_last_id=new_last_id)

    return result


def test():
    get_latest_posts('1779813246914220032', start_time='2025-02-03T00:00:00Z')

if __name__ == "__main__":
    # test()
    print(get_latest_posts.name)
    print(get_latest_posts.description)
    print(get_latest_posts.args)