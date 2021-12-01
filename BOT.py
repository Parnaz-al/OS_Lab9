import telebot
import qrcode
from gtts import gTTS
from khayyam import JalaliDatetime
bot = telebot.TeleBot("2147078247:AAH3TdUwzK2huDFX-Eg97LY6i9ODSQpNhhI")


@bot.message_handler(commands=['help'])
def help_func(message):
 bot.reply_to(message,"/start ->welcome to bot\n /game ->play a game \n/age ->calculate your age  \n/voice -> convert text to voice \n /max -> find max number \n /argmax -> find index of max number \n /qrcode -> make Qrcode \n /help -> menu" )



@bot.message_handler(commands=['start'])
def salam(message):
    bot.reply_to (message,"Welcome " +  message.chat.first_name)


@bot.message_handler(commands=['qrcode'])

def send(message):
    sent=bot.send_message(message.chat.id,"send me your text:")
    bot.register_next_step_handler(sent,make)
def make(message):
    url=qrcode.make(message.text)
    url.save("url.png")
    bot.send_photo(message.chat.id,open("url.png","rb"))




@bot.message_handler(commands=['argmax'])
def Argmax(message):
    array1 = bot.send_message(message.chat.id, "Enter your numbers")
    bot.register_next_step_handler(array1, index_max)

def index_max(array1):
    array2 = list(map(int,array1.text.split(',')))
    index = array2.index(max(array2)) + 1

    bot.send_message(array1.chat.id, "index of max number is "+str(index))




@bot.message_handler(commands=['max'])
def max1(message):
    array1=bot.send_message(message.chat.id,"Enter your numbers please")
    bot.register_next_step_handler(array1,max2)
def max2(message):
         array2=list(map(int,message.text.split(",")))
         bot.reply_to(message=message,text="Max is "+str(max(array2)))
   
       


@bot.message_handler(commands=['voice'])
def text_to_voice1(message):
    text1 = bot.send_message(message.chat.id, 'enter the english text')
    bot.register_next_step_handler(text1,text_to_voice2)

def text_to_voice2(text1):

        text2 = text1.text
        language = 'en'
        v = gTTS(text=text2, lang=language, slow=False)
        v.save("v.mp3")
        voice = open('v.mp3', 'rb')
        bot.send_voice(text1.chat.id, voice)
   



@bot.message_handler(commands=['age'])
def age1(message):
    date = bot.send_message(message.chat.id, "Enter your birthday" )
    bot.register_next_step_handler(date,age2)

def age2(date):
    spl = (date.text).split("/")
    rem = JalaliDatetime.now() - JalaliDatetime(spl[0],spl[1],spl[2])
    bot.send_message(date.chat.id,str(rem))



@bot.message_handler(func=lambda message:True)
def echo(message):
  bot.reply_to(message,"I can't undrestand")
bot.infinity_polling()


