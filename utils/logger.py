# logger.py

import logging

from common.configs import LOG_DIR

logging.basicConfig(
        filename=LOG_DIR,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def log(*args, **kwargs):
    if args is not None and len(args) > 0:
        args = [x if x else 'None' for x in args ]
        msg = ", ".join(args)
        print(msg)
        logging.info(msg)
    if kwargs is not None and len(kwargs) > 0:
        msg = ', '.join([f'{k}:{v}' for k,v in kwargs.items()])
        print(msg)
        logging.info(msg)


if __name__ == '__main__':
    log('test')
    log('hello', 'world')
    log(name='hello, kiki', event='happy new year')
