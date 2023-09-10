from typing import Dict, Any
import Data
import telebot
import EmailConfirm as ec
from  DBControler import  Connection as dbc

API_TOKEN = '6420379111:AAH8anDwpxdg6jI2ReRbQ_Ky_fMSH9DCSQw'
bot = telebot.TeleBot(API_TOKEN)

server = 'DESKTOP-VONE3CS\SQLEXPRESS'
database = 'GenerateS_Database'
users: dict[Any, Any] = {}
isSignUp = {}
isSignIn = {}
dataForGenerationId = [None, None, None]
listOfCommands = ['/start', 'Зарегистрироваться', 'Войти']
waiting_admin_confirmation = {}
currentUserId = None
admin_user_id = '1267059395' #'5439246019'

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True)
    item_start = telebot.types.KeyboardButton('/start')
    item_reg = telebot.types.KeyboardButton('Зарегистрироваться')
    item_login = telebot.types.KeyboardButton('Войти')
    markup.row(item_start, item_reg, item_login)
    currentUserId = message.chat.id
    dataForGenerationId = [None, None, None]
    isSignUp = False
    isSignIn = False
    bot.send_message(message.chat.id, f"Привет! Что бы вы хотели сделать: зарегистрироваться или войти?",
                     reply_markup=markup)


def save_user_info(user_id, key, value):
    if user_id not in users:
        users[user_id] = {}
    users[user_id][key] = value


def get_user_info(user_id, key):
    return users.get(user_id, {}).get(key)


def clear_user_data(user_id):
    users.pop(user_id, None)


def generate_student_id(user_id):
    country = dataForGenerationId[0]
    city = dataForGenerationId[1]
    school = dataForGenerationId[2]
    unique_id = user_id % 1000 # Получаем последние 4 цифры user_id
    return f"{country}-{city}-{school}-{unique_id}"


def check_by_comands(msg):
    for command in listOfCommands:
        if msg == command:
            return False
    return True

def save_user_info_to_db(user_id):
    con = dbc(server, database)
    con.insert(get_user_info(user_id, 'surname'), get_user_info(user_id, 'name'), get_user_info(user_id, 'country'),
               get_user_info(user_id, 'region'), get_user_info(user_id, 'city'), get_user_info(user_id, 'school'),
               get_user_info(user_id, 'email'),get_user_info(user_id, 'phone'), get_user_info(user_id, 'password'), generate_student_id(user_id))
    con.select('Accounts')
    con.close()



def check_login(login):
    check = dbc('DESKTOP-VONE3CS\SQLEXPRESS', 'GenerateS_Database').search('Accounts' ,'email', login)
    return (login != 'Зарегистрироваться' and login != 'Войти' and not login.startswith(
        '/') and '@' in login and '.' in login and check)


def check_pass(password):
    check = dbc('DESKTOP-VONE3CS\SQLEXPRESS', 'GenerateS_Database').search('Accounts' ,'pass', password)
    return (6 <= len(password) <= 25 and not password.startswith('/') and check)



@bot.message_handler(func=lambda message: message.text == 'Зарегистрироваться' )
def registration(message):
    if isSignUp == True:
        bot.send_message(message.chat.id, "Вы уже зарегистрировались.")
        return
    save_user_info(message.chat.id, 'isSignUp', False)
    bot.send_message(message.chat.id, "Введите свою фамилию:")
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    save_user_info(message.chat.id, 'surname', message.text)
    bot.send_message(message.chat.id, "Введите своё имя:")
    bot.register_next_step_handler(message, get_name)


def get_name(message):
    save_user_info(message.chat.id, 'name', message.text)
    bot.send_message(message.chat.id, "Введите страну:")
    bot.register_next_step_handler(message, get_country)


def get_country(message):
    country = Data.check_country(message.text)
    if country == None:
        bot.send_message(message.chat.id, "Неверная страна! Повторите попытку:")
        bot.register_next_step_handler(message, get_country)
        return
    save_user_info(message.chat.id, 'country', message.text)
    dataForGenerationId[0] = country
    print(dataForGenerationId[0])
    bot.send_message(message.chat.id, "Введите регион:")
    bot.register_next_step_handler(message, get_region)


def get_region(message):
    save_user_info(message.chat.id, 'region', message.text)
    bot.send_message(message.chat.id, "Введите город:")
    bot.register_next_step_handler(message, get_city)


def get_city(message):
    con = dbc(server, database)
    city = con.search('Cities', 'name', message.text)
    con.close()

    if city is not None:
        cityid = city[1]

        dataForGenerationId[1] = cityid
    else:
        con1=dbc(server, database)

        rows_count = con1.request("SELECT COUNT(*) FROM Cities")
        cityid = rows_count[0] + 1
        con1.close()
        conn = dbc(server, database)

        conn.insertCountry(f"INSERT INTO Cities(name, num) VALUES('{message.text}', {cityid})")

        conn.close()

        dataForGenerationId[1] = cityid


    save_user_info(message.chat.id, 'city', message.text)
    bot.send_message(message.chat.id, "Введите название школы:")
    bot.register_next_step_handler(message, get_school)


def get_school(message):
    num = ''.join(filter(str.isdigit, message.text))
    if num == '':
        bot.send_message(message.chat.id, "Название должно содержать номер школы:")
        bot.register_next_step_handler(message, get_school)
        return
    dataForGenerationId[2] = num
    save_user_info(message.chat.id, 'school', message.text)
    bot.send_message(message.chat.id, "Введите телефон:")
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    save_user_info(message.chat.id, 'phone', message.text)
    bot.send_message(message.chat.id, "Введите e-mail:")
    bot.register_next_step_handler(message, get_email)


def get_email(message):
    email = message.text
    code = ec.generate_verification_code()
    is_confirmed = ec.send_verification_email(email, code)

    if is_confirmed:
        save_user_info(message.chat.id, 'email', email)
        save_user_info(message.chat.id, 'verification_code', code)
        bot.send_message(message.chat.id, "Вам на почту отправлен код. Введите его для подтверждения почты:")
        bot.register_next_step_handler(message, get_verification_code)
    else:
        bot.send_message(message.chat.id, "Ошибка! Пожалуйста, введите существующую почту:")
        bot.register_next_step_handler(message, get_email)


def get_verification_code(message):
    user_id = message.chat.id
    user_code = message.text
    saved_code = get_user_info(user_id, 'verification_code')

    if user_code == saved_code:
        bot.send_message(user_id, "Придумайте надёжный пароль:")
        bot.register_next_step_handler(message, get_password)
    else:
        bot.send_message(user_id, "Неверный код! Попробуйте ещё раз:")
        bot.register_next_step_handler(message, get_verification_code)


def get_password(message):
    if(len(message.text) >= 6 and message.text[0] != '/' and len(message.text) <= 25):
         users[message.chat.id]['password'] = message.text
         isSignUp[message.chat.id] = True
         bot.send_message(message.chat.id, "Подтвердите личность документом, содержащим вашу фамилию и имя:")
         users[message.chat.id]['wait_for_confirmed'] = 0
    else:
        bot.send_message(message.chat.id, """Пароль должен быть длиной от 6 до 25 символов.
            Повторите попытку:""")
        bot.register_next_step_handler(message, get_password)


@bot.message_handler(content_types=['document'])
def handle_document(message):
    # Сохраняем информацию о файле для ожидания подтверждения админом
    waiting_admin_confirmation[message.from_user.id] = {'file_id': message.document.file_id,
                                                        'file_name': message.document.file_name}

    # Отправляем файл админу (замените admin_user_id на ID админа)
    bot.send_document(admin_user_id, message.document.file_id)
    bot.send_message(message.chat.id, "Отправлено. Ожидание регистрации...")

    # Отправляем запрос на подтверждение
    bot.send_message(admin_user_id,
                     f"""Пользователь:
               {get_user_info(message.from_user.id, 'surname')}
               {get_user_info(message.from_user.id, 'name')}
               {get_user_info(message.from_user.id, 'country')}
               {get_user_info(message.from_user.id, 'region')}
               {get_user_info(message.from_user.id, 'city')}
               {get_user_info(message.from_user.id, 'school')}
               {get_user_info(message.from_user.id, 'email')}
               {get_user_info(message.from_user.id, 'phone')}
               {generate_student_id(message.from_user.id)}""")
    global currentUserId
    currentUserId = message.from_user.id
    bot.register_next_step_handler_by_chat_id(admin_user_id, admin_confirm)


@bot.message_handler(commands=['adminconfirm7428'])
def admin_confirm(message):
    markup = telebot.types.ReplyKeyboardMarkup()
    item_confirm = telebot.types.KeyboardButton('Подтверждаю')
    item_unconfirm = telebot.types.KeyboardButton('Отказ')
    markup.row(item_confirm, item_unconfirm)
    bot.send_message(message.chat.id, "Подтвердите, пожалуйста, личность, написав 'Подтверждаю' или 'Отказ'.", reply_markup=markup)
    bot.register_next_step_handler(message, handle_admin_response)

def handle_admin_response(message):
    print(message.text)
    if message.text == 'Подтверждаю':
        if currentUserId in waiting_admin_confirmation:
            file_name = waiting_admin_confirmation[currentUserId]['file_name']
            user_id = currentUserId
            bot.send_message(admin_user_id, "Заявка принята!")
            bot.send_message(user_id, "Заявка принята! Добро пожаловать!")
            del waiting_admin_confirmation[user_id]
            save_user_info_to_db(user_id)
        else:
            bot.send_message(admin_user_id, "Нет ожидающих подтверждения файлов.")
    elif message.text == 'Отказ':
        if currentUserId in waiting_admin_confirmation:
            file_name = waiting_admin_confirmation[currentUserId]['file_name']
            user_id = currentUserId
            bot.send_message(admin_user_id, f"Заявка не принята!")
            bot.send_message(user_id, f"Заявка не принята!")
            del waiting_admin_confirmation[user_id]
        else:
            bot.send_message(admin_user_id, "Нет ожидающих подтверждения файлов.")


@bot.message_handler(func=lambda message: message.text == 'Войти')
def login(message):
    if isSignIn == True:
        bot.send_message(message.chat.id, "Вы уже вошли.")
        return
    save_user_info(message.chat.id, 'isSignIn', False)
    bot.send_message(message.chat.id, "Введите ваш логин (электронную почту):")
    bot.register_next_step_handler(message, successful_login)


def successful_login(message):
    user_id = message.chat.id
    login = message.text

    if not check_login(login):
        bot.send_message(user_id, "Неверный логин")
        bot.register_next_step_handler(message, successful_login)
        return

    save_user_info(user_id, 'login', login)
    bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(message, get_password_on_sign_in)

def get_password_on_sign_in(message):
    user_id = message.chat.id
    password = message.text

    if not check_pass(password):
        bot.send_message(user_id, "Неверный пароль")
        bot.register_next_step_handler(message, get_password_on_sign_in)
        return

    save_user_info(user_id, 'password', password)
    isSignUp = True
    isSignIn = True
    print(users)
    markup = telebot.types.ReplyKeyboardMarkup()
    item_get_num = telebot.types.KeyboardButton('Получить личный код')
    markup.row(item_get_num)
    bot.send_message(message.chat.id, "Успешный вход! Что вы хотите сделать?", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Получить личный код' )
def get_code(message):
    if isSignIn == False:
        bot.send_message(message.chat.id, "Для начала работы войдите.")
        return
    con = dbc(server, database)
    num = con.request(f"SELECT personal_number FROM Accounts WHERE email='{get_user_info(message.chat.id, 'login')}' AND pass='{get_user_info(message.chat.id, 'password')}'")
    con.close()
    bot.send_message(message.chat.id, num[0])



if __name__ == '__main__':
    bot.polling(none_stop=True)
