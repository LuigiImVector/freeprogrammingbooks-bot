import telebot
from telebot import types
from flask import Flask, request
import requests
import re
import os
import sqlite3


TOKEN = "2112871440:AAG_klNRhGq6Ruhq_uPB45sw7QMQ_MdAJqk"
bot = telebot.TeleBot(TOKEN)

server = Flask(__name__)

urlDb = "database.db"

if not os.path.isfile(urlDb):
    print("Database not found!")
else:
    conn=sqlite3.connect(urlDb, check_same_thread=False)
    cursor=conn.cursor()
    print("Database connected!")

# only for testing 
#@bot.message_handler(commands=['del'])
#def del_tmp(message):
#    cursor.execute('DELETE FROM fpb')
#    conn.commit()

def log(message, text):
    print(message.chat.first_name+"@"+message.chat.username+" >> "+message.text)
    print("Free Programming Books@freeprogrammingbooks_bot >> "+text+"\n")


@bot.message_handler(commands=['start'])
def start_message(message):
    text = "Hello \U0001F44B\nThis is the un-official bot of [EbookFoundation/free-programming-books](https://github.com/EbookFoundation/free-programming-books/), you can find free resources easily.\n\nType /howto for understanding how to use the bot."

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )

    log(message, text)

    cursor.execute('SELECT * FROM fpb WHERE id=?;', (message.chat.id,))

    defaultCategory = "books/free-programming-books-langs.md"

        
    if cursor.fetchone() is not None:
        print("Username already saved")
    else:
        cursor.execute('INSERT INTO fpb(id, username, choice) VALUES (?, ?, ?);', (message.chat.id, message.chat.username, defaultCategory,))
        conn.commit()
        print("Username saved")

@bot.message_handler(commands=['howto'])
def howto(message):
    text = "*INSTRUCTIONS* ⚙️\n\n*Index*:\nType /index to see the index of the current file.\n\n*Change category*:\nType /category and write in the chat the exactly name of the category (default is `books/free-programming-books-langs.md`).\n\n*Search resources*:\nType /search and then write the name of the sub-category (Android, Java, PHP...).\n\n*Contact the support*:\nType /support to know how to contact support.\n\nIf you want to contribute to this repository check [this](https://github.com/EbookFoundation/free-programming-books/blob/main/CONTRIBUTING.md)."

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )

    log(message, text)

@bot.message_handler(commands=['index'])
def index(message):
    categoryName = cursor.execute('SELECT choice FROM fpb WHERE id=?', (message.chat.id,))
    categoryName = categoryName.fetchall()
    categoryName = ''.join(categoryName[0])
    category = "https://raw.githubusercontent.com/EbookFoundation/free-programming-books/master/" + categoryName

    r = requests.get(category)
    f = r.text
    f = f.splitlines()

    check = False
    text = ""

    for line in f:
        if line == "### Index":
            check = True
            text += "*Index* of `" + categoryName + "`\n\n"
        elif line[:1] == "#" and check:
            check = False
            break

        if check and re.findall(r'\((.*?)\)', line):
            tmp = re.findall(r'\[(.*?)\]', line)
            text += tmp[0] + "\n"

    bot.reply_to(
            message,
            text,
            parse_mode="markdown"
        )

    log(message, text)

@bot.message_handler(commands=['category'])
def select_category(message):
    categoryFile = requests.get('https://raw.githubusercontent.com/EbookFoundation/free-programming-books/master/README.md')
    categoryFile = categoryFile.text
    categoryFile = categoryFile.replace("####", "###")
    categoryFile = categoryFile.splitlines()

    check = False
    text = ""

    for line in categoryFile:
        if line == "### Books":
            check = True
        elif line == "## License":
            check = False
            break

        if check and line[:1] == "#":
            line = line.replace("### ", "")
            text += "\n*" + line + "*\n"
        
        if check and re.findall(r'[^\(]+\.md(?=\))', line):
            tmp = re.findall(r'[^\(]+\.md(?=\))', line)
            text += "`" + tmp[0] + "`\n"
       
    global categoryMessage
    categoryMessage = text
    categoryMessage = categoryMessage.replace("`", "")

    keyboard=types.InlineKeyboardMarkup(row_width=1)
    cancelButton=types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(cancelButton)

    bot.register_next_step_handler(
        bot.send_message(
            message.chat.id,
            text,
            reply_markup=keyboard,
            parse_mode="markdown"
        ),
        change_category
    )

    log(message, text)
    
def change_category(message):
    check = False

    categoryFile = requests.get('https://raw.githubusercontent.com/EbookFoundation/free-programming-books/master/README.md')
    categoryFile = categoryFile.text
    categoryFile = categoryFile.splitlines()

    text = "Not correct"

    for line in categoryFile:
        if re.findall(r'[^\(]+\.md(?=\))', line):
            tmp = re.findall(r'[^\(]+\.md(?=\))', line)
            tmp = "" + str(tmp[0])
            if tmp == message.text:
                cursor.execute('UPDATE fpb SET choice=? WHERE id=?', (message.text, message.chat.id,))
                conn.commit()
                check = True
                text = "Updated"
    
    bot.reply_to(
        message,
        text,
        parse_mode="markdown"
    )

    log(message, text)

@bot.message_handler(commands=['search'])
def search_resource(message):
    text = "Searching..."
    keyboard=types.InlineKeyboardMarkup(row_width=1)
    cancelButton=types.InlineKeyboardButton(text="Cancel", callback_data="cancel")
    keyboard.add(cancelButton)
    bot.register_next_step_handler(
        bot.reply_to(
            message,
            text,
            reply_markup=keyboard,
            parse_mode="markdown"
        ),
        print_resource
    )

    log(message, text)

def print_resource(message):
    category = cursor.execute('SELECT choice FROM fpb WHERE id=?', (message.chat.id,))
    category = category.fetchall()
    category = ''.join(category[0])
    category = "https://raw.githubusercontent.com/EbookFoundation/free-programming-books/master/" + category

    r = requests.get(category)
    f = r.text
    f = f.replace("####", "###")
    f = f.splitlines()
    t = message.json

    search = "### " + str(t['text']) # improve name
    
    check = False
    text = ""

    for line in f:
        if line.lower() == search.lower():
            line = line.replace("### ", "")
            text += "*" + line + "*\n"
            check = True
    
        if check:
            if line[:1] == "*":
                line = line[:0] + "- " + line[2:]
                text += line + "\n"
            elif line == "":
                text += line + "\n"
            elif line[:1] == "#":
                check = False
                break
    
    
    
    if text.count("\n") < 3:
        text = "\U0000274c No resource found \U0000274c"
    bot.reply_to(
        message,
        text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )

    log(message, text)

@bot.message_handler(commands=['support'])
def support(message):
    text = "For any issues you can contact the bot and github repository support at: github.com/EbookFoundation/free-programming-books/issues"

    bot.send_message(
        message.chat.id,
        text,
        parse_mode="markdown",
        disable_web_page_preview=True
    )

    log(message, text)

@bot.callback_query_handler(lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "cancel":
            text = "Operation cancelled"
            bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
        
        bot.send_message(
                call.from_user.id,
                text
                )

        print("Free Programming Books@freeprogrammingbooks_bot >> "+text+"\n") # log

@bot.message_handler(func=lambda message: True)
def error_message(message):
    text = "Incorrect command"
    bot.send_message(
        message.chat.id,
        text
    )

    log(message, text)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://freeprogrammingbooks-bot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == '__main__':
    bot.infinity_polling()  # keep running even if there are errors3
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))
