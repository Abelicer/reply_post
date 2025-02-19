import os

# Twitter params
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_CLIENT_ID=os.getenv("TWITTER_CLIENT_ID")
TWITTER_CLIENT_SECRET=os.getenv("TWITTER_CLIENT_SECRET")

# Qwen params
DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')
BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL="qwen-plus"
DEFAULT_ROLE_DESC='You are a helpful assistant.'

# Redis params
REDIS_HOST="127.0.0.1"
REDIS_PORT=6379
REDIS_PASSWORD="xxxx"
REDIS_DB=1


# Keywords and themes
TWITTER_USER_NAME='xxxx'

# log path
LOG_DIR = os.path.dirname(__file__) + r'/../log/app.log'


if __name__ == '__main__':
    print(TWITTER_API_KEY)
    print(TWITTER_API_SECRET)
    print(TWITTER_ACCESS_TOKEN)
    print(TWITTER_ACCESS_TOKEN_SECRET)
    print(TWITTER_BEARER_TOKEN)
    print(TWITTER_CLIENT_ID)
    print(TWITTER_CLIENT_SECRET)
    print(DASHSCOPE_API_KEY)
    print(os.path.dirname(__file__))
    print(LOG_DIR)