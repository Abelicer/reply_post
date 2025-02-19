from agents.agent_auto_reply_posts import run
from utils.logger import log
from datetime import datetime

if __name__ == "__main__":
    log(f'main started, now={datetime.now()}')
    run()
    log(f'main finished, now={datetime.now()}')