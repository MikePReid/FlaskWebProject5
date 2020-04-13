from flask import Flask

app = Flask(__name__)

import HelloFlask.views
import HelloFlask.models

# Instantiate the Blockchain
blockchain = BlockChain()
