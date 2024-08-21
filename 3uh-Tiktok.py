import telebot
from telebot import types

# Your bot token
bot = telebot.TeleBot("7480473881:AAFvgLeXIN_3Emb5ikfpAvHUito3kKub48A")

# Telegram Bot Handlers

@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("عرض القناة", url="https://t.me/pyterm1")
    item2 = types.InlineKeyboardButton("تواصل مع الدعم", url="https://t.me/t3uhBot")
    markup.add(item1, item2)
    
    bot.send_message(
        message.chat.id,
        " اهلا وسهلا صديقي ✨️\n\n"
        "🔧 **البوت حاليا قيد التحديث.**\n\n"
        "📢 **تابع القناة هنا:** [قناة التعليمات](https://t.me/pyterm1)\n"
        "📩 **إذا تحتاج مساعدة، تواصل مع الدعم من خلال بوت التواصل هنا:** [بوت التواصل](https://t.me/t3uhBot)\n\n"
        "🔹 **راح نعلمك أول ما يخلص التحديث. شكراً لصبرك.**",
        parse_mode='Markdown',
        reply_markup=markup
    )

if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=10)