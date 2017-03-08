#!/usr/bin/liquidsoap

# Log settings
set("log.file.path","/ls/test.log")
#Comment this line for prod
set("log.stdout", true)

#Icecast Param
host = "icecast.bretzel"
port = 8000
name = "Papy Bretzel Radio Project"
desc = "Radio test"
genre = "test"
url = "http://icecast.bretzel:8000/radiobretzel"
passwd = "sourcepass"
mountpoint = "test"


#Playlist Handler
radio=mksafe(single("/ls/audio/test.mp3"))

#security file 
#fail=single("/ls/audio/fail.mp3")
##Making source unfaillible
#radio=fallback(track_sensitive=false, [pl, fail])

#Streaaaamin out !
output.icecast(%vorbis,
host = host, port = port,
name = name, description = desc, genre = genre, url = url,
password = passwd,
mount = mountpoint,
radio)
