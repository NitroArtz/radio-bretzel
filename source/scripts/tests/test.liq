#!/usr/bin/liquidsoap

#log dir
set("log.file",false)
set("log.stdout", true)

host = getenv('STREAM_HOST')
mountpoint = getenv('STREAM_MOUNTPOINT')
password = getenv('STREAM_SOURCE_PASSWD')

myPlaylist = playlist("/audio-test/")
security = single("/fail.mp3")

radio = fallback(track_sensitive = false, [myPlaylist, security])

output.icecast(%mp3,
   host=host,
   port=8000,
   password=password,
   mount=mountpoint,
   radio)
