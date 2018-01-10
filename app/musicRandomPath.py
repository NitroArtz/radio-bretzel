from flask import Flask
app = Flask(__name__)

@app.route("/")


def generatePathSong():
    int random_song = random.randint(1, 3)
    
    return "/audio/test{%s}.mp3" % random_song