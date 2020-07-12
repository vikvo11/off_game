#import pymongo
#from pymongo import MongoClient
import json
#import pymongo
#from bson import BSON
#from bson import json_util
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,logging #For work with HTTP and templates
import requests # For HTTP requests
from functools import wraps # For lock access
from HTTP_basic_Auth import auths # For lock access
from flask_mysqldb import MySQL #For connect to MySQL DB

from flask import jsonify #For response in /webhook
from flask_sslify import SSLify #For use HTTPS
from misck import token # Misck.py - config for telegram_bot
from flask import make_response
import re
#import telebot
#from telebot import types



#********
#import socket
#import socks
#socks.set_default_proxy(socks.SOCKS5, '148.251.130.165',8080,True)
#socket.socket = socks.socksocket
#print(requests.get('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=').text)
#print(requests.get('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=https://vorovik.pythonanywhere.com/webhooks/').text)
#answer = {'chat_id': 488735610, 'text': 'test'}
#print(requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer).text)
#*********

#select from costs ;
#delete from costs where id=25;
URL='https://api.telegram.org/bot{}/'.format(token)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'morkovka18'
app.debug = True
sslify=SSLify(app)
#Config mysql
app.config['MYSQL_HOST']='Ladymarlene.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='Ladymarlene'
app.config['MYSQL_PASSWORD']='cb.,fq12-'
app.config['MYSQL_DB']='Ladymarlene$bot'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
mysql=MySQL(app)

#*****
global last_msg
last_msg=''

curs =3 # 1=RUB; 3=CZK
currency = 'CZK' # 'RUB'
limit_value='limit_czk_value' #'limit_value' - RUB

#listOfInvite = ['OFF_GAME_INVITE_12345' , 'OFF_GAME_INVITE_54321']
listOfInvite ={"OFF_GAME_INVITE_12345": "offgame_user_1", "OFF_GAME_INVITE_54321": "offgame_user_2"}

#https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=https://vorovik.pythonanywhere.com/webhooks/



def write_json(data,filename='answer.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)


def get_updates():
    url=URL+'getUpdates'
    r=requests.get(url)
    write_json(r.json())
    return r.json()

def send_message(chatId,text='Please wait a few seconds...!',parse_mode='',disable_web_page_preview=''):
    url=URL+'sendMessage'
    answer = {'chat_id': chatId, 'text': text, 'parse_mode':parse_mode, 'disable_web_page_preview':disable_web_page_preview}
    print(answer)
    #r=requests.get(url,json=answer)
    #print(r.json())

    request = requests.post(url, data=answer)

    print(request.json())
    return request.json()

def send_photo(chatId,photo='',parse_mode='',caption=''):
    url=URL+'sendPhoto'
    answer = {'chat_id': chatId, 'photo': photo, 'parse_mode':parse_mode, 'caption':caption}
    print(answer)
    #r=requests.get(url,json=answer)
    #print(r.json())

    request = requests.post(url, data=answer)

    print(request.json())
    return request.json()

def parc_text(text):
    # bitcoin pattern = r'/\w+'
    pattern =r'/\S+'
    crypto = re.search(pattern,text).group()
    #crypto = re.search(pattern,text)
    return crypto[1:]
#patter1=r' \w+'
#k=re.search(pattern,text)
#kk=re.search(pattern,k)
def parc_text_cost(text):
    #pattern = r' \w+'
    pattern = r' \-?[0-9]\d*(\.\d+)?$'
    #cost = re.search(pattern,text).group()
    cost = re.search(pattern,text)
    return cost[1:]

def get_price(crypto):
    url='https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@is_logged_in
def home():
    a=1
    return redirect(url_for('dashbord'))
'''
@app.route('/')
def home():
    urla = 'https://demo.offgame.gg/iamgroot/posts'
    headers = {
    'User-Agent': 'ofgroot,
    'From': 'youremail@domain.com'  # This is another valid field
    }
    a=1
    response = requests.get(urla, headers=headers)
    return response
'''
#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#User Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form fields
        username = request.form['username']
        password_candidate = request.form['password']
        #users=auths()
        if auths(username,password_candidate):
            session['logged_in']= True
            return redirect(url_for('dashbord'))
        else:
                error='Invalid login'
                return render_template('login.html',error=error)

    return render_template('login.html')

#Dashbord
@app.route('/dashbord',methods=['GET','POST'])
@is_logged_in
def dashbord():
    #msg = py()
    #add_costs('costs','test123',100)
    #table='costs'
    #title='test'
    #cost=100
    #update_costs('costs','test123',100)
    msg = mysqls('costs')
    #keys = dict(msg[0])
    #b=msg.keys()
    return render_template('dashbordpymongo.html', articles=msg)

#Articles
@app.route('/articles')
def articles():
    return '<h1>Hello bot</h1>'
    # Create cursor
    #cur = mysql.connection.cursor()

    # Get articles
    #result = cur.execute("SELECT * FROM articles")

    #articles = cur.fetchall()

    #if result > 0:
        #return render_template('articles.html', articles=articles)
    #else:
        #msg = 'No Articles Found'
        #return render_template('articles.html', msg=msg)
    # Close connection
    #cur.close()

@app.route('/webhooks/',methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        r = request.get_json()
        chat_id=r['message']['chat']['id']
        text=r['message']['text']
        from_=r['message']['from']['first_name']
        #from_id=r['message']['from']['id']
        #username=r['message']['from']['username']
        #if r['message']['from']['username']:
        #    usrname=r['message']['from']['username']
        #else:
        #    usrname="noname"

        global last_msg
        last_msg=''
        #last_msg=json.dumps(r,ensure_ascii=False)
        last_msg=r
        #bitcoin pattern =r'/\w+'
        pattern =r'/\S+'
        #patternSum =r'/сумма'
        patternSum =r'/pass'
        #patternLim =r'/лимит'
        #patternInv =r'/invite'
        patternStart =r'/start'
        patternCheck =r'/OFF_GAME'
        #The code you entered does not exist, please try again:

        #answer = {'chat_id': 488735610, 'text': 'test'}
        #print(requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer).text)
#****
        #if re.search(patternInv,text):
            #send_message(chat_id,""+from_+" ")
            #cur = mysql.connection.cursor()
            #Lims=cur.execute("SELECT title,limits,cost FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            #Lims = cur.fetchall()
            #cur.close()
            #send_message(chat_id,'Категория = '+str(Lim['title'])+'лимит=' + str(Lim['limits']))
            #for Lim in Lims:
                #send_message(chat_id,'Категория = '+str(Lim['title'])+' лимит=' + str(Lim['limits']))
                #send_message(chat_id,str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits']))
                #limmsg=limmsg+str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits'])
                #limmsg=str(Lim['title'])+': текущий = '+str(Lim['cost']) +currency+' лимит=' + str(Lim['limits'])+currency
                #lmsg=lmsg+""+limmsg+". \n"
            #send_message(chat_id,""+from_+" ")

            #inv=parc_text_cost(text)
            #inv.replace(" ", "")

            #send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            #send_message(chat_id,""+from_+" "+str(parc_text(text))+". \n"+inv+"")
            #send_message(chat_id,""+from_+". \n"+inv+"")
            #return jsonify(r)
            #return response(status=200)
#*****
        #if re.search(patternLim,text):
            #cur = mysql.connection.cursor()
            #Lims=cur.execute("SELECT title,limits,cost FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            #Lims = cur.fetchall()
            #cur.close()
            #send_message(chat_id,'Категория = '+str(Lim['title'])+'лимит=' + str(Lim['limits']))
            #for Lim in Lims:
                #send_message(chat_id,'Категория = '+str(Lim['title'])+' лимит=' + str(Lim['limits']))
                #send_message(chat_id,str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits']))
                #limmsg=limmsg+str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits'])
                #limmsg=str(Lim['title'])+': текущий = '+str(Lim['cost']) +currency+' лимит=' + str(Lim['limits'])+currency
                #lmsg=lmsg+""+limmsg+". \n"
            #send_message(chat_id,""+limmsg+". \n"+limmsg+"")

            #return jsonify(r)
            #return response(status=200)

        if re.search(patternStart,text):
            #cur = mysql.connection.cursor()
            #Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            #Sum = cur.fetchone()
            #cur.close()
            send_message(chat_id,""+from_+", please enter the invitation code: ")
            #send_message(chat_id,'Общая потраченная сумма в этом месяце = '+str(Sum['summa']))

            #inv=parc_text(text)
            #inv.replace(" ", "")
            #send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            #send_message(chat_id,""+from_+" "+str(parc_text(text))+". \n"+inv+"")
            #return jsonify(r)
            return '',200

        if re.search(patternCheck,text):
            #cur = mysql.connection.cursor()
            #Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            #Sum = cur.fetchone()
            #cur.close()
            #send_message(chat_id,""+from_+" ")
            #send_message(chat_id,'Общая потраченная сумма в этом месяце = '+str(Sum['summa']))

            inv=parc_text(text)
            inv.replace(" ", "")
            #send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            if inv in listOfInvite:
                invite={'chat_id': -472269034}
                url=URL+'exportChatInviteLink'
                link=requests.post(url,data=invite)
                #answer2 = {'chat_id': 488735610, 'text': link}
                #requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage',data=answer2)
                send_message(chat_id,""+str(r['message']['from']['id'])+" - Registered successfully- assigned internal name-"+listOfInvite[inv])
                #send_message(chat_id," - Registered successfully- assigned internal name-"+listOfInvite[inv])
                send_message(chat_id,link)
                #return jsonify(r)
                return '',200
            else:
                send_message(chat_id,"The code you entered does not exist, please try again:")
                #return jsonify(r)
                return '',200

        if re.search(patternSum,text):
            #cur = mysql.connection.cursor()
            #Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            #Sum = cur.fetchone()
            #cur.close()

            #send_message(chat_id,"https://demo.offgame.gg/p/405gzqhkbzvq5vm?ts=1593863055210")
            testmsg="""<b>bold</b>, <strong>bold</strong>
<i>italic</i>, <em>italic</em>
<u>underline</u>, <ins>underline</ins>
<s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
<b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
<a href="http://www.example.com/">inline URL</a>
<a href="tg://user?id=488735610">inline mention of a user</a>
<code>inline fixed-width code</code>
<pre>pre-formatted fixed-width code block</pre>
<pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>"""
            testmsg2="""
            <strong>Заголовок</strong>
*** Произвольный текст ***
<a href="https://demo.offgame.gg/p/405ophhkchemqu7?ts=1594457171218">Линка на сайт</a>


            """
            #<a href="https://demo.offgame.gg/p/405ophhkchemqu7?ts=1594457171218">Линка на сайт</a>
            #<a href="https://m.offgame.gg/u/2898c608-b92e-4396-8299-059d03eabdb0/p/405gzqhkbzvq5vm/405gzqhkbzvq65n">&#8205; </a>
            #send_message(chat_id,testmsg,"HTML")
            send_message(chat_id,testmsg2,"HTML",'false')
            #send_photo(chat_id,"https://m.offgame.gg/u/2898c608-b92e-4396-8299-059d03eabdb0/p/405gzqhkbzvq5vm/405gzqhkbzvq65n","TeXt")
            #send_message(chat_id,'Общая потраченная сумма в этом месяце = '+str(Sum['summa']))

            #inv=parc_text(text)
            #inv.replace(" ", "")
            #send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            #send_message(chat_id,""+from_+" "+str(parc_text(text))+". \n"+inv+"")
            #return jsonify(r)
            return '',200
            #return response(status=200)
        #else:
            #if re.search(pattern,text) and not re.search(patternLim,text) :
                #bitcoin price = get_price(parc_text(text))
               #cost=parc_text_cost(text)
                #cost.replace(" ", "")

            #add_costs()
            #send_message(chat_id,price)
            #add_costs('costs','test123',100)

            #*update_costs('costs',str(parc_text(text)),int(cost))

            #current_costs('costs',str(parc_text(text)))

            #*send_message(chat_id,parc_text(text))
                #send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            #update_costs('costs','test123',100)
            #if re.search(pattern1,text):
                #a=re.search(pattern1,text)
                #update_costs('costs',a,900)
            #return jsonify(r)
            #return response(status=200)
        #return response(status=200)
        return '', 200
        #return jsonify(r)

    return '<h1>Hello bot</h1>'

@app.route('/webhooks1/',methods=['POST','GET'])
def webhooks1():
    if request.method == 'GET':
        #socks.set_default_proxy(socks.SOCKS5, '148.251.130.165',8080,True)
        #socket.socket = socks.socksocket
        #answer1 = {'chat_id': 488735610, 'text': 'test'}
        answer1 = {'chat_id': 488735610, 'text': 'test'}
        pin={'chat_id': -482246882, 'message_id': 66,}
        invite={'chat_id': -482246882}
        #requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer1).text
        #requests.post('https://yandex.ru',data=answer1)

        #requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage',data=answer1)

        link=requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/exportChatInviteLink',data=invite)
        answer2 = {'chat_id': 488735610, 'text': link}
        requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage',data=answer2)

        requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/pinChatMessage',data=pin)
#https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/setWebhook?url=https://ladymarlene.pythonanywhere.com/webhooks/
        return '<h1>Hello bot</h1>'

    return '<h1>Hello bot</h1>'

@app.route('/test/',methods=['POST','GET'])
def test():
    if request.method == 'GET':
        r = request.get_json()
        #socks.set_default_proxy(socks.SOCKS5, '148.251.130.165',8080,True)
        #socket.socket = socks.socksocket
        #answer1 = {'chat_id': 488735610, 'text': 'test'}
        #answer1 = {'chat_id': 488735610, 'text': 'test'}
        #pin={'chat_id': -482246882, 'message_id': 66,}
        #invite={'chat_id': -482246882}
        #requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer1).text
        #requests.post('https://yandex.ru',data=answer1)

        #requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage',data=answer1)

        #link=requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/exportChatInviteLink',data=invite)
        #answer2 = {'chat_id': 488735610, 'text': link}
        #requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/sendMessage',data=answer2)

        #requests.post('https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/pinChatMessage',data=pin)
#https://api.telegram.org/bot1238610737:AAGiXsnB_h-JvYKKZKMkaUsM3nTkHQyyjwA/setWebhook?url=https://ladymarlene.pythonanywhere.com/webhooks/
        return '',200
        #return jsonify(r)
        #return response(status=200)

    return '<h1>Hello bot123</h1>'

@app.route('/last_msg/',methods=['POST','GET'])
#curl -u vorovik:python123 -i https://vorovik.pythonanywhere.com/last_msg/
def teslast():
    r='<h2>{}</h2>'.format(str(last_msg))
    return r

def py():
    client = MongoClient("ds141786.mlab.com:41786", username = 'podarkin', password = 'podarkin', authSource = 'heroku_q51pzrtm')
    db = client["heroku_q51pzrtm"]
    bookings_coll = db.bookings
    doc = bookings_coll.find_one()
    asa = json.dumps(doc, sort_keys=True, indent=4, default=json_util.default)
    docs = bookings_coll.find()
    id = docs[0]['name']
    return docs
def mysqls(table):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    #result = cur.execute("SELECT * FROM %s",(art))
    #result = cur.execute("SELECT * FROM articles")
    result = cur.execute("SELECT * FROM {}".format(table))

    #result = cur.execute("SELECT * FROM users WHERE username=%s",[username])
    #cur.execute("INSERT INTO articles(title,author,body) VALUES(%s,%s,%s)",(title,session['username'],body))
    articles = cur.fetchall()
    cur.close()
    return articles

def add_costs(table,title,cost):
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute query
    #cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
    cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
    #result = cur.execute("SELECT * FROM {} WHERE id=%s".format('articles'),[username])
    #Commit ot db
    mysql.connection.commit()
    #Close connection
    cur.close()
    return 'ok'

def update_costs(table,title,cost):
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute query
    #year and month
    result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
    limit= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
    if result>0:
        if limit>0:
            cur.execute("UPDATE {} SET cost=cost+%s,limits=limits-%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,cost,title))
        else:
            cur.execute("UPDATE {} SET cost=cost+%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,title))
        #cur.execute("UPDATE {} SET cost=cost+%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,title))
        mysql.connection.commit()
        result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
        result = cur.fetchone()
        #cur.close()
    else:
        if limit>0:
            limits= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
            limits = cur.fetchone()
            cur.execute("INSERT INTO {}(title,cost,year,month,limits) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())),%s)".format(table),(title,cost,int(limits[str(limit_value)])-cost))
        else:
            cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
        #cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
        #result = cur.execute("SELECT * FROM {} WHERE id=%s".format('articles'),[username])
        #Commit ot db
        mysql.connection.commit()
        result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
        result = cur.fetchone()

        #Close connection
        #cur.close()
    #return str(result)
    #limit= cur.execute("SELECT * FROM limit where title=%s",[title])
    if limit>0:
        limits= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
        limits = cur.fetchone()

        LimitSum= cur.execute("SELECT * FROM limit_dict where title=%s",['общий'])
        limitsSum = cur.fetchone()
        Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
        Sum = cur.fetchone()
        testsum=str(limitsSum[str(limit_value)]-Sum['summa'])
        if int(testsum)<10000/curs:
            totallimit='Заканчивается общий лимит!!! Осталось ='+testsum+' '+currency
        else:
            totallimit=''
        cur.close()
        return ('Затраты в текущем месяце на '+str(result['title'])+'= '+str(result['cost'])+' '+currency+'. Лимит = '+str(result['limits'])+' '+currency+' '+totallimit)
    else:
        cur.close()
        return ('Затраты в текущем месяце на '+str(result['title'])+'= '+str(result['cost'])+' '+currency)
def main():
    #doc = bookings_coll.find_one()


    pass
   # a = [x for x in bookings_coll.find()]


if __name__ == '__main__':
    #bot.polling(none_stop=True)
    main()
