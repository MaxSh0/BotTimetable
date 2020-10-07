import config
import telebot
import re
import json
import datetime

bot = telebot.TeleBot(config.TOKEN)

def Today():
    with open('timetable.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    now = datetime.datetime.now()
    i = 0
    for Day in text:
        textDay = re.sub(r'\d+','',Day,flags=re.UNICODE)
        for CurDate in text[Day]['Date']:
            if (now.strftime("%d-%m-%Y") == CurDate):
                TextSubject = "\n";
                for Subject in text[Day]['Subjects']:
                    TextSubject = TextSubject + Subject + "  " + text[Day]['Time'][i] + "\n"
                    i += 1
                fulltext = textDay+"\nДата: " + CurDate + "\nПредметы: " + TextSubject
    return fulltext

def Tomorrow():
    with open('timetable.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    today = datetime.datetime.now()
    tomorrow = today + datetime.timedelta(days=1)
    i = 0
    for Day in text:
        textDay = re.sub(r'\d+', '', Day, flags=re.UNICODE)
        for CurDate in text[Day]['Date']:
            if (tomorrow.strftime("%d-%m-%Y") == CurDate):
                TextSubject = "\n";
                for Subject in text[Day]['Subjects']:
                    TextSubject = TextSubject + Subject + "  " + text[Day]['Time'][i] + "\n"
                    i += 1
                fulltext = textDay+"\nДата: " + CurDate + "\nПредметы: " + TextSubject
    return fulltext

def All():
    with open('timetable.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
        fulltext = ""
        i = 0
    for Day in text:
        textDay = Day
        TextDate = ""
        for CurDate in text[Day]['Date']:
            TextDate += CurDate + " "
            TextSubject = "\n";
            for Subject in text[Day]['Subjects']:
                TextSubject = TextSubject + Subject + "  " + text[Day]['Time'][i] + "\n"
                i += 1
            i = 0
            AllDayText = textDay + "\nДата: " + TextDate + "\nПредметы: " + TextSubject + "\n\n"
        fulltext = fulltext + AllDayText
    return fulltext

def Week(): #TO DO
    return 0


def definition_of_the_week():
    with open('timetable.json', 'r', encoding='utf-8') as f:
        text = json.load(f)
    today = datetime.datetime.now()
    for Day in text:
        for CurDate in text[Day]['Date']:
            if (today.strftime("%d-%m-%Y") == CurDate):
                if(re.search(r'1',Day) !=None):
                    return '1'
                else:
                    return '2'

@bot.message_handler(commands=['start'])
def welcome(massage):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttonToday = telebot.types.KeyboardButton('Сегодня')
    buttonTomorrow = telebot.types.KeyboardButton('Завтра')
    buttonAll = telebot.types.KeyboardButton('Общее')
    markup.add(buttonToday,buttonTomorrow,buttonAll)
    bot.send_message(massage.chat.id, "Расписание 4.1 курс", reply_markup=markup)




@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    if message.chat.type == 'private':
        if(re.search(r'(П|п)ривет|(З|з)дравствуй|(Х|х)ей|(Х|х)елло|(H|h)ello',message.text) != None):
            bot.send_message(message.chat.id, "Ну здравствуй, сталкер")
        elif(re.search(r'(h|H)elp|(п|П)омощь|(П|п)омоги',message.text) !=None):
            bot.send_message(message.chat.id, "Команды:\nСегодня\nЗавтра\nНеделя\nОбщее")
        elif(re.search(r'(С|с)егодня',message.text) !=None):
            bot.send_message(message.chat.id, Today())
        elif(re.search(r'(З|з)автра',message.text) !=None):
            bot.send_message(message.chat.id, Tomorrow())
        elif(re.search(r'(О|о)бщее',message.text) !=None):
            bot.send_message(message.chat.id, All())
        else:
            bot.send_message(message.chat.id, "Ключевые слова не найдены")





if __name__ == '__main__':
    bot.polling(none_stop=True)



