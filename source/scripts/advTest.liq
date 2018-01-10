#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

# Loading config from environment and building API url from that
mountpoint = getenv("STREAM_MOUNTPOINT")
id = getenv("SOURCE_ID")
apihost = getenv("API_HOST")
key = getenv("SOURCE_TOKEN")
url = string.concat(['http://', apihost, '/', mountpoint,'/next'])

def getHttpStatusCode (httpResponse)
  httpStatusCode = snd(fst(fst(fst(response))))
  httpStatusCode
end

def getFilePathFromAPI (id, key)
  response = http.get(headers=[('source-id', id), ('source-key', key)], url)
  response
end

def getFileFromAPIOrHandleFail (id, key)
  getFilePathFromAPI(id, key)
  if getHttpStatusCode(response) == 200
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
output.harbor(%mp3,
  mount = mountpoint,
  radio)

