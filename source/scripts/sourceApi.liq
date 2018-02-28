#!/usr/bin/liquidsoap
%include "includes/defaults.liq"

apihost = getenv("API_HOST")
apiport = getenv("API_PORT")

id = getenv("SOURCE_ID")
key = getenv("SOURCE_TOKEN")

url = string.concat(['http://', apihost, ':', apiport, '/channel/next'])

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

source = request.dynamic(createSource)

%include "includes/createStream.liq"

%include "includes/outputStream.liq"
