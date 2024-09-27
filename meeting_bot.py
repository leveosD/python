import telebot
import datetime

bot = telebot.TeleBot('token')
info = ('Здравствуйте! Это бот, помогающий вам создавать записи о встречах.\nВсё очень просто, просто следуйте инструкциям!\n'
        'Если хотите создать запись прямо сейчас, напишите \'Начать\'.')
repeat_info = 'Если вы хотите создать новую запись, напишите \'Начать\'.'
name = ''
surname = ''
phone = ''
available_symbs = '()-+ '
meeting_date = None
date_format = '%d.%m.%Y'

repeat = False

@bot.message_handler(content_types =['text'])
def start(message):
    global name
    global surname
    global phone
    global meeting_date
    #global assistant
    global thread
    global repeat

    if message.text == 'Начать':
        name = ''
        surname = ''
        phone = ''
        meeting_date = None

        bot.send_message(message.from_user.id, "Введите фамилию.")
        bot.register_next_step_handler(message, get_surname)
    elif not repeat:
        bot.send_message(message.from_user.id, info)
        repeat = True
    else:
        bot.send_message(message.from_user.id, repeat_info)

def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Введите имя')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Введите телефон')
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    global phone
    full_str = message.text
    for i in range(len(full_str)):
        if full_str[i].isdigit():
            phone += full_str[i]
        elif full_str[i] not in available_symbs:
            bot.send_message(message.from_user.id, 'Номер должен содержать только цифры или символы: \"{0}\"'.format(
                available_symbs))
            bot.register_next_step_handler(message, get_phone)
            phone = ''
            return
    if len(phone) > 15:
        bot.send_message(message.from_user.id, 'Этот номер слишком длинный {0}.\nВведите корректный номер.'.format(len(phone)))
        phone = ''
        bot.register_next_step_handler(message, get_phone)
    elif len(phone) < 10:
        bot.send_message(message.from_user.id, 'Этот номер слишком короткий {0}.\nВведите корректный номер.'.format(len(phone)))
        phone = ''
        bot.register_next_step_handler(message, get_phone)
    else:
        bot.send_message(message.from_user.id, 'Введите дату(день.месяц.год):')
        bot.register_next_step_handler(message, get_date)
def get_date(message):
    global meeting_date
    try:
       meeting_date = datetime.datetime.strptime(message.text, date_format)
       result = 'Сделка успешно создана!\nИмя: {0} {1}.\nТелефон: {2}.\nДата: {3}.'.format(surname, name, phone, meeting_date)
       bot.send_message(message.from_user.id, result)
    except:
        bot.send_message(message.from_user.id, 'Введите корректную дату(день.месяц.год):')
        bot.register_next_step_handler(message, get_date)

bot.polling(none_stop=True, interval=0)