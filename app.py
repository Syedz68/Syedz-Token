from flask import Flask, render_template, request, redirect, url_for
from token_deploy_01 import myAddress, privateKey, w3, chain_id
from token_deploy_02 import deploy, total_supply, get_balance, get_allowance, make_transfer, approve_user, \
    transfer_from, mint_token, burn_token

app = Flask('__name__')

owner = myAddress[0]
deploy(owner)


@app.route('/')
def home():
    total = total_supply()
    return render_template('index.html', total=total)


@app.route('/balance')
def balance():
    add = myAddress
    bal = 0
    return render_template('balance.html', add=add, bal=bal)


@app.route('/balanceof', methods=['POST'])
def showBalance():
    address = request.form['account']
    bal = get_balance(address)
    add = myAddress  # Assuming myAddress is defined somewhere in your code
    return render_template('balance.html', add=add, bal=bal)


@app.route('/transfer')
def transfer():
    add = myAddress
    tok = 0
    return render_template('transfer.html', add=add, tok=tok)


@app.route('/transfer_from_owner', methods=['POST'])
def transferredToken():
    add = myAddress
    address = request.form['receiver']
    amount = request.form['amount']
    amount = int(amount)
    idx = myAddress.index(owner)
    key = privateKey[idx]
    make_transfer(owner, key, address, amount)
    return render_template('transfer.html', add=add, tok=amount)


@app.route('/approve')
def approve():
    add = myAddress
    tok = 0
    user1 = None
    user2 = None
    return render_template('approve.html', add=add, tok=tok, user1=user1, user2=user2)


@app.route('/approved', methods=['POST'])
def approval():
    add = myAddress
    user1 = None
    user2 = None
    sender = request.form['sender']
    spender = request.form['receiver']
    tok = request.form['amount']
    tok = int(tok)
    idx = myAddress.index(sender)
    key = privateKey[idx]
    if sender == myAddress[1]:
        user1 = 'User A'
    elif sender == myAddress[2]:
        user1 = 'User B'
    else:
        user1 = 'User C'
    if spender == myAddress[1]:
        user2 = 'User A'
    elif spender == myAddress[2]:
        user2 = 'User B'
    else:
        user2 = 'User C'
    approve_user(sender, key, spender, tok)
    return render_template('approve.html', add=add, tok=tok, user1=user1, user2=user2)


@app.route('/allowance')
def allowance():
    add = myAddress
    tok = 0
    return render_template('allowance.html', add=add, tok=tok)


@app.route('/see_allowance', methods=['POST'])
def showAllowance():
    sender = request.form['sender']
    spender = request.form['spender']
    add = myAddress
    tok = get_allowance(sender, spender)
    return render_template('allowance.html', add=add, tok=tok)


@app.route('/transferfrom')
def transferFrom():
    add = myAddress
    tok = None
    user1 = None
    user2 = None
    return render_template('transferform.html', add=add, tok=tok, user1=user1, user2=user2)


@app.route('/transfer_from_users', methods=['POST'])
def transferFromUser():
    add = myAddress
    user1 = None
    user2 = None
    sender = request.form['sender']
    recipient = request.form['receiver']
    tok = request.form['amount']
    tok = int(tok)
    idx = myAddress.index(recipient)
    key = privateKey[idx]
    if sender == myAddress[1]:
        user1 = 'User A'
    elif sender == myAddress[2]:
        user1 = 'User B'
    else:
        user1 = 'User C'
    if recipient == myAddress[1]:
        user2 = 'User A'
    elif recipient == myAddress[2]:
        user2 = 'User B'
    else:
        user2 = 'User C'
    transfer_from(sender, recipient, key, tok)
    return render_template('transferform.html', add=add, tok=tok, user1=user1, user2=user2)


@app.route('/mint')
def mint():
    add = myAddress
    total = total_supply()
    bal = None
    return render_template('mint.html', add=add, total=total, bal=bal)


@app.route('/minting', methods=['POST'])
def mintingToken():
    add = myAddress
    minter = request.form['minter']
    tok = request.form['amount']
    tok = int(tok)
    idx = myAddress.index(minter)
    key = privateKey[idx]
    mint_token(minter, key, tok)
    total = total_supply()
    bal = get_balance(minter)
    return render_template('mint.html', add=add, total=total, bal=bal)


@app.route('/burn')
def burn():
    add = myAddress
    total = total_supply()
    bal = None
    return render_template('burn.html', add=add, total=total, bal=bal)

@app.route('/burning', methods=['POST'])
def burningToken():
    add = myAddress
    burner = request.form['burner']
    tok = request.form['amount']
    tok = int(tok)
    idx = myAddress.index(burner)
    key = privateKey[idx]
    burn_token(burner, key, tok)
    total = total_supply()
    bal = get_balance(burner)
    return render_template('burn.html', add=add, total=total, bal=bal)

if __name__ == '__main__':
    app.run(debug=True)
