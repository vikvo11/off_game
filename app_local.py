
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,logging #For work with HTTP and templates
import requests
import datetime
from time import sleep
app = Flask(__name__)
url = "https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/"
 

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = get_result[len(get_result)]

        return last_update	

greet_bot = BotHandler('1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA')  
greetings = ('hello', 'hi', 'greetings', 'sup')
commands = ('/posts', 'news')   
now = datetime.datetime.now()
urla = 'https://demo.offgame.gg/iamgroot/posts'
headers = {
    'User-Agent': 'ofgroot',
	'From': 'youremail@domain.com'  # This is another valid field
    }
		
def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    while True:
        greet_bot.get_updates(new_offset)

        last_update = greet_bot.get_last_update()

        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name='test' #= last_update['message']['chat']['first_name']
		
        if last_chat_text.lower() in commands and new_offset == last_update_id:
            req = requests.get(urla, headers=headers).json()
            for post in req['list']:
               print(post['url'])
               #requests.get('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage?chat_id=488735610&text='+str(post['url']))
               greet_bot.send_message(last_chat_id,str(post['url']))
            #today += 1
			
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Good Morning  {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Good Afternoon {}'.format(last_chat_name))
            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Good Evening  {}'.format(last_chat_name))
            today += 1

        new_offset = last_update_id + 1

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'GET':
	    print ('test')
    urla = 'https://demo.offgame.gg/iamgroot/posts'
    headers = {
    'User-Agent': 'ofgroot',
	'From': 'youremail@domain.com'  # This is another valid field
    }
    a=1
    #response = requests.get(urla, headers=headers)
    req = requests.get(urla, headers=headers).json()
    #return 'response' 
    #print(request['list'])
    for post in req['list']:
       print(post['url'])
       requests.get('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage?chat_id=488735610&text='+str(post['url']))
    return str(req['list'][2]['url'])
@app.route('/123')
def home1():
    print ('test')
    return '123'
if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
#app.run(debug=True)