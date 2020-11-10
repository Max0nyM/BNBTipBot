import json
import requests
#### My Bot ###
import telebot
from telebot import types
import logging
logger = telebot.logger
#telebot.logger.setLevel(logging.DEBUG)

TOKEN = '1287299690:AAHxBShPZa4D7Yz5HP6_x1Pe8WuU1HM5-cQ'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

BOTNAME='MykurdishBot' 

welcome_text ="""Welcome to MyTipBot, a Telegram Tipper Bot for multiple blockchains. Click the Menu icon to get started.

Getting Started
MyTipBot automatically generates a wallet address for you on multiple blockchains. Currently, these are Binance BNB.

Select which wallet you would like to open by pressing the 🏦 Wallets button.
Check your public deposit address for each blockchain by pressing the 🔤 Address button."""

welcome_text1 ="""Click on the button below, choose the group and start tipping your friends! """

wallet_text = """Binance DEX - BEP-20 BNB 

Description
Binance DEX refers to the decentralized exchange features developed on top of Binance Smart Chain.

Links
🌐 Website (https://www.binance.org/en/smartChain)
🐦 Twitter (https://twitter.com/binance_dex) """


#@bot.message_handler(commands=['help'])
#def send_welcome(message):
#	bot.reply_to(message, "HowDy, how are you doing?")

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)

@bot.message_handler(regexp="HELP")
def handle_message(message):
	bot.reply_to(message, "HELP HERE") 


@bot.message_handler(regexp="wt")
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
	inline_markup.add(types.InlineKeyboardButton(text="Add MyTipBot to your Group", url="https://telegram.me/"+BOTNAME+"?startgroup=true"))
	bot.send_message(message.chat.id, welcome_text1, reply_markup=inline_markup)



@bot.message_handler(regexp="🏦 Wallet")
def handle_message(message):
	myinline_markup = types.InlineKeyboardMarkup()
	myinline_markup.add(
		types.InlineKeyboardButton(text="🔤 Address", callback_data="callbackbnb_addr"),
		types.InlineKeyboardButton(text="💰 Balance", callback_data="callbackbnb_bal"),
		types.InlineKeyboardButton(text="🔑 Private Key", callback_data="callbackbnb_pk")
	)

	bot.send_message(message.chat.id, wallet_text, reply_markup=myinline_markup)


###### CALL BACK QUERY HANDLER 
@bot.callback_query_handler(func=lambda call: True)
def callbackbnb_addr(call):
	if call.data == "callbackbnb_addr":
		print(call.data)

	if call.data == "callbackbnb_bal":
		print(call.data)

        if call.data == "callbackbnb_pk":
		print(call.data)


###### FOR ANY OTHER NONSENSE TEXT #####    DELETE  TEXT/CHAT TEXT ######## REMAIN
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
