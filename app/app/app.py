from flask import Flask
import docker

from api.source import SourceModels

app = Flask(__name__)
docker_client = docker.DockerClient(
   base_url='unix://var/run/docker.sock',
   version='auto'
)

@app.route('/')
def hello_world():
   return 'Welcome to Radio Bretzel'

@app.route('/new', methods=['POST'])
def new():
   
   else:
      source = SourceModels.create(docker_client, 'test_source-creation')
      return source.id

@app.route('/source', methods=['POST'])
def source():
   if request.method == 'POST':
      source_data = SourceModels.create_valid_source_data(request.args['id'], 
                               request.args['active'], 
                               request.args['name'], 
                               request.args['container'], 
                               request.args['description'])
      source = SourceModels.create_source(source_date)
      return source.id
         

      
@app.route('/next')
def next():
   return SourceModels.select_next_track()

if __name__ == '__main__':
   app.run(debug=True,host='0.0.0.0')
