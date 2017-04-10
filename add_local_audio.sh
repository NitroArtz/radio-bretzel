#!/bin/bash
#     -- This script is a streaming creation tunnel. Its allows you to pop a new stream on your app in a second, using your local files.
#        It MUST be run by root or an user in the "docker" group which must have writing permissions on this script's folder and its childrens.
#         Any PR is welcome :)

readonly WORK_DIR=$(pwd)
declare SOURCE_PATH
declare NAME
declare GENRE
declare DESC
declare MOUNTPOINT
declare OK=0
declare BACKUP=0
declare DOCKER_RETURN_STATUS

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
until [[ ${OK} = 1 ]]; do
  read MOUNTPOINT
  # Checking synthax by regex
  if [[ ${MOUNTPOINT} =~ ^[a-z0-9]+$ ]]; then
    # Checking if mountpoint is already taken
    if [[ -d ${WORK_DIR}/liquidsoap/${MOUNTPOINT} ]]; then
      OVERRIDE=n
      echo "[ WARN ]  This mountpoint already exists ! Do you want to override it (you'll be able to append the playlist later)? (y/n)"
      read OVERRIDE
      if [[ ${OVERRIDE} =~ ^[yn]{1}$ ]]; then
        if [[ ${OVERRIDE} == y ]]; then
          # If folder already exists, we make a backup copy. :|
          cp -r ${WORK_DIR}/liquidsoap/${MOUNTPOINT} ${WORK_DIR}/liquidsoap/${MOUNTPOINT}.bak
          BACKUP=1
          OK=1
        else echo "[ ERROR ]  Type another mountpoint name (again, only lowercase and digits)"
        fi
      else echo "[ ERROR ]  I didn't understand your choice. Retype your mountpoint to be sure ;)"
      fi
    else OK=1
    fi
  else echo "[ ERROR ]  Verify your input (only lowercase or digits)"
  fi
done
echo "[  OK  ]  Infos successfully saved. Creating the files ..."

# Now all our parameters are set and verified. We can create files and start the new container.
# We create the forlder and throw a potential "already exists" error.
mkdir ${WORK_DIR}/liquidsoap/${MOUNTPOINT} 2> /dev/null
# We create the infos.liq file
echo -e "name = \"${NAME}\"\n desc = \"${DESC}\"\n genre = \"${GENRE}\"\n mountpoint = \"${MOUNTPOINT}\"" > ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/infos.liq
# Checking ...
if [[ ! -f ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/infos.liq ]]; then
  # If file doesn't exists, we restore backup and exit
  echo "[ FATAL ]  Something Wrong happened creating the source information file. Exiting..."
  rm -rf ${WORK_DIR}/liquidsoap/${MOUNTPOINT}
  [[ BACKUP==1 ]] && rm -rf ${WORK_DIR}/liquidsoap/${MOUNTPOINT}.bak
  exit 1
else echo "[  OK  ]  File \"${WORK_DIR}/liquidsoap/${MOUNTPOINT}/infos.liq\" have been successfully created."
fi

# now we fill the playlist.m3u with all the files found in our SOURCE_PATH folder
SOURCE_LIST=$(find ${SOURCE_PATH} -type f)
REPLACEMENT="~/audio/"
# Asking to override or append
if [[ -f ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u ]]; then
  APPEND=o
  echo "[ WARN ]  The file ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u already exists. Do you want to append it or override it ? Type 'a' to append, selse to override"
  read APPEND
  if [[ APPEND == a ]]; then
    echo -e "\n${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" >> ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u
  else echo -e "#EXTM3U ${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u
  fi
  else echo -e "#EXTM3U ${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u
fi
# Checking ...
if [[ ! -f ${WORK_DIR}/liquidsoap/${MOUNTPOINT}/playlist.m3u ]]; then
  echo "[ FATAL ]  Something Wrong happened creating the playlist file."
  # Checking for backup file
  rm -rf ${WORK_DIR}/liquidsoap/${MOUNTPOINT}
  if [[ BACKUP == 1 ]];then
     echo "[ WARN ]  Restoring infos and playlist backups..."
     mv ${WORK_DIR}/liquidsoap/${MOUNTPOINT}.bak ${WORK_DIR}/liquidsoap/${MOUNTPOINT}
     echo "[  OK  ]  Backup successfully restored."
   fi
  echo "Exiting ..."
  exit 1

  else echo "[  OK  ]  Playlist file is ready."
fi
# Everything seems to be ok, now let's run the container !
echo "[  OK  ]  Mountpoint successfully created. Starting container ..."

# The big Docker Command :| Using "Pool" as value.
docker_output=$(docker run -v $(pwd)/liquidsoap/${MOUNTPOINT}/:/home/liquy/var/ \
  -v ${SOURCE_PATH}:/home/liquy/audio/ \
  -h source-${MOUNTPOINT}.bretzel \
  --name radiobretzel_source-${MOUNTPOINT}_1 \
  --network radiobretzel_main \
  --network-alias source-${MOUNTPOINT}.bretzel \
  -d source-bretzel)

# Checking container is running
DOCKER_RETURN_STATUS=$?
# If not, throw error and exit script
if [[ DOCKER_RETURN_STATUS == 0 ]]; then
  echo "[ FATAL ]  Container creation failed. docker return status : ${DOCKER_RETURN_STATUS}. Error output :"
  echo -e ${docker_output}
  echo "Aborting ..."
  # Checking for backup files ...
  if [[ BACKUP == 1 ]]; then
     rm -rf ${WORK_DIR}/liquidsoap/${MOUNTPOINT}
     echo "[ WARN ]  Restoring infos and playlist backups..."
     mv ${WORK_DIR}/liquidsoap/${MOUNTPOINT}.bak ${WORK_DIR}/liquidsoap/${MOUNTPOINT}
     echo "[  OK  ]  Backup successfully restored."
   fi
  echo "Exiting ..."
  exit 1
else
  echo "[  OK  ]  Your new stream is up !! Here's your source container id : ${docker_output}"
  echo "    Thank you, come again ! =|"
  exit 0
fi
