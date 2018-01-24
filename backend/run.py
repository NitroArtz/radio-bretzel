from app import start, config

app = start(config.Dev)

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
