import os
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
