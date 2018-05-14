# -*- coding: utf-8 -*-
import sys
import threading
import time
import logging
import logging.config
import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
from irc.client import Connection
from slackbot import settings
from slackbot.bot import Bot
from jaraco.stream import buffer

logger = logging.getLogger(__name__)

class IgnoreErrorsBuffer(buffer.DecodingLineBuffer):
    def handle_exception(self):
        logger.info('DecodingLineBuffer Exception occured!')
        pass

class IrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self):
        channel = settings.IRC_CHANNEL if hasattr(settings,
                                                    'IRC_CHANNEL') else None
        nickname = settings.IRC_NICKNAME if hasattr(settings,
                                                    'IRC_NICKNAME') else None
        server = settings.IRC_SERVER if hasattr(settings,
                                               'IRC_SERVER') else None
        port = settings.IRC_PORT if hasattr(settings,
                                            'IRC_PORT') else None
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.slack_bot = Bot(self)
        self.slack_channel = settings.SLACK_CHNNEL if hasattr(settings,
                                                             'SLACK_CHNNEL') else None
        Connection.transmit_encoding = 'iso-2022-jp-ext'
        irc.client.ServerConnection.buffer_class.encoding = 'iso-2022-jp-ext'
        irc.client.ServerConnection.buffer_class.errors = 'replace'
        irc.client.ServerConnection.buffer_class = IgnoreErrorsBuffer

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        for one_line in e.arguments[0]:
            logger.info('on_pubmsg "%s"', one_line)
            self.send_to_slack(c,e, one_line)
            time.sleep(1)
        pass
        #self.do_command(e, e.arguments[0])

    def on_pubmsg(self, c, e):
        #s = e.arguments[0].encode()
        #s = s1.decode('iso-2022-jp')
        #a = s.split(":", 1)
        a = e.arguments[0].split(":", 1)
        # for one_line in a:
        #     logger.info('on_pubmsg "%s"', one_line)
        if len(a) > 1 and irc.strings.lower(a[0]) == irc.strings.lower(
                self.connection.get_nickname()):
            self.do_command(e, a[1].strip())
        else:
            #send to Slack
            self.send_to_slack(c,e, ':'.join(a))
            # for one_line in a:
            #     self.send_to_slack(c,e, one_line)
            #     time.sleep(1)
            # pass
        return

    def on_dccmsg(self, c, e):
        # non-chat DCC messages are raw bytes; decode as text
        text = e.arguments[0].decode('utf-8')
        c.privmsg("You said: " + text)

    def on_dccchat(self, c, e):
        if len(e.arguments) != 2:
            return
        args = e.arguments[1].split()
        if len(args) == 4:
            try:
                address = ip_numstr_to_quad(args[2])
                port = int(args[3])
            except ValueError:
                return
            self.dcc_connect(address, port)

    def do_command(self, e, cmd):
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = sorted(chobj.users())
                c.notice(nick, "Users: " + ", ".join(users))
                opers = sorted(chobj.opers())
                c.notice(nick, "Opers: " + ", ".join(opers))
                voiced = sorted(chobj.voiced())
                c.notice(nick, "Voiced: " + ", ".join(voiced))
        elif cmd == "dcc":
            dcc = self.dcc_listen()
            c.ctcp("DCC", nick, "CHAT chat %s %d" % (
                ip_quad_to_numstr(dcc.localaddress),
                dcc.localport))
        else:
            c.notice(nick, "Not understood: " + cmd)

    def send_to_slack(self, c, e, message):
        nick = e.source.nick
        msg = ':{0}: {1}'.format(nick, message)
        self.slack_bot.send_message(self.slack_channel,msg)

    def send_to_irc(self, message):
        messages = message.split('\n')
        for one_line in messages:
            self.connection.privmsg(self.channel, one_line)

    def run(self):
        thread = threading.Thread(target=self.run_slack_bot)
        thread.start()
        #self.slack_bot.run()
        #this will block
        self.start()

    def run_slack_bot(self):
        self.slack_bot.run()