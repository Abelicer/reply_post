from common.configs import TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET
from requests_oauthlib import OAuth1Session
from datetime import timedelta
from langchain_core.tools import tool
from pydantic import BaseModel, Field

def generate_oauth():
    oauth = OAuth1Session(
        TWITTER_API_KEY,
        client_secret=TWITTER_API_SECRET,
        resource_owner_key=TWITTER_ACCESS_TOKEN,
        resource_owner_secret=TWITTER_ACCESS_TOKEN_SECRET,
    )
    return oauth


class GetTwitterDatetimeInput(BaseModel):
    hour_before: int = Field(description="如果想要知道几个小时之前的时间，则这里传小时数。只允许传>=0的数字，不需要时传0")
    hour_after: int = Field(description="如果想要知道几个小时之后的时间，则这里传小时数。只允许传>=0的数字，不需要时传0")


@tool("get_twitter_datetime", args_schema=GetTwitterDatetimeInput)
def get_twitter_datetime(hour_before: int=None, hour_after: int=None) -> str:
    '''
    当你想查询 当前/几个小时之前/之后 的时间时非常有用。
    '''
    time = datetime.now()
    if hour_before and hour_before > 0:
        time = time - timedelta(hours=hour_before)
    if hour_after and hour_after > 0:
        time = time + timedelta(hours=hour_after)
    time = format_twitter_time(time)
    print(f'time={time}')
    return time

def format_twitter_time(time):
    # 将时间转换为 Twitter API 支持的格式（ISO 8601）YYYY-MM-DDTHH:MM:SSZ, UTC
    return time.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


from datetime import datetime, timezone


def test():
    time = datetime.now()
    print(format_twitter_time(time))

    time2 = time.astimezone(timezone.utc)
    print(format_twitter_time(time))
    print(format_twitter_time(time2))


if __name__ == '__main__':
    # print(get_twitter_datetime(hour_before=2))
    # print(get_twitter_datetime.name)
    # print(get_twitter_datetime.description)
    # print(get_twitter_datetime.args)
    test()