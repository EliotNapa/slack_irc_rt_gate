# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys
import threading
import time
import logging
import logging.config
from slackbot import settings
from slackbot.bot import Bot
from ircbot.ircbot import IrcBot


def main():
    kw = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**kw)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
    #bot = Bot()
    irc_bot = IrcBot()
    irc_bot.run()
    #bot.run()
    #thread = threading.Thread(target=run, args=(irc_bot))
    #thread.start()
    #irc_bot.start()

    #time.sleep(1)
    #bot.send_message('testforbot','test message')
    #while True:
    #    time.sleep(10)

def run(bot, irc_bot):
    irc_bot.run()


if __name__ == '__main__':
    main()
