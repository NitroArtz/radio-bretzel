import os
import re
from random import randint

def create(docker, name):
   return docker.containers.run(
      image='radiobretzel/source:dev',
      command='./test.liq',
      name=name,
      ports={
         '8080/tcp': 3000
      }
   )

def select_next_track():
   random_song = randint(1, 3)
   return "/audio/test%s.mp3" % random_song

def validate_source_data(sourceData):
   if re.match('((?:[a-z][a-z]+))(-)((?:[a-z][a-z]+))', sourceData['id']):
      if sourceData['active'] == 'False' or sourceData['active'] == 'True':
         if (re.match('((?:[a-z][a-z]*[0-9]*[a-z0-9]*))(-?)((?:[a-z][a-z]*[0-9]*[a-z0-9]*)?)(-?)((?:[a-z][a-z]*[0-9]*[a-z0-9]*)?)', sourceData['name']) and len(sourceData['name']) > 64): #slug
            if (re.match('regex', sourceData['description'])):
               return True
   return False

def create_valid_source_data(sourceData):
    # This code doesn't work yet

   # if not re.match('((?:[a-z][a-z]+))(-)((?:[a-z][a-z]+))', sourceData['id']):
   #    #should be generated
   #    id = "jean-patate"
   # if not sourceData['active'] == 'False' and sourceData['active'] != 'True':
   #
   # if not re.match('((?:[a-z][a-z]*[0-9]*[a-z0-9]*))(-?)((?:[a-z][a-z]*[0-9]*[a-z0-9]*)?)(-?)((?:[a-z][a-z]*[0-9]*[a-z0-9]*)?)', sourceData['name']) and len(sourceData['name']) > 64: #slug
   #    sourceData['name']='L4T34M-d3s-p4t4t3s'
   # if not re.match('regex', sourceData['description']):
   #    sourceData['description']=''
   return sourceData

class SourceModel:

   def __init__(self, sourceData):
      self.id = sourceData['id']
      self.active = True if sourceData['active'] == "True" else False
      self.name = sourceData['name']
      self.description = sourceData['description']
