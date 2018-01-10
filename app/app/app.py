from flask import Flask
import docker

import SourceModels

app = Flask(__name__)
docker_client = docker.DockerClient(
    base_url='unix:///var/run/docker.sock',
    version='auto'
)

@app.route('/')
def hello_world():
    return 'Welcome to Radio Bretzel'

@app.route('/new')
SourceModels.create()

@app.route('/next')
SourceModels.select_next_track()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
