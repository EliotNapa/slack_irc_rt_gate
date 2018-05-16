 [lins05/slackbot](https://github.com/lins05/slackbot)と[jaraco/irc](https://github.com/jaraco/irc)を改造したIRC Slackゲートウェイです。

Slack Real Time Messaging APIを利用しているのでSlack IRC gatewayとXAMP APIがシャットダウンされた後も利用可能です。
日本のIRCでよく使われる8bit JISにも対応しています。

 開発中ですが、一応動くみたい？

使い方

1)リポジトリをローカルにcloneしてください。

2)slackbot_settings-template.py を slackbot_settings.py
にコピーし'<' '>'で囲まれた部分を必要に応じて編集してください。

3)slack irc gatewayを起動するにはコマンドラインで、
$python3 run_gate.py 
とタイプしてください。