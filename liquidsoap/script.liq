#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

# Loading config from environment
icecastHost = getenv("ICECAST_HOST")
icecastPort = getenv("ICECAST_PORT")
sourcePasswd = getenv("ICECAST_SOURCE_PASSWD")
icecastMountpoint = getenv("ICECAST_MOUNTPOINT")
serverURL = getenv("ICECAST_URL")

name = getenv("SOURCE_NAME")
desc = getenv("SOURCE_DESC")
genre = getenv("SOURCE_GENRE")
playlistUrl=string.concat(["~/conf/",icecastHost,"/",icecastMountpoint,"/playlist.m3u"])

#Playlist Handler
pl=playlist(reload=1, reload_mode="rounds", mode="normal", playlistUrl)
security=single("~/fail.mp3")
radio=fallback([pl, security])

#Streaaaamin out !
output.icecast(%mp3,
host = icecastHost,
port = int_of_string(icecastPort),
name = name,
description = desc,
genre = genre,
url = serverURL,
password = sourcePasswd,
mount = icecastMountpoint,
radio)
