import telebot

# Initialize the bot with the token
TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)

# Handle command /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Welcome! Please select an option below:')
    # Create buttons
    keyboard = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton(text='Option 1', callback_data='option_1')
    button2 = telebot.types.InlineKeyboardButton(text='Option 2', callback_data='option_2')
    keyboard.add(button1, button2)
    bot.send_message(message.chat.id, 'Choose:', reply_markup=keyboard)

# Handle callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'option_1':
        bot.send_message(call.message.chat.id, 'You selected Option 1!')
    elif call.data == 'option_2':
        bot.send_message(call.message.chat.id, 'You selected Option 2!')
    bot.answer_callback_query(call.id)

# Start polling
if __name__ == '__main__':
    bot.polling()