from token_deploy_01 import abi, bytecode, chain_id, myAddress, privateKey, w3

tx_receipt = None
nonce = None
token = None
contract_address = None
flag = True


def deploy_token(initial_supply, address):
    Token = w3.eth.contract(abi=abi, bytecode=bytecode)
    global nonce
    nonce = w3.eth.get_transaction_count(address)
    transaction = Token.constructor(initial_supply).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": address,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(transaction, private_key=privateKey[0])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    global tx_receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    global contract_address
    contract_address = tx_receipt.contractAddress
    global flag
    flag = False


def total_supply():
    try:
        token_contract = w3.eth.contract(address=contract_address, abi=abi)
        return token_contract.functions.totalSupply().call()
    except Exception as e:
        print(f"Error fetching total supply: {e}")
        return None


def get_balance(address):
    try:
        token_contract = w3.eth.contract(address=contract_address, abi=abi)
        balance = token_contract.functions.balanceOf(address).call()
        return balance
    except Exception as e:
        print(f"Error fetching balance for address {address}: {e}")
        return None


def get_allowance(owner, spender):
    token_contract = w3.eth.contract(address=contract_address, abi=abi)
    return token_contract.functions.allowance(owner, spender).call()


def make_transfer(sender, key, recipient, amount):
    global tx_receipt
    global contract_address
    global nonce
    nonce = w3.eth.get_transaction_count(sender)
    Token = w3.eth.contract(address=contract_address, abi=abi)
    create_transaction = Token.functions.transfer(recipient, amount).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": sender,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(create_transaction, private_key=key)
    tx_signed_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(tx_signed_hash)


def approve_user(sender, key, spender, amount):
    global tx_receipt
    global contract_address
    global nonce
    nonce = w3.eth.get_transaction_count(sender)
    Token = w3.eth.contract(address=contract_address, abi=abi)
    create_transaction = Token.functions.approve(spender, amount).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": sender,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(create_transaction, private_key=key)
    tx_signed_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(tx_signed_hash)


def transfer_from(sender, recipient, key, amount):
    global tx_receipt
    global contract_address
    global nonce
    nonce = w3.eth.get_transaction_count(recipient)
    Token = w3.eth.contract(address=contract_address, abi=abi)
    create_transaction = Token.functions.transferFrom(sender, recipient, amount).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": recipient,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(create_transaction, private_key=key)
    tx_signed_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(tx_signed_hash)


def mint_token(minter, key, amount):
    global tx_receipt
    global contract_address
    global nonce
    nonce = w3.eth.get_transaction_count(minter)
    Token = w3.eth.contract(address=contract_address, abi=abi)
    create_transaction = Token.functions.mint(amount).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": minter,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(create_transaction, private_key=key)
    tx_signed_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(tx_signed_hash)


def burn_token(burner, key, amount):
    global tx_receipt
    global contract_address
    global nonce
    nonce = w3.eth.get_transaction_count(burner)
    Token = w3.eth.contract(address=contract_address, abi=abi)
    create_transaction = Token.functions.burn(amount).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,
            "from": burner,
            "nonce": nonce,
        }
    )
    nonce += 1
    signed_tx = w3.eth.account.sign_transaction(create_transaction, private_key=key)
    tx_signed_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.get_transaction_receipt(tx_signed_hash)


def deploy(address):
    global flag
    while flag:
        deploy_token(50, address)


"""deploy_token(50)
print(f"Total Supply: {total_supply()}")
tamm = 10 * 10 ** 18
transfer(myAddress[0], privateKey[0], myAddress[1], tamm)
print(f"Balance of Owner: {get_balance(myAddress[0])}")
print(f"Balance of user A: {get_balance(myAddress[1])}")
print(f"Balance of user B: {get_balance(myAddress[2])}")
tamm = 5 * 10 ** 18
approve(myAddress[1], privateKey[1], myAddress[2], tamm)
print(f"User B is allowed to spend: {get_allowance(myAddress[1], myAddress[2])}")
tamm = 3 * 10 ** 18
transfer_from(myAddress[1], myAddress[2], privateKey[2], tamm)
print(f"Balance of Owner: {get_balance(myAddress[0])}")
print(f"Balance of user A: {get_balance(myAddress[1])}")
print(f"Balance of user B: {get_balance(myAddress[2])}")
print(f"User B is allowed to spend: {get_allowance(myAddress[1], myAddress[2])}")
tamm = 13 * 10 ** 18
mint_token(myAddress[1], privateKey[1], tamm)
print(f"Total Supply: {total_supply()}")
print(f"Balance of user A: {get_balance(myAddress[1])}")
tamm = 1 * 10 ** 18
burn_token(myAddress[2], privateKey[2], tamm)
print(f"Total Supply: {total_supply()}")
print(f"Balance of user B: {get_balance(myAddress[2])}")"""
