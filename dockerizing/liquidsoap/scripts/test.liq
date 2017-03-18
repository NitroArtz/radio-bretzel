#!/usr/bin/liquidsoap

# Log settings
set("log.file.path","/home/liquy/test.log")
#Comment this line for prod
set("log.stdout", true)

#Icecast Param
host = "icecast.bretzel"
port = 8000
name = "Papy Bretzel Radio Project"
desc = "Radio test"
genre = "test"
url = "http://icecast.bretzel:8000/test"
passwd = "sourcepass"
mountpoint = "test"

#Playlist Handler
radio=mksafe(single("/home/liquy/audio/test/test.mp3"))

#Streaaaamin out !
output.icecast(%mp3mp3mp3,
host = host, port = port,
name = name, description = desc, genre = genre, url = url,
password = passwd,
mount = mountpoint,
radio)
