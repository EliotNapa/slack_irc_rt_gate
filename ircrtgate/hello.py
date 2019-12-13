#coding: UTF-8
import re
import urllib.parse
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
    """

    result = src_string
    match = re.search(r'<ht.+\|ht.+>',src_string)

    if match:
        result = re.findall(r'<ht.+\|(ht.+)>',src_string)
        result = '<' + result[0] + '>'

    match_enc = re.search(r'<http.+\/\/.+>',result)

    Encode_Path_only = True

    if match_enc:
        if Encode_Path_only:
            last_pos = result.rfind('/')
            param_pos = result.rfind('?')
            if 0 < last_pos:
                if 0 < param_pos:
                    result = '<{0}/{1}?{2}>'.format(
                            result[1:last_pos],
                            urllib.parse.quote(result[last_pos+1:param_pos]),
                            result[param_pos+1:-1]
                        )
                else:
                    result = '<{0}/{1}>'.format(
                            result[1:last_pos],
                            urllib.parse.quote(result[last_pos+1:-1])
                        )
        
        else:
            find_pos = result.find('://')
            if 0 < find_pos:
                result = '<{0}://{1}>'.format(
                        result[1:find_pos],
                        urllib.parse.quote(result[find_pos+3:-1])
                    )

    return result