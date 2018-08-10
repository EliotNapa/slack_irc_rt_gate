API_TOKEN = "<slack api-token>" #set your api token
DEFAULT_REPLY = "Sorry but I didn't understand you" #no need to edit

PLUGINS = [
    'ircrtgate.hello', #no need to edit
]
SLACK_CHNNEL = '<target slack channel>' #without '#' like 'general'

ERRORS_TO = None #if need, specify error trace slack channel like 'bot_error'

IRC_SERVER = '<irc server>' #like 'irc.ircnet.ne.jp'
IRC_PORT = 6667
IRC_CHANNEL = '<irc channel name>' #with '#' like '#slack-irc'
IRC_NICKNAME = '<irc bot name>'

#if no need to use connection password, remove below line 
IRC_PASSWORD = '<irc password>'