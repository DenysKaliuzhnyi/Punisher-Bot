import rw
from main import bot

file_of_members = r'~/members.txt'
members = eval(rw.read_last_line_of_file(file_of_members))

################################new_chat_members################################


def allow_add_member(message):
    chat_id = message.chat.id
    username = message.new_chat_member.username
    if username is None:
        username = message.new_chat_member.first_name
    user_id = message.new_chat_member.id
    user = (username, user_id)
    return user not in members[chat_id] and not message.new_chat_member.is_bot

def add_member(message):
    chat_id = message.chat.id
    username = message.new_chat_member.username
    if username is None:
        username = message.new_chat_member.first_name
    user_id = message.new_chat_member.id
    user = (username, user_id)
    members[chat_id].append(user)

def send_greetings(message):
    chat_id = message.chat.id
    username = message.new_chat_member.username
    if username is None:
        username = message.new_chat_member.first_name
    msg = "Ласкаво просимо, @{0}!".format(username)
    bot.send_message(chat_id, msg)


################################left_chat_member################################


def allow_remove_member(message):
    chat_id = message.chat.id
    username = message.left_chat_member
    if username is None:
        username = message.left_chat_member.first_name
    user_id = message.left_chat_member.id
    user = (username, user_id)
    return user in members[chat_id]

def remove_member(message):
    chat_id = message.chat.id
    username = message.left_chat_member.username
    if username is None:
        username = message.left_chat_member.first_name
    user_id = message.left_chat_member.id
    user = (username, user_id)
    members[chat_id].remove(user)

def send_parting(message):
    chat_id = message.chat.id
    username = message.left_chat_member.username
    if username is None:
        username = message.left_chat_member.first_name
    msg = "Прощайте, @{0}!".format(username)
    bot.send_message(chat_id, msg)


###############################remove_participant###############################

def check_valid_syntax(message):
    content = message.text
    return content.count('[') == 1 and content.count(']') == 1 and content.find('[')+1 < content.find(']')

def get_username_from_text(content):
    return content.split('[')[1].split(']')[0].strip(' ').replace('@', '')

def send_invalid_syntax(message):
    chat_id = message.chat.id
    msg = 'команда має структуру: /remove_participant [username] \n' \
          'у квадратних дужках вказується юзернейм вилучаємого зі списку'
    bot.send_message(chat_id, msg)


def is_group(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    return chat_id != user_id

def send_isnt_group(message):
    chat_id = message.chat.id
    msg = "вибачте, дана команда не доступна у приватній бесіді"
    bot.send_message(chat_id, msg)

def is_called_by_admin(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    admins = bot.get_chat_administrators(chat_id)
    admins_id = [admin.user.id for admin in admins]
    return user_id in admins_id

def send_refuse(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    msg = "Вибачте, @{0}, дана команда доступна лише для адміністраторів".format(username)
    bot.send_message(chat_id, msg)

def remove_member_by_command(message):
    chat_id = message.chat.id
    content = message.text
    rm_username = get_username_from_text(content)
    for user in members[chat_id]:
        if user[0] == rm_username:
            members[chat_id].remove(user)
            return True
    return False

def send_member_removed(message):
    chat_id = message.chat.id
    content = message.text
    rm_username = get_username_from_text(content)
    msg = "@{0} вилучено зі списку. Повернутись до списку можна лише за виконанням відповідної команди самим юзером".format(rm_username)
    bot.send_message(chat_id, msg)

def send_member_not_exists(message):
    chat_id = message.chat.id
    msg = "такого учасника не існує!"
    bot.send_message(chat_id, msg)


###############################add_me_to_participants###########################


def add_member_by_command(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    user = (username, user_id)
    members[chat_id].append(user)

def is_in_participants(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    user = (username, user_id)
    return user in members[chat_id]

def send_add_refuse(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    msg = "@{0}, ви вже є у списку!".format(username)
    bot.send_message(chat_id, msg)

def send_participant_added(message):
    chat_id = message.chat.id
    username = message.from_user.username
    if username is None:
        username = message.from_user.first_name
    msg = "@{0}, вас додано до списку. Тепер вилучити вас може лише адміністратор!".format(username)
    bot.send_message(chat_id, msg)

def is_chat_registered(message):
    chat_id = message.chat.id
    return chat_id in members.keys()

def add_chat(message):
    chat_id = message.chat.id
    members.update({chat_id: []})


###############################rules############################################


def send_rules(message):
    chat_id = message.chat.id
    msg = "Всім привіт! Даний бот призначений для обирання випадкогово учасника чату, який належить до відповідного списку."\
        " Даний список формується автоматично - юзер додається до нього, коли приєднується до чату та вилучається у випадку покидання." \
        " Також ці команди доступі мануально: додати юзера - це може зробити лише сам юзер; вилучити юзера - це може зробити лише адміністратор групи"\
        " (отже, щоб самостійно не доводилось додавати кожного юзера, під час створення групи до учасників требя включити лише Punisher'a, а потім додати всіх людей)."\
        " Жоден бот не може бути в списку. Використовуйте відповідну команду для обирання випадкового учасника чату."
    bot.send_message(chat_id, msg)


###############################other############################################

def is_no_participants(message):
    chat_id = message.chat.id
    return len(members[chat_id]) == 0

def send_no_participants(message):
    chat_id = message.chat.id
    msg = 'список порожній!'
    bot.send_message(chat_id, msg)
