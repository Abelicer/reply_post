# https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/Manage-Tweets/create_tweet.py

from twitter_apis.common_api import generate_oauth
from utils.logger import log
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class PostInput(BaseModel):
    text: str = Field(description="发帖时的帖文内容")
    reply_tweet_id: str = Field(description="评论帖文时，被评论的帖文的id，不是评论的场景时传'NOT_REPLY'")

@tool("post_reply_tweets", args_schema=PostInput)
def post(text:str, reply_tweet_id:str=None) -> dict:
    '''
    当你想在twitter上发帖文或者评论其它帖文时非常有用。当发帖文时，只需要传入text；当评论其他帖文时，需要传入text和reply_tweet_id
    '''
    payload = {"text": text}
    if reply_tweet_id is not None and reply_tweet_id != 'NOT_REPLY':
        payload["reply"] = dict()
        payload["reply"]["in_reply_to_tweet_id"]=reply_tweet_id
    log(payload=payload)

    # Making the request
    response = generate_oauth().post(
        "https://api.twitter.com/2/tweets",
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Request returned an error: {} {}".format(response.status_code, response.text)
        )

    log(f'status_code:{response.status_code}, json:{response.json()}')
    return response.json()


def test():
    post("这是第3个发帖", 'NOT_REPLY')

if __name__ == '__main__':
    # test()
    print(post.name)
    print(post.description)
    print(post.args)