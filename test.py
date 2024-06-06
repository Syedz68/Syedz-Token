from token_deploy_02 import deploy_token, get_balance, transfer
from token_deploy_01 import abi, bytecode, chain_id, myAddress, privateKey, w3

deploy_token(50)
transfer(myAddress[0], privateKey[0], myAddress[1], 10)