import json
import requests
#### My Bot ###
import telebot

from telebot import types


TOKEN = '1287299690:AAHxBShPZa4D7Yz5HP6_x1Pe8WuU1HM5-cQ'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

welcome_text ="""Welcome to MyTipBot, a Telegram Tipper Bot for multiple blockchains. Click the Menu icon to get started.

Getting Started
MyTipBot automatically generates a wallet address for you on multiple blockchains. Currently, these are Binance BNB.

Select which wallet you would like to open by pressing the 🏦 Wallets button.
Check your public deposit address for each blockchain by pressing the 🔤 Address button."""


welcome_text1 ="""Click on the button below, choose the group and start tipping your friends! """

#@bot.message_handler(commands=['help'])
#def send_welcome(message):
#	bot.reply_to(message, "HowDy, how are you doing?")

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)

@bot.message_handler(regexp="HELP")
def handle_message(message):
	bot.reply_to(message, "HELP HERE") 


@bot.message_handler(regexp="wallet")
def handle_message(message):
	bot.reply_to(message, message)

##########  Button Pallete  ##########
@bot.message_handler(regexp="/start")
def handle_message(message): 
	markup = types.ReplyKeyboardMarkup(row_width=1)
	itmBtn1 = types.KeyboardButton('Help')
	itmBtn2 = types.KeyboardButton('🏦 Wallet')
	itmBtn3 = types.KeyboardButton('🎁 Airdrop')
	markup.add(itmBtn1,itmBtn2,itmBtn3)
	#bot.send_message(message.chat.id, welcome_text)
	bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
	inline_markup = types.InlineKeyboardMarkup()
	inline_markup.add(types.InlineKeyboardButton(text="Add MyTipBot to your Group", url= "http://google.com", callback_data="callback_btn"))
	bot.send_message(message.chat.id, welcome_text1, reply_markup=inline_markup)


@bot.message_handler()
def handle_message(message):
	bot.reply_to(message, message.chat.id)

bot.polling()

#url = "https://api.telegram.org/bot1287299690:AAHxBShPZa4D7Yz5HP6_x1Pe8WuU1HM5-cQ/getMe"
#parameters = {
#	"chat_id":"1287299690",
#	"text": "/HEllo"
#}
#response = requests.post(url)
#x = json.loads(json.dumps(response.json()))
#id = "@"+str(x["result"]["id"])
#print (x)

#parameters = {
#	"chat_id": '@kurdish_bot',
#	"text": "/HELLO"
#}
#par = {
#	"chat_id": id,
#	"text": "\/Dice"
#}
#res = requests.post("https://api.telegram.org/bot1287299690:AAHxBShPZa4D7Yz5HP6_x1Pe8WuU1HM5-cQ/sendMessage",params=parameters);
#print(res.json())
