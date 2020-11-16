import json
import requests
#### My Bot ###
import telebot
from telebot import types
import logging
import pymongo
logger = telebot.logger
from binance_chain.wallet import Wallet
from binance_chain.environment import BinanceEnvironment
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bnbwalletsdb"]
mycol = mydb["wallets"]

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
	bot.reply_to(message, message.from_user.id)

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
	#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	p = call.message.json
	chat_id = p["chat"]["id"]
	#print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	d = str(call.data)
	if d == "callbackbnb_addr":
		testnet_env = BinanceEnvironment.get_testnet_env()
		wallet = Wallet.create_random_wallet(env=testnet_env)
		print(wallet.ToJson())
		#print(">>>>>>>>$$$$$$$<<<<<<<<<")
		#print(wallet.address)
		#print(wallet.private_key) 
		#print("Hello")
		findtelegram = { "telegram_id": call.from_user.id }
		mydoc = mycol.find(findtelegram)
		if mydoc.count() > 0:
			for x in mydoc:
				######print(x)
				obj = {}
				obj["address"] = x["address"]
				######Send wallet  details to user
				bot.send_message(chat_id, x["address"])
			return
		else:
			myjsondata = { "telegram_id": call.from_user.id, "address": wallet.address, "privateKey": wallet.private_key }
			x = mycol.insert_one(myjsondata)
			bot.send_message(chat_id, wallet.address)
	if d == "callbackbnb_bal": 
		print("Hi")
	if d == "callbackbnb_pk": 
		print("hola")

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
