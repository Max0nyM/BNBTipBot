from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider)
from eth_account import Account

try:
	nonceNum = 4
	senderKey = 'ad7e51ec3cbaae06e892698a7d09703e8c83676d07c237068d09b3ed37da1fe9'
	val = 1*1000000000000000000
	to = '0x1c28C63FF68D88cE245fCbf98d8ccE20C0620a71'
	gas = 2000000
	gasPrice = 23456789765
	web3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
	#print(web3.eth.getBalance('0x8f1ABf8AF352C1A7aa55EB5fF3C56def94FEb849'))
	tx = w3.eth.account.sign_transaction({'gasPrice':gasPrice,'gas':gas,'nonce':nonceNum,'to':to,'value':val},
senderKey)
	web3.eth.sendRawTransaction(tx.rawTransaction)
except Exception as exp:
	print(exp)
