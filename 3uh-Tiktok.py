import hashlib
import json
from time import time, sleep
from hashlib import md5
from copy import deepcopy
from random import choice, randint
import requests
from urllib.parse import quote
import telebot
from telebot import types

# Your bot token
bot = telebot.TeleBot("7480473881:AAFvgLeXIN_3Emb5ikfpAvHUito3kKub48A")

# Function Definitions
def hex_string(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return tmp_string

def RBIT(num):
    result = ''
    tmp_string = bin(num)[2:]
    while len(tmp_string) < 8:
        tmp_string = '0' + tmp_string
    for i in range(0, 8):
        result = result + tmp_string[7 - i]
    return int(result, 2)

def file_data(path):
    with open(path, 'rb') as f:
        result = f.read()
    return result

def reverse(num):
    tmp_string = hex(num)[2:]
    if len(tmp_string) < 2:
        tmp_string = '0' + tmp_string
    return int(tmp_string[1:] + tmp_string[:1], 16)

class XG:
    def __init__(self, debug):
        self.length = 0x14
        self.debug = debug
        self.hex_CE0 = [0x05, 0x00, 0x50, choice(range(0, 0xFF)), 0x47, 0x1e, 0x00, choice(range(0, 0xFF)) & 0xf0]

    def addr_BA8(self):
        tmp = ''
        hex_BA8 = []
        for i in range(0x0, 0x100):
            hex_BA8.append(i)
        for i in range(0, 0x100):
            if i == 0:
                A = 0
            elif tmp:
                A = tmp
            else:
                A = hex_BA8[i - 1]
            B = self.hex_CE0[i % 0x8]
            if A == 0x05:
                if i != 1:
                    if tmp != 0x05:
                        A = 0
            C = A + i + B
            while C >= 0x100:
                C = C - 0x100
            if C < i:
                tmp = C
            else:
                tmp = ''
            D = hex_BA8[C]
            hex_BA8[i] = D
        return hex_BA8

    def initial(self, debug, hex_BA8):
        tmp_add = []
        tmp_hex = deepcopy(hex_BA8)
        for i in range(self.length):
            A = debug[i]
            if not tmp_add:
                B = 0
            else:
                B = tmp_add[-1]
            C = hex_BA8[i + 1] + B
            while C >= 0x100:
                C = C - 0x100
            tmp_add.append(C)
            D = tmp_hex[C]
            tmp_hex[i + 1] = D
            E = D + D
            while E >= 0x100:
                E = E - 0x100
            F = tmp_hex[E]
            G = A ^ F
            debug[i] = G
        return debug

    def calculate(self, debug):
        for i in range(self.length):
            A = debug[i]
            B = reverse(A)
            C = debug[(i + 1) % self.length]
            D = B ^ C
            E = RBIT(D)
            F = E ^ self.length
            G = ~F
            while G < 0:
                G += 0x100000000
            H = int(hex(G)[-2:], 16)
            debug[i] = H
        return debug

    def main(self):
        result = ''
        for item in self.calculate(self.initial(self.debug, self.addr_BA8())):
            result = result + hex_string(item)

        return '8404{}{}{}{}{}'.format(hex_string(self.hex_CE0[7]), hex_string(self.hex_CE0[3]),
                                       hex_string(self.hex_CE0[1]), hex_string(self.hex_CE0[6]), result)

def X_Gorgon(param, data, cookie):
    gorgon = []
    ttime = time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = md5(bytearray(param, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))
    if data:
        if isinstance(data, str):
            data = data.encode(encoding='utf-8')
        data_md5 = md5(data).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    gorgon = gorgon + [0x1, 0x1, 0x2, 0x4]
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

def run(param="", stub="", cookie=""):
    gorgon = []
    ttime = time()
    Khronos = hex(int(ttime))[2:]
    url_md5 = md5(bytearray(param, 'utf-8')).hexdigest()
    for i in range(0, 4):
        gorgon.append(int(url_md5[2 * i: 2 * i + 2], 16))
    if stub:
        data_md5 = stub
        for i in range(0, 4):
            gorgon.append(int(data_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    if cookie:
        cookie_md5 = md5(bytearray(cookie, 'utf-8')).hexdigest()
        for i in range(0, 4):
            gorgon.append(int(cookie_md5[2 * i: 2 * i + 2], 16))
    else:
        for i in range(0, 4):
            gorgon.append(0x0)
    gorgon = gorgon + [0x1, 0x1, 0x2, 0x4]
    for i in range(0, 4):
        gorgon.append(int(Khronos[2 * i: 2 * i + 2], 16))
    return {'X-Gorgon': XG(gorgon).main(), 'X-Khronos': str(int(ttime))}

def get_stub(data):
    if isinstance(data, dict):
        data = json.dumps(data)

    if isinstance(data, str):
        data = data.encode(encoding='utf-8')
    if data == None or data == "" or len(data) == 0:
        return "00000000000000000000000000000000"

    m = hashlib.md5()
    m.update(data)
    res = m.hexdigest()
    res = res.upper()
    return res

def get_profile(session_id, device_id, iid):
    """Retrieve the current TikTok username for a given session, device, and iid."""
    try:
        url = f"https://api.tiktokv.com/passport/account/info/v2/?id=kaa&version_code=34.0.0&language=en&app_name=lite&app_version=34.0.0&carrier_region=SA&device_id=7256623439258404357&tz_offset=10800&mcc_mnc=42001&locale=en&sys_region=SA&aid=473824&screen_width=1284&os_api=18&ac=WIFI&os_version=17.3&app_language=en&tz_name=Asia/Riyadh&carrier_region1=SA&build_number=340002&device_platform=iphone&iid=7353686754157692689&device_type=iPhone13,4"
        headers = {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": f"sessionid={session_id}",
            "sdk-version": "2",
            "user-agent": "com.zhiliaoapp.musically/432424234 (Linux; U; Android 5; en; fewfwdw; Build/PI;tt-ok/3.12.13.1)",
        }
        
        response = requests.get(url, headers=headers, cookies={"sessionid": session_id})
        return response.json().get("data", {}).get("username", "None")
    except Exception:
        return "None"

def check_is_changed(last_username, session_id, device_id, iid):
    """Check if the username has been changed in the TikTok profile."""
    return get_profile(session_id, device_id, iid) != last_username

def change_username(session_id, device_id, iid, last_username, new_username):
    """Attempt to change a TikTok username."""
    data = f"aid=364225&unique_id={quote(new_username)}"
    parm = f"aid=364225&residence=&device_id={device_id}&version_name=1.1.0&os_version=17.4.1&iid={iid}&app_name=tiktok_snail&locale=en&ac=4G&sys_region=SA&version_code=1.1.0&channel=App%20Store&op_region=SA&os_api=18&device_brand=iPad&idfv=16045E07-1ED5-4350-9318-77A1469C0B89&device_platform=iPad&device_type=iPad13,4&carrier_region1=&tz_name=Asia/Riyadh&account_region=sa&build_number=11005&tz_offset=10800&app_language=en&carrier_region=&current_region=&aid=364225&mcc_mnc=&screen_width=1284&uoo=1&content_language=&language=en&cdid=B75649A607DA449D8FF2ADE97E0BC3F1&openudid=7b053588b18d61b89c891592139b68d918b44933&app_version=1.1.0"
    
    sig = run(parm, md5(data.encode("utf-8")).hexdigest() if data else None, None)  
    url = f"https://api.tiktokv.com/aweme/v1/commit/user/?{parm}"
    headers = {
        "Connection": "keep-alive",
        "User-Agent": "Whee 1.1.0 rv:11005 (iPad; iOS 17.4.1; en_SA@calendar=gregorian) Cronet",
        "Cookie": f"sessionid={session_id}",
    }
    headers.update(sig)
    response = requests.post(url, data=data, headers=headers)
    result = response.text
    if "unique_id" in result:
        if check_is_changed(last_username, session_id, device_id, iid):
            return "Username change successful."
        else:
            return "Failed to change username: " + str(result)
    else:
        return "Failed to change username: " + str(result)

# Telegram Bot Handlers

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("عرض يوزرك الحالي", callback_data="view_profile")
    item2 = types.InlineKeyboardButton("تغيير اسم المستخدم", callback_data="change_username")
    item3 = types.InlineKeyboardButton("تعليمات الاستخدام", callback_data="help")
    item4 = types.InlineKeyboardButton("اتصل بالدعم", callback_data="contact_support")
    markup.add(item1, item2, item3, item4)
    
    bot.send_message(
        message.chat.id,
        "👋 هلا وسهلا بيك في بوت تغيير يوزرات تيك توك! ✨\n\n"
        "*اختر وحدة من الخيارات اللي تحت:*",
        parse_mode='Markdown',
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "view_profile")
def handle_view_profile_callback(call):
    bot.send_message(
        call.message.chat.id,
        "🔍 **أرسللي السشن آي دي مال حسابك:** 📧\n\n"
        "📘 **إذا ما تعرف تطلع السشن آي دي، شوف القناة هنا:** [قناة التعليمات](https://t.me/pyterm1)\n\n"
        "🔸 **تأكد من كتابة السشن آي دي صح.\n"
        "🔸 إذا صار أي خطأ، تواصل مع الدعم من [بوت التواصل](https://t.me/T3uhBot).**",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_session_id_for_profile)

@bot.callback_query_handler(func=lambda call: call.data == "change_username")
def handle_change_username_callback(call):
    bot.send_message(
        call.message.chat.id,
        "✏️ **أرسللي السشن آي دي مال حسابك:** 📧\n\n"
        "📘 **إذا ما تعرف تطلع السشن آي دي، شوف القناة هنا:** [قناة التعليمات](https://t.me/pyterm1)\n\n"
        "🔸 **تأكد من كتابة السشن آي دي صح.\n"
        "🔸 إذا صار أي خطأ، تواصل مع الدعم من [بوت التواصل](https://t.me/T3uhBot).**",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_session_id_for_change)

@bot.callback_query_handler(func=lambda call: call.data == "help")
def handle_help_callback(call):
    bot.send_message(
        call.message.chat.id,
        "📘 **تعليمات الاستخدام:**\n\n"
        "1. **عرض يوزرك الحالي:**\n"
        "   - أرسللي السشن آي دي مال حسابك.\n"
        "   - البوت راح يعرضلك يوزرك الحالي على تيك توك.\n\n"
        "2. **تغيير اسم المستخدم:**\n"
        "   - أرسللي السشن آي دي مال حسابك.\n"
        "   - بعدين أرسل الاسم الجديد اللي تريده.\n\n"
        "🔹 **إذا تحتاج مساعدة أكثر، شوف [قناة التعليمات](https://t.me/pyterm1).**",
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "contact_support")
def handle_contact_support_callback(call):
    bot.send_message(
        call.message.chat.id,
        "📩 **إذا تحتاج تتواصل مع الدعم، استخدم الرابط التالي:** [بوت التواصل](https://t.me/T3uhBot)\n\n"
        "🔹 **راح يردون عليك بأسرع وقت ممكن.**",
        parse_mode='Markdown'
    )

def process_session_id_for_profile(message):
    session_id = message.text
    device_id = str(randint(777777788, 999999999999))
    iid = str(randint(777777788, 999999999999))
    
    unique_id = get_profile(session_id, device_id, iid)
    if unique_id != "None":
        bot.send_message(message.chat.id, f"📊 يوزرك الحالي على تيك توك: {unique_id}")
    else:
        bot.send_message(
            message.chat.id,
            "❌ **صار خطأ بالسشن آي دي مالك.**\n"
            "🔹 **شلون تتصرف:**\n"
            "   - تأكد من صحة السشن آي دي.\n"
            "   - حاول ترسل السشن آي دي مرة ثانية.\n"
            "   - إذا المشكلة ما راحت، شوف الشروحات بالقناة هنا: [قناة التعليمات](https://t.me/pyterm1).\n\n"
            "🔸 **للمساعدة السريعة، تواصل مع [بوت التواصل](https://t.me/T3uhBot).**",
            parse_mode='Markdown'
        )

def process_session_id_for_change(message):
    session_id = message.text
    bot.send_message(
        message.chat.id,
        "🔄 **هسة، أرسللي الاسم الجديد اللي تريده:** ✏️\n\n"
        "📘 **إذا تحتاج تعلم شلون تستخدم التشكيل بالاسم، شوف القناة هنا:** [قناة التعليمات](https://t.me/pyterm1)\n\n"
        "🔸 **ملاحظات مهمة:**\n"
        "   - استخدم التشكيل مثل الضمة، الفتحة، الكسرة إذا تحتاج.\n"
        "   - تقدر تضيف نقاط ببداية أو نهاية الاسم.\n"
        "   - تأكد من كتابة الاسم بشكل صحيح عشان ما تصير مشاكل.\n\n"
        "🔹 **إذا تحتاج مساعدة، تواصل مع [بوت التواصل](https://t.me/T3uhBot).**",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler_by_chat_id(message.chat.id, process_new_username, session_id)

def process_new_username(message, session_id):
    new_username = message.text
    device_id = str(randint(777777788, 999999999999))
    iid = str(randint(777777788, 999999999999))

    last_username = get_profile(session_id, device_id, iid)
    if last_username == "None":
        bot.send_message(
            message.chat.id,
            "❌ **صار خطأ بالسشن آي دي مالك.**\n"
            "🔹 **شلون تتصرف:**\n"
            "   - تأكد من صحة السشن آي دي.\n"
            "   - حاول ترسل السشن آي دي مرة ثانية.\n"
            "   - إذا المشكلة استمرت، حاول تضيف التشكيل أو النقاط بالاسم.\n\n"
            "🔸 **للمساعدة السريعة، تواصل مع [بوت التواصل](https://t.me/T3uhBot).**",
            parse_mode='Markdown'
        )
        return

    # إرسال رسالة تتغير بمرور الوقت لتوضيح تقدم عملية تغيير اسم المستخدم
    for i in range(3):
        bot.send_message(
            message.chat.id,
            f"🔄 **جارٍ تغيير اسم المستخدم...** ({i+1}/3)"
        )
        sleep(1)  # تأخير بين الرسائل للتأثير الديناميكي
    
    result = change_username(session_id, device_id, iid, last_username, new_username)
    bot.send_message(message.chat.id, result)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=10)  # مهلة الاتصال 10 ثوانٍ
        except requests.exceptions.ReadTimeout:
            print("Read timeout occurred. Retrying...")
        except Exception as e:
            print(f"An error occurred: {e}")
            sleep(5)  # تأخير بسيط 5 ثوانٍ قبل إعادة المحاولة