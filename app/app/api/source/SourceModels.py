import os

def create():
   source = docker_client.containers.run(
      image='radiobretzel/source:dev',
      command='test.liq',
      detached=True,
      volumes={
         '/home/papy/Work Space/Lab/radio-bretzel/_data/audio/ok':{
            bind: '/audio'
            mode: 'ro'
         },
         '/home/papy/Work Space/Lab/radio-bretzel/source/scripts':{
            bind: '/scripts',
            mode: 'ro'
         }
      },
      ports={
         '8080/tcp':3000
      }
   )

   return {
      'id': source.id,
      'status': source.status
   }

def select_next_track():
    int random_song = random.randint(1, 3)
    return "/audio/test%s.mp3" % random_song
