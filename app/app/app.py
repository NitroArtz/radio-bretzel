from flask import Flask
from api import app

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Welcome to Radio Bretzel'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
