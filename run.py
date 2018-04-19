#!/usr/bin/env python

import sys
import threading
import time
import logging
import logging.config
from slackbot import settings
from slackbot.bot import Bot


def main():
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    bot = Bot()
    #bot.run()
    thread = threading.Thread(target=run, args=(bot,))
    time.sleep(1)
    bot.send_message('testforbot','test message')
    while True:
        pass

def run(bot):
    bot.run()


if __name__ == '__main__':
    main()
