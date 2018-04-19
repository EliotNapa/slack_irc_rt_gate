#coding: UTF-8
import re
from slackbot.bot import listen_to


@listen_to('.+$')
def hello_send(message):
    message.send('{0} {1}!'.format(message.body['text'], message.body['username']))

