#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

# Loading config from environment
icecastHost = getenv("STREAM_HOST")
icecastPort = getenv("STREAM_PORT")
sourcePasswd = getenv("STREAM_SOURCE_PASSWD")
mountpoint = getenv("STREAM_MOUNTPOINT")
serverURL = getenv("STREAM_URL")
id = getenv("SOURCE_ID")
apihost = getenv("API_HOST")
key = getenv("SOURCE_TOKEN")
name = getenv("SOURCE_NAME")
desc = getenv("SOURCE_DESC")
genre = getenv("SOURCE_GENRE")


def filePath (id, key)
  url = string.concat(['http://', apihost, '/', mountpoint,'/next'])
  response = http.get(headers=[('source-id', id), ('source-key', key)], url)
  if snd(fst(fst(fst(response)))) == 200
    then
    echo=string.concat(['~/audio/', snd(response)])
    echo
  else
    log("Server bad response :")
    "../fail.mp3"
  end
end

def createSource()
  request.create(filePath(id,key))
end

security = single("~/fail.mp3")
radio = fallback([
  request.dynamic(createSource),
  security
  ])

#Streaaaamin out !
output.icecast(%mp3,
host = icecastHost,
port = int_of_string(icecastPort),
name = name,
description = desc,
genre = genre,
url = serverURL,
password = sourcePasswd,
mount = mountpoint,
radio)
