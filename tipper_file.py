from web3 import Web3, EthereumTesterProvider
w3 = Web3(EthereumTesterProvider)
from eth_account import Account

### Binance details
binanceSmartChainTestNet = 'https://data-seed-prebsc-2-s1.binance.org:8545/'

class Tipper:		
	def __init__(self, senderAddress, senderKey, touser, cur, amt):
		try:		
			val = int(amt) * 1000000000000000000		
			to = str(touser)				
			url = 'https://data-seed-prebsc-2-s1.binance.org:8545/'
			web3 = Web3(Web3.HTTPProvider(binanceSmartChainTestNet))
			#web3 = Web3(Web3.HTTPProvider('https://data-seed-prebsc-1-s1.binance.org:8545'))
			gasPrice = web3.eth.gasPrice
			print("Estimate Gas::::")		
			estimatedGas = web3.eth.estimateGas({"from":senderAddress,"to": touser,"data": b''})
			print(estimatedGas)
			if estimatedGas < 21000:
				estimatedGas = 21000		
			print(estimatedGas)
			
			#print(to)		
			nonce = int(web3.eth.getTransactionCount(senderAddress,'latest'))
			print(">>>>>>>>> Sending TIP >>>>>>>>>>>>")
			print(nonce)		
			tx = web3.eth.account.sign_transaction(dict(gasPrice=gasPrice,gas=estimatedGas,nonce=nonce,to=to,value=val,data=b''), senderKey)
			print(tx.rawTransaction)		
			web3.eth.sendRawTransaction(tx.rawTransaction)
		except Exception as exp:
			print(exp)
