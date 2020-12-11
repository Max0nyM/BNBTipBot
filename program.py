import json
import requests
import string
import random
#### My Bot ###
import telebot
from telebot import types
import logging
import pymongo
from PIL import Image
import qrcode
import asyncio

from tipper_file import Tipper

from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider)
from eth_account import Account

logger = telebot.logger
#from binance_chain.wallet import Wallet
#from binance_chain.environment import BinanceEnvironment

from eth_wallet import Wallet
from eth_wallet.utils import generate_entropy

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["bnbwalletsdb"]
mycol = mydb["wallets"]

### Binance details
binanceSmartChainTestNet = 'https://data-seed-prebsc-2-s1.binance.org:8545/'

#telebot.logger.setLevel(logging.DEBUG)
TOKEN = '1287299690:AAHxBShPZa4D7Yz5HP6_x1Pe8WuU1HM5-cQ'
bot = telebot.TeleBot(TOKEN, parse_mode=None)

BOTNAME='MykurdishBot'

ADDRESS_BTN_TEXT1=""" <a href="google.com">THIS IS TEXT</a>"""

ADDRESS_BTN_TEXT="""*Address:* {MYADDRESS}

*Receive Address:*
{MYADDRESS}


This is your public deposit address for each blockchain\.

View on [https://bscscan\.org/]

You can change the address on which you receive tips by using the 
[\\wallet] command in private chat with the bot


For example:
[\/wallet  \<chain\>  \<address\>]
[\/wallet  binance  {MYADDRESS}]

If you want to change the receiving wallet back to your original 
Tip bot wallet then use the [\/resetwallet \<chain\>] command in a
private chat with the bot\."""


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


tipcurrency = ['BNB','BUSD','BTCB','ETH','SPX','DOT','CAKE','LINK','ALPHA','XRP','EOS','XVS','ADA','BAND','TWT','DAI','USDC','BURGER',
'YFI','BCH','UNI','LTC','XTZ','CTK','CREAM','BAKE','ONT','FRIES','NAR','DRUGS','GUNS','NYA','SPARTA']

myqrcodeinline_markup = types.InlineKeyboardMarkup()
myqrcodeinline_markup.add(
        types.InlineKeyboardButton(text="QR Code", callback_data="callbackbnb_qrcode")
)
myqrcodeinline_markup.add(
        types.InlineKeyboardButton(text="🔤 Address", callback_data="callbackbnb_addr"),
        types.InlineKeyboardButton(text="💰 Balance", callback_data="callbackbnb_bal"),
        types.InlineKeyboardButton(text="🔑 Private Key", callback_data="callbackbnb_pk")
)

async def getbalance(addr, chat_id):
	try:
		#print("ADDR")
		#print(addr)
		random_str1 = ''.join(random.choice(string.ascii_letters) for i in range(7))
		random_str2 = ''.join(random.choice(string.ascii_letters) for i in range(14))
		random_str3 = ''.join(random.choice(string.digits) for i  in range(3))
		random_str4 = ''.join(random.choice(string.ascii_letters) for i in range(3))
		print(">>>>")
		random_str = random_str1+"-"+random_str2+str(random_str3)+random_str4
		#print(random_str)
		url = "https://api-testnet.bscscan.com/api"
		querystring = {"module":"account","action":"balance","address":str(addr),"tag":"latest"}
		payload = ""
		headers = {'cache-control': "no-cache",'Postman-Token': str(random_str)}
		#print(">>>>>>#######<<<<<")
		response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
		print("############")
		print(response.text)
		balanc = json.loads(response.text)
		if balanc["result"]:
			mybalanc = "<b>Balance: (BNB) </b>"+str(int(balanc["result"])/1000000000000000000)
			bot.send_message(chat_id=chat_id, text=mybalanc, parse_mode='HTML')
			return
		else:
			bot.send_message(chat_id=chat_id, text="0", parse_mode='HTML')
			return
			#print(">>>><<<<<>>>><<<<>>>><<<<>>>>")
			####return response
	except Exception as e:
		print(e)

def mydef(coroutine):
	try:
		coroutine.send(None)
	except StopIteration as e:
		return e.value


@bot.message_handler(regexp="HELP")
def handle_message(message):
	bot.reply_to(message, "HELP HERE")


##### TIP user function
def tipuser(cur, touser, amt, senderAddress, senderKey):
	#print(cur)
	#print(touser)
	#print(amt)	
	### moved from here
	T = Tipper(senderAddress, senderKey, touser, cur, amt)


##### TIP User
@bot.message_handler(regexp="/tip")
def handle_message(message):		
	print(message.from_user.id)
	tip_text = message.text.split()
	cur = message.text.split()[2]
	tousertxt = message.text.split()[1]
	touser = tousertxt.split("@")[1]
	amt = message.text.split()[3]
	#print("###################################")
	#print(len(tousertxt))
	findtelegram = { "username": touser }
	mydocumenta = mycol.find(findtelegram)
	if mydocumenta.count() > 0:
		for item in mydocumenta:			
			transfertowallet = item["address"]
			if cur in tipcurrency:
				senderdetails = mycol.find({"telegram_id": message.from_user.id})
				if senderdetails.count() > 0:
					for myitem in senderdetails:
						senderAddress = myitem["address"]
						senderKey = myitem["privateKey"]
						tipuser(cur, transfertowallet, amt, senderAddress, senderKey)
					return
			else:
				bot.reply_to(message,'Sorry! We don\'t understand this currency')
		return

	#print("###################################")	
	#bot.reply_to(message, amt)	

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
	bot.send_message(chat_id=message.chat.id, text=wallet_text, reply_markup=myinline_markup)


###### CALL BACK QUERY HANDLER 
@bot.callback_query_handler(func=lambda call: True)
def callbackbnb_addr(call):
	#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	p = call.message.json
	chat_id = p["chat"]["id"]
	#print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	d = str(call.data)
	print(d)
	if d == "callbackbnb_addr":
		###########################
		ENTROPY = generate_entropy(strength=128)
		randomstr1 = ''.join(random.choice(string.digits) for i  in range(2))
		randomstr2 = ''.join(random.choice(string.ascii_letters) for i in range(10))
		randomstr4 = ''.join(random.choice(string.ascii_letters) for i in range(8))
		randomstr3 = ''.join(random.choice(string.digits) for i in range(1))
		PASSPHRASE = str(randomstr1)+str(randomstr2)+'@$'+str(randomstr4)+str(randomstr3)
		#PASSPHRASE = str("5oM3P@ssw0rdqwertasdfzxcv")
		#PASSPHRASE = str(pass_phrase)
		# Choose language english, french, italian, spanish, chinese_simplified, chinese_traditional, japanese & korean
		LANGUAGE = "english"  # default is english
		wallet = Wallet()
		wallet.from_entropy(entropy=ENTROPY, passphrase=PASSPHRASE, language=LANGUAGE)
		# Derivation from path
		# wallet.from_path("m/44'/60'/0'/0/0'")
		# Or derivation from index
		wallet.from_index(44, harden=True)
		wallet.from_index(60, harden=True)
		wallet.from_index(0, harden=True)
		wallet.from_index(0)
		wallet.from_index(0, harden=True)
		w = wallet.dumps()
		# Print all wallet information's ----
		###print(json.dumps(wallet.dumps()))
		address = w["address"]
		private_key = w["private_key"]
		public_key = w["public_key"]
		passphrase = w["passphrase"]
		mnemonic = w["mnemonic"]
		########################### 		
		findtelegram = { "telegram_id": call.from_user.id }
		mydoc = mycol.find(findtelegram)
		if mydoc.count() > 0:
			for x in mydoc:
				######Send wallet  details to user
				z = ADDRESS_BTN_TEXT.format(MYADDRESS=x["address"])
				#bot.send_message(chat_id, x["address"])
				bot.send_message(chat_id=chat_id, text=z, parse_mode='MarkdownV2', reply_markup=myqrcodeinline_markup)
			return
		else:
			myjsondata = { "telegram_id": call.from_user.id, "username": call.from_user.username, "address": address, "privateKey": private_key, "mnemonic": mnemonic,"passphrase": passphrase, "walletDetails": json.dumps(w) }
			x = mycol.insert_one(myjsondata)
			z = ADDRESS_BTN_TEXT.format(MYADDRESS=str(address))
			#bot.send_message(chat_id, address)
			bot.send_message(chat_id=chat_id, text=z, parse_mode='MarkdownV2', reply_markup=myqrcodeinline_markup)
			try:
				qr = qrcode.QRCode(box_size=2)
				qr.add_data(str(address))
				qr.make()
				img = qr.make_image()
				filename = str(call.from_user.id)+".png"
				img.save(filename)
			except Exception as e:
				print(e)

	if d == "callbackbnb_bal":
		##print("In if loop")
		##print(chat_id)
		#getbalance.send(None)
		findmyaddr = { "telegram_id": call.from_user.id }
		mydoc = mycol.find(findmyaddr)
		if mydoc.count() > 0:
			for y in mydoc:
				#foraddress = '0xBd32a2023C127EA99082Dd9B3044B2Bf61CFAe7E'
				#balanceurl = 'https://api-testnet.bscscan.com/api?module=account&action=balance&address=0xBd32a2023C127EA99082Dd9B3044B2Bf61CFAe7E&tag=latest'
				foraddress = y["address"]
				mydef(getbalance(foraddress,chat_id))
			return
		##print(">>><<>>><<@@@@@@>><>><<<>><<>>")

	if d == "callbackbnb_pk": 
		##print("hola")
		findtelegram = { "telegram_id": call.from_user.id }
		mydoc = mycol.find(findtelegram)
		if mydoc.count() > 0:
			for x in mydoc:
				######Send wallet Private Key details to user
				z = str("<b>privateKey:</b>"+x["privateKey"])
				bot.send_message(chat_id, z, parse_mode="HTML")
			return


	if d == "callbackbnb_qrcode":
		myqrcodeimage = str(call.from_user.id)+".png"
		try:
			photo = Image.open(myqrcodeimage)
			bot.send_photo(chat_id, photo)
		except Exception as e:
			print(e)


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
