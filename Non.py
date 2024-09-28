import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests, re, json, time
bot = telebot.TeleBot(input('tokenn: '))
R44, R33, followers, status, bad, R22, failed, try_list = [], [], {"count": 0}, [], [], [], [], []
R02 = {}
def R55(session, username, password, host, your_username):
    global R44, R33, status, failed, bad, R22
    session.headers.update({
        'Accept-Encoding': 'gzip, deflate',
       
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',        
        'Host': '{}'.format(host),
        
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Connection': 'keep-alive'
    })
    
    response = session.get('https://{}/login'.format(host))
    R01 = re.search('"&antiForgeryToken=(.*?)";', str(response.text))
    
    if R01:
        token = R01.group(1)
        session.headers.update({
            'Accept': 'application/json, text/javascript, */*; q=0.01',
           
            'Referer': 'https://{}/login'.format(host),
           
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            
            'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()]),
            'Origin': 'https://{}'.format(host)
        })
        
        data = {
            'username': username,
            'antiForgeryToken': token,
            'userid': '',
            'password': password
        }
        
        response2 = session.post('https://{}/login?'.format(host), data=data)
        json_response = json.loads(response2.text)
        
        if 'status' in json_response and json_response['status'] == 'success':
            session.headers.update({
                'Referer': 'https://{}/tools/send-follower'.format(host),
                'Cookie': '; '.join([str(key) + '=' + str(value) for key, value in session.cookies.get_dict().items()])
            })
            data = {'username': your_username}
            response3 = session.post('https://{}/tools/send-follower?formType=findUserID'.format(host), data=data)
            
            if 'name="userID"' in response3.text:
                user_id = re.search('name="userID" value="(\d+)">', response3.text).group(1)
                data = {
                    'userName': your_username,
                    'adet': '500',
                    'userID': user_id,
                }
                response4 = session.post('https://{}/tools/send-follower/{}?formType=send'.format(host, user_id), data=data)
                R0 = json.loads(response4.text)
                
                if 'status' in R0 and R0['status'] == 'success':
                    R44.append(R0)
                    status.append(R0)
                    return True
                else:
                    R33.append(R0)
                    return False
    return False

def R9(your_username):
    with requests.Session() as session:
        session.headers.update({
            'User-Agent': 'Instagram 317.0.0.0.3 Android (27/8.1.0; 360dpi; 720x1280; LAVA; Z60s; Z60s; mt6739; en_IN; 559698990)',
            'Host': 'i.instagram.com',
            'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        response = session.get('https://i.instagram.com/api/v1/users/web_profile_info/?username={}'.format(your_username))
        
        if '"status":"ok"' in response.text:
            followers_count = json.loads(response.text)['data']['user']['edge_followed_by']['count']
            return followers_count
        return 0
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    R7 = InlineKeyboardButton(text="أدخل اسم المستخدم", callback_data="enter_username")
    R8 = InlineKeyboardButton(text="أدخل كلمة المرور", callback_data="enter_password")
    R6 = InlineKeyboardButton(text="أدخل المستخدم المستهدف", callback_data="enter_target_username")
    
    markup.add(R7, R8, R6)
    bot.send_message(message.chat.id, "مرحباً! اختر العملية:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def R5(call):
    if call.data == "enter_username":
        msg = bot.send_message(call.message.chat.id, "أدخل اسم المستخدم الخاص بحسابك:")
        bot.register_next_step_handler(msg, R4)
    elif call.data == "enter_password":
        msg = bot.send_message(call.message.chat.id, "أدخل كلمة المرور الخاصة بحسابك:")
        bot.register_next_step_handler(msg, R3)
    elif call.data == "enter_target_username":
        msg = bot.send_message(call.message.chat.id, "أدخل اسم المستخدم المستهدف:")
        bot.register_next_step_handler(msg, R2)

def R4(message):
    R02['username'] = message.text
    bot.send_message(message.chat.id, f"تم حفظ اسم المستخدم: {message.text}")

def R3(message):
    R02['password'] = message.text
    bot.send_message(message.chat.id, f"تم حفظ كلمة المرور")

def R2(message):
    R02['target_username'] = message.text
    bot.send_message(message.chat.id, f"تم حفظ اسم المستخدم المستهدف: {message.text}")

    bot.send_message(message.chat.id, "جاري إرسال المتابعين...")
    R1(message)

def R1(message):
    if all(key in R02 for key in ['username', 'password', 'target_username']):
        for host in ['instamoda.org', 'takipcitime.com', 'takipcikenti.com']:
            session = requests.Session()
            result = R55(session, R02['username'], R02['password'], host, R02['target_username'])
            
            if result:
                bot.send_message(message.chat.id, f"تم إرسال المتابعين بنجاح من {host}")
            else:
                bot.send_message(message.chat.id, f"فشل في إرسال المتابعين من {host}")
    else:
        bot.send_message(message.chat.id, "يرجى إدخال جميع البيانات أولاً.")

bot.infinity_polling()
