#!/usr/bin/liquidsoap

#log dir
set("log.file",false)
set("log.stdout", true)

myPlaylist = playlist("/audio/playlist.m3u")

security = single("/fail.mp3")

radio = fallback(track_sensitive = false, [myPlaylist, security])

output.harbor(%mp3 , port=8080, mount="music.mp3", radio)
