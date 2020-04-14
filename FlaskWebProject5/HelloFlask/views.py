from datetime import datetime
from flask import render_template, jsonify
from HelloFlask import app
import json
from uuid import uuid4
from HelloFlask.models import BlockChain

# Instantiate the Blockchain
blockchain = BlockChain()

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

@app.route('/')
@app.route('/home')
def home():
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    return render_template(
        "index.html",
        title = "Hello Flask",
        message = "Hello, Flask!",
        content = " on " + formatted_now)

@app.route('/api/data')
def get_data():
  return app.send_static_file('data.json')

@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
        )

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        }
    return render_template(
        "BlockChain.html",
        title = "Block Chain - Mine",
        content = response)


@app.route('/transactions/new', methods=['POST'])  #<-- Change to POST
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
         return 'Missing values', 400
    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to Block {index}'}

    return render_template(
        "BlockChain.html",
        title = "Block Chain - New Transaction",
        content = reposnse,
#        content = jsonify(reposnse),
        )

@app.route('/chain', methods=['GET'])
def full_chain():
    print({
            'chain': blockchain.chain,
            'length': len(blockchain.chain)
            }
          )
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
        }
    return render_template(
        "BlockChain.html",
        title = "Block Chain - The Chain",
        content = response,
#        content = jsonify(response)
        )

@app.route('/about')
def about():
    return render_template(
        "about.html",
        title = "About HelloFlask",
        content = "Example app page for Flask.")

@app.route('/BlockChain')
def BlockChain():
    return render_template(
        "BlockChain.html",
        title = "BlockChain HelloFlask",
        content = "Example BlockChain app page for Flask.")