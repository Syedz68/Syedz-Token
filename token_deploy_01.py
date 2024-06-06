import json
from web3 import Web3
from solcx import install_solc, compile_standard

# Install the specific Solidity compiler version
install_solc('0.8.0')

with open("./ERC_20.sol", "r") as file:
    ierc20_source = file.read()

with open("./SyedzToken.sol", "r") as file:
    mytoken_source = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "ERC_20.sol": {"content": ierc20_source},
            "SyedzToken.sol": {"content": mytoken_source},
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0"
)

with open("compiled_code_token.json", "w") as file:
    json.dump(compiled_sol, file)

# Extract the bytecode and ABI
bytecode = compiled_sol["contracts"]["SyedzToken.sol"]["SyedzToken"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["SyedzToken.sol"]["SyedzToken"]["abi"]

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337

# These addresses are the accounts of the local Blockchain Ganache
myAddress = ["0x56F04Bf3C27377B60514ABF29e14243d630EBE56", "0x3DF3A021524c828254aAd79CB8F8Aa0B9F144788",
             "0x16de9fB16EeF6d91026667AD20cd24d0E81Fac3F", "0xE7DCA184bf225751F13f7CAb2Ae48901cD14885E"]

# These are the private keys of the accounts in myAddress
privateKey = ["0x9368e11d407bd1eb851e6c560180218afbbcb7b5d530c4e7464ae93ab9e36eb1",
              "0x318c559e7ae42f6e6ffd59c762e2b00e45fb68af19b7fbcac041f4a8d45d9539",
              "0xe243e37a62d127840dbd0ac2e0ae8b22f48866f9896834cc8907ec1d9e820394",
              "0x7ca1158fe9c2621b66b9e4b388191dbe17b86cc1844c4925fe7cd5f5891ec598"]

# Print bytecode and ABI
print("Bytecode: ", bytecode)
print("ABI: ", abi)