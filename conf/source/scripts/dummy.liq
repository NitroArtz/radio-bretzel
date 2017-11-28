#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

audio = single("/fail.mp3")

output.dummy(audio)
