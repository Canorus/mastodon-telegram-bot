import os
import telegram
import json
import requests
import re
from credential import retrieve

#basic setup
base = os.path.dirname(os.path.abspath(__file__))

#telegram bot credential
with open(base+'/telegram_credential.json') as f:
    tele_cred = json.loads(f.read())

mytoken = tele_cred['mytoken']
chatid = tele_cred['chatid']
bot = telegram.Bot(token = mytoken)
#bot.sendMessage(chat_id=chatid, text = str('message_content_here'))

#start timeline streaming
try:
    with open('config.json','r') as f:
        cred = json.loads(f.read())
        username = cred['username']
        instance = cred['instance']
except:
    username = input('Please input your username: ')
    instance = input('Please input your instance: ')
acc = retrieve(username, instance)


