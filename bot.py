import os
import telegram
import json
import requests
import re
from credential import retrieve

# basic setup
base = os.path.dirname(os.path.abspath(__file__))

# telegram bot credential
with open(base+'/telegram_credential.json') as f:
    tele_cred = json.loads(f.read())

mytoken = tele_cred['mytoken']
chatid = tele_cred['chatid']
bot = telegram.Bot(token = mytoken)
# bot.sendMessage(chat_id=chatid, text = str('message_content_here'))

# start timeline streaming
try:
    with open('config.json','r') as f:
        cred = json.loads(f.read())
        username = cred['username']
        instance = cred['instance']
except:
    username = input('Please input your username: ')
    instance = input('Please input your instance: ')
acc = retrieve(username, instance)
head = {'Authorization':'Bearer '+acc}
uri = instance+'/api/v1/streaming/user'
r_user = requests.get(uri,headers=head,stream=True)

# keyword parsing
with open(base+'/keyword.txt','r') as f:
    kw = f.read().split('\n')

def send_tg_message(t):
    bot.sendMessage(chat_id=chatid,text=t)

# run timeline streaming

for l in r_user.iter_lines():
    dec = l.decode('utf-8')
    try:
        newdec = json.loads(re.sub('data: ','',dec))
        if newdec['reblog']:
            content = newdec['reblog']['content']
        else:
            content = newdec['content']
        for keyword in kw:
            if keyword in content:
                send_tg_message(content)
