#!/usr/bin/liquidsoap

# Log settings
set("log.file", false)
set("log.stdout", true)

# Loading config from environment and building API url from that
mountpoint = getenv("STREAM_MOUNTPOINT")
host = getenv('STREAM_HOST')
password = getenv('STREAM_SOURCE_PASSWD')
log(mountpoint)
id = getenv("SOURCE_ID")
apihost = getenv("API_HOST")
key = getenv("SOURCE_TOKEN")
url = string.concat(['http://', apihost, ':5000/', mountpoint,'/next'])

def getHttpStatusCode (httpResponse)
   httpStatusCode = snd(fst(fst(fst(httpResponse))))
   httpStatusCode
end

def getFilePathFromAPI (id, key)
   # response = http.get(headers=[('source-id', id), ('source-key', key)], url)
   response =http.get(url)
   response
end

def getFileFromAPIOrHandleFail (id, key)
   response = getFilePathFromAPI(id, key)
   log(string.concat(["Trying to get : ", url]))
   if getHttpStatusCode(response) == 200
      then
      log(string.concat(["Success : ", string_of(response)]))
      echo=string.concat(["/audio/", snd(response)])
      echo
   else
      log("Server bad response :")
      log(string_of(response))
      "../fail.mp3"
   end
end

def createSource()
log("creating source")
   request.create(getFileFromAPIOrHandleFail(id,key))
end


security = single("/fail.mp3")
radio = fallback(track_sensitive = false, [
   request.dynamic(createSource),
   security
   ])

#Streaaaamin out !
output.icecast(%mp3,
   host=host,
   port=8000,
   password=password,
   mount=mountpoint,
   radio)
