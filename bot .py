import telebot
import qrcode
from gtts import gTTS
from khayyam import JalaliDatetime
import random

from telebot.types import Message

bot = telebot.TeleBot("2147078247:AAH3TdUwzK2huDFX-Eg97LY6i9ODSQpNhhI")

@bot.message_handler(commands=['start'])
def salam(message):
    bot.reply_to (message,"Welcome to my bot " +  message.chat.first_name +"😀")



@bot.message_handler(commands=['help'])
def help_func(message):
 bot.reply_to(message,"You can choose:\n/start ->welcome to bot\n/game ->play a game \n/age ->calculate your age  \n/voice -> convert text to voice \n/max -> find max number \n/argmax -> find index of max number \n/qrcode -> make Qrcode \n/help -> menu" )


@bot.message_handler(commands=['qrcode'])


def send(message):
    sent=bot.send_message(message.chat.id,"enter your text please.")
    bot.register_next_step_handler(sent,make)
def make(message):
    img=qrcode.make(message.text)
    img.save("img.png")
    bot.send_photo(message.chat.id,open("img.png","rb"))


@bot.message_handler(commands=['voice'])
def play_voice(message):
    text1 = bot.send_message(message.chat.id,"enter your text please.")
    bot.register_next_step_handler(text1,voice)

def voice(text1):
        text2 = text1.text
        language = 'en'
        v = gTTS(text=text2, lang=language, slow=False)
        v.save("v.mp3")
        bot.send_voice(text1.chat.id, open('v.mp3', 'rb'))
   

@bot.message_handler(commands=['max'])
def max1(message):
    array1=bot.send_message(message.chat.id,"enter your numbers in this format: \"number1,number2,number3,...\"")
    bot.register_next_step_handler(array1,max2)
    
def max2(message):
    try:
         array2=message.text.split(",")
         bot.reply_to(message=message,text="Max is "+(max(array2)))
    except:
        array1 = bot.send_message(message.chat.id,"please enter the numbers in correct format.")
        bot.register_next_step_handler(array1, max1)     

       


@bot.message_handler(commands=['argmax'])

def argmax(message):
    array1 = bot.send_message(message.chat.id, "enter your numbers in this format: \"number1,number2,number3,...\"")
    bot.register_next_step_handler(array1, index_max)

def index_max(array1):
    try:
        array2 = array1.text.split(',')
        m=max(array2)
        index = array2.index(m) + 1
        bot.send_message(array1.chat.id, "index of max number is "+ str(index))
    except:
        array1 = bot.send_message(message.chat.id,"please enter the numbers in correct format.")
        bot.register_next_step_handler(array1, argmax)     
  







@bot.message_handler(commands = ['age'])
def age(message):
    user = bot.send_message(message.chat.id, "enter your birthday in this format: \"1350/2/14\"")
    bot.register_next_step_handler(user,age_calculator)

def age_calculator(message):
    try:
        remainder= JalaliDatetime.now() - JalaliDatetime(message.text.split('/')[0], message.text.split('/')[1], message.text.split('/')[2])
        year = remainder.days // 365
        day = remainder.days % 365
        bot.send_message(message.chat.id, "You have " + str(year) + " years and "  + str(day)  + " days.")
    except:
        user = bot.send_message(message.chat.id,"please enter your age in correct format.")
        bot.register_next_step_handler(user,age)


@bot.message_handler(commands=['game'])
def guess(message):
    global number
    number=random.randint(0,10)
    choice=bot.send_message(message.chat.id,"guess the number between 0-10.")
    bot.register_next_step_handler(choice, game)
def game(choice):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    Button = telebot.types.KeyboardButton('new game')
    markup.add(Button)
    global number

    if choice.text == "new game":
        choice = bot.send_message(choice.chat.id, "You pressed \" new game\" guess the new number between 0-10")
        number= random.randint(0,10)
        bot.register_next_step_handler(choice, game)
    else:  
          
            if int(choice.text) > number:
                choice = bot.send_message(choice.chat.id, "go down ⬇",reply_markup=markup)
                bot.register_next_step_handler(choice, game)
            elif int(choice.text) < number :
                choice=bot.send_message(choice.chat.id,"go up ⬆",reply_markup=markup)
                bot.register_next_step_handler(choice, game)
            else :
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                choice=bot.send_message(choice.chat.id,"you Win!",reply_markup=markup)              


 
@bot.message_handler(func=lambda message:True)
def echo(message):
  bot.reply_to(message,"I can't undrestand.Please try again!")


bot.infinity_polling()
