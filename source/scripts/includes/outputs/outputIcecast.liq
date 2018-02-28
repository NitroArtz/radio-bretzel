#load config from env
mountpoint = getenv("STREAM_MOUNTPOINT")
host = getenv('STREAM_HOST')
password = getenv('STREAM_SOURCE_PASSWD')

#Streaaaamin out !
output.icecast(%mp3,
   host=host,
   port=8000,
   password=password,
   mount=mountpoint,
   radio)
