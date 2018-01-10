from flask import Flask
import docker

app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Welcome to Radio Bretzel'

@app.route('/new')
def create_source():



if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
