from web3 import Web3
import string

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>https://t.me/hobotilnya<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>https://t.me/hobotilnya<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>https://t.me/hobotilnya<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\n")

#подключение к ноде
RPC = "https://base-goerli.public.blastapi.io"
web3 = Web3(Web3.HTTPProvider(RPC))
print('Connect is: ' + str(web3.isConnected()) + "\n")


#переписываю приватники, bytecode, abi из файлов
private_keys = []
with open("private_keys.txt", "r") as file:
	for line in file:
		private_keys.append(line.strip())
with open("bytecode.txt", "r") as file:
	base_contract = file.read()
with open("abi.txt", "r") as file:
	abi = file.read()


#делаю транзакцию и отправляю ее
i = 0
base_contract = web3.eth.contract(bytecode = base_contract, abi = abi)

for private_key in private_keys:
	i += 1

	#обработка ошибки с неправильным приватником
	try:
		address = web3.eth.account.privateKeyToAccount(private_key).address
	except __import__('binascii').Error as err:
		print(f">>>{i} {private_key}  Ошибка в приватнике")
		continue

	nonce = web3.eth.get_transaction_count(address)
	contract_txn = {
			'chainId': 84531,
			'nonce': nonce,
			'from': address,
			'gasPrice': web3.eth.gas_price}
	contract_txn = base_contract.constructor().buildTransaction(contract_txn)
	signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key = private_key)

	#обработка ошибки с нехваткой баланса
	try:
		tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
		print(f">>>{i} {address}   tx hash:" + tx_hash.hex())
	except ValueError:
		print(f">>>{i} {address}  Не хватает eth на балансе")