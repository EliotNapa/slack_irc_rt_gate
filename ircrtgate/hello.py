#coding: UTF-8
import re
from xml.sax.saxutils import unescape
from slackbot.bot import listen_to
from ircbot.iso2022encx import Iso2022jpEncX

@listen_to('.+$')
def hello_send(message):
    """
    send slack messeget to irc
    """
    msg_str = Iso2022jpEncX.regularize('{0}'.format(message.body['text']))
    msg_str = url_convert(msg_str)
    user_str = Iso2022jpEncX.regularize('{0}'.format(message.body['username']))
    message._client.irc_bot.send_to_irc(unescape(user_str), unescape(msg_str))
    #message._client.irc_bot.send_to_irc('({1}) {0}'.format(message.body['text'], message.body['username']))
    #message.send('{0} {1}!'.format(message.body['text'], message.body['username']))



def url_convert(src_string):
    """
    simplify slack url repleat
    """
    result = src_string
    match = re.search(r'<ht.+\|ht.+>',src_string)

    if match:
        result = re.findall(r'<(ht.+)\|ht.+>',src_string)
        result = '<' + result[0] + '>'

    return result
