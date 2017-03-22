#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

%include "~/conf.liq"
%include "~/var/infos.liq"

#Playlist Handler
pl=playlist(reload=1, reload_mode="rounds", mode="normal", "~/var/playlist.m3u")
security=single("~/fail.mp3")
radio=fallback([pl, security])

#Streaaaamin out !
output.icecast(%mp3,
host = host,
port = port,
name = name,
description = desc,
genre = genre,
url = url,
password = src_passwd,
mount = mountpoint,
radio)
