import os
from HelloFlask import app    # Imports the code from HelloFlask/__init__.py

#from HelloFlask import Blockchain

# Instantiate the Blockchain
# blockchain = Blockchain()

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
