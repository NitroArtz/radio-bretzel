#!/bin/bash

declare SOURCE_PATH
declare NAME
declare GENRE
declare DESC
declare MOUNTPOINT
declare OK=false
declare BACKUP=false

echo "  -- Welcome to this (very) simple script. It'll allow you to make one of your local folder a streaming source named \"pool\"  --"
echo "  First, paste here the path of the folder music you want to use as streaming source. (absolute path recommanded)"

# Setting the Music folder path
until [[ -d ${SOURCE_PATH} ]] ; do
  read SOURCE_PATH
  # we verify the folder exists
  [[ -d ${SOURCE_PATH} ]] && echo "[  OK  ]  Your folder has been successfully registered." || echo "[ ERROR ]  Please, verify you input."
done
# adding a "/" if not already present
[[ ${SOURCE_PATH: -1} == / ]] || SOURCE_PATH="${SOURCE_PATH}/"

# Adding stream informations
echo "      Now, we'll ask you a little more informations on the stream you want to create :)"
# Asking for Stream Name.
echo "      Starting with your stream's name : (if blank, default name is \"default-local\")"
read NAME
[[ -n ${NAME} ]] && echo "[  OK  ]  Name registered." || NAME="default-local"
# Asking for Description.
echo "      Now, add an optionnal description :"
read DESC
[[ -n ${DESC} ]] && echo "[  OK  ]  Description registered." || DESC="No description"
# Asking for Genre.
echo "      Now, add an optionnal genre :"
read GENRE
[[ -n ${GENRE} ]] && echo "[  OK  ]  Genre registered." || GENRE="Undefined"

# Now we choose a mountpoint for Icecast. This will also be the name of the folder containing the new source container configuration.
echo "      Finally, you have to choose a mountpoint for Icecast Server. It must be unique on the Icecast Server, and only contain letters (lowercase) or digits."
while [[ ${OK} = true ]]; do
  read MOUNTPOINT
  # Checking synthax by regex
  if [[ ${MOUNTPOINT} =~ ^[a-z0-9]+$ ]]; then
    # Checking if mountpoint is already taken
    if [[ -d ./liquidsoap/${MOUNTPOINT} ]]; then
      OVERRIDE=n
      echo "[ WARN ]  This mountpoint already exists ! Do you want to override it (you'll be able to append the playlist later)? (y/n)"
      read OVERRIDE
      if [[ ${OVERRIDE} =~ ^[yn]{1}$ ]]; then
        if [[ ${OVERRIDE} == y ]]; then
          # If folder already exists, we make a backup copy. :|
          cp -r ./liquidsoap/${MOUNTPOINT} ./liquidsoap/${MOUNTPOINT}.bak
          BACKUP=true
          OK=true
        else echo "[ ERROR ]  Type another mountpoint name (again, only lowercase and digits)"
        fi
      else echo "[ ERROR ]  I didn't understand your choice. Retype your mountpoint to be sure ;)"
      fi
    else OK=true
    fi
  else echo "[ ERROR ]  Verify your input (only lowercase or digits)"
  fi
done
echo "[  OK  ]  Infos successfully saved. Creating the files ..."

# Now all our parameters are set and verified. We can create files and start the new container.
# We create the forlder and throw a potential "already exists" error.
mkdir ./liquidsoap/${MOUNTPOINT} 2> /dev/null
# We create the infos.liq file
echo "name = '${NAME}'
desc = '${DESC}'
genre = '${GENRE}'
mountpoint = '${MOUNTPOINT}'" > ./liquidsoap/${MOUNTPOINT}/infos.liq
# Checking ...
if [[ -f ./liquidsoap/${MOUNTPOINT}/infos.liq ]]; then
  echo "[ FATAL ]  Something Wrong happened creating the source information file. Exiting..."
  [[ BACKUP == true ]] && rm -rf ./liquidsoap/${MOUNTPOINT}
  exit 1
else echo "[  OK  ]  File \"./liquidsoap/${MOUNTPOINT}/infos.liq\" have been successfully created."
fi

# now we fill the playlist.m3u with all the files found in our SOURCE_PATH folder
SOURCE_LIST=$(find ${SOURCE_PATH} -type f)
REPLACEMENT="~/audio/"
# Asking to override or append
if [[ -f ./liquidsoap/${MOUNTPOINT}/playlist.m3u ]]; then
  APPEND=o
  echo "[ WARN ]  The file ./liquidsoap/${MOUNTPOINT}/playlist.m3u already exists. Do you want to append it or override it ? Type 'a' to append, selse to override"
  read APPEND
  if [[ APPEND == a ]]; then
    echo -e "\n${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" >> ./liquidsoap/${MOUNTPOINT}/playlist.m3u
  else echo -e "#EXTM3U ${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > ./liquidsoap/${MOUNTPOINT}/playlist.m3u
  fi
  else echo -e "#EXTM3U ${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > ./liquidsoap/${MOUNTPOINT}/playlist.m3u
fi
# Checking ...
if [[ -f ./liquidsoap/${MOUNTPOINT}/playlist.m3u ]]; then
  echo "[ FATAL ]  Something Wrong happened creating the playlist file. Exiting..."
  [[ BACKUP == true ]] && rm -rf ./liquidsoap/${MOUNTPOINT}
  exit 1
else echo "[  OK  ]  Playlist file is ready."

# Everything seems to be ok, now let's run the container !
echo "[  OK  ]  Mountpoint successfully created. Starting container ..."

# The big Docker Command :| Using "Pool as value."
# docker run -v '/home/papy/Work\ Space/Lab/radio-bretzel/liquidsoap/pool:/home/liquy/var' \
#   -v '/home/papy/Musique/Music/Pendulum:/home/liquy/' \
#   -h 'source-pool.bretzel' \
#   --name 'radiobretzel_source-pool_1' \
#   --network 'radiobretzel_main' \
#   --network-alias 'source-pool.bretzel' \
#   source-bretzel

                # "container_linux.go:247: starting container process caused "exec: \"./script.liq\": stat ./script.liq: no such file or directory"
                # docker: Error response from daemon: oci runtime error: container_linux.go:247: starting container process caused "exec: \"./script.liq\": stat ./script.liq: no such file or directory".
                # ERRO[0001] error getting events from daemon: net/http: request canceled "
                
exit 0
