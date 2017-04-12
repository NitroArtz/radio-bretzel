#!/bin/bash
#     -- This script is a streaming creation tunnel. Its allows you to pop a new stream on your app in a second, using your local files.
#        It MUST be run by root (for now) and from the radiobretzel directory
#
#       To Do :
#         - Handle every variable through argument.
#         - add a usage() function binded to -h
#         - escape characters at input ()
# Any PR is welcome :)

if [[ $EUID != 0 ]]; then
   echo "[ !ERR ]  This script must be run as root and from this script's directory." 1>&2
   exit 1
fi



readonly WORK_DIR=$(pwd)                                      # Working Directory Path.
declare INSTANCE_ID="1"                                       # This one will be dynamically handled later. Notify the quotes
declare SOURCE_PATH                                           # Contains the path of the music directory given as source
declare MOUNTPOINT                                            # Icecast mountpoint
declare MOUNTPOINT_PATH                                       # Full path of the config file created for the new mountpoint
declare NAME                                                  # Stream name (infos.liq)
declare GENRE                                                 # Stream genre (infos.liq)
declare DESC                                                  # Stream description (infos.liq)
declare AUTH_URL="http://frontend.bretzel:8082/auth/check"    # Contains the URL of the backend server which handle user authentication.
declare BACKUP=0                                              # If this variable is set to 1, we create a backup file (user might override a mountpoint)


echo "  -- Welcome to this (very) simple script. It'll allow you to make one of your local directory a streaming source named \"pool\"  --"
echo "First, paste here the path of the music directory you want to use as streaming source. (absolute path is needed)"

# Setting the Music directory path
#  --> Might be handled by an argument to the script (later)
until [[ -d ${SOURCE_PATH} ]] ; do
  read SOURCE_PATH
  # HERE WE NEED TO ESCAPE POTENTIAL CHARACTERS (following were tested and error showed up):
  #   - "
  #   - $
  #   - \

  # we verify the directory exists
  [[ -d ${SOURCE_PATH} ]] && echo "[  OK  ]  Your directory has been successfully registered." || echo "[ !ERR ]  Please, verify you input."
done
# adding a "/" if not already present
[[ ${SOURCE_PATH: -1} == / ]] || SOURCE_PATH="${SOURCE_PATH}/"

# Here we choose a mountpoint for Icecast. This will also be the name of the directory containing the new source container configuration.
echo "First of all, you have to choose a mountpoint for Icecast Server. It must be unique on the Icecast Server, and only contain letters (lowercase) or digits."
OK=0
until [[ ${OK} = 1 ]]; do
  read MOUNTPOINT
  # Simplifying reading
  MOUNTPOINT_PATH="${WORK_DIR}/liquidsoap/${MOUNTPOINT}"
  # Checking synthax by regex
  if [[ "${MOUNTPOINT}" =~ ^[a-z0-9]+$ ]]; then
    # Checking if mountpoint is already taken
    if [[ -d "${MOUNTPOINT_PATH}" ]]; then
      OVERRIDE=n
      echo "[ WARN ]  This mountpoint already exists ! Do you want to override it (you'll be able to append the playlist later)? (y/n)"
      read OVERRIDE
      if [[ ${OVERRIDE} =~ ^[yn]{1}$ ]]; then
        if [[ ${OVERRIDE} == y ]]; then
          # If directory already exists, we make a backup copy. :|
          cp -r "${MOUNTPOINT_PATH}" "${MOUNTPOINT_PATH}.bak"
          BACKUP=1
          OK=1
        else echo "Type another mountpoint name (again, only lowercase and digits)"
        fi
      else echo "[ !ERR ]  I didn't understand your choice. Retype your mountpoint to be sure ;)"
      fi
    else OK=1
    fi
  else echo "[ !ERR ]  Verify your input (only lowercase or digits)"
  fi
done

# Adding stream informations
# Wanna erase conf file or keep the same ?
INFOS=1
if [[ ${BACKUP} == 1 ]]; then
  OK=0
  until [[ ${OK} == 1 ]]; do
    OVERRIDE=n
    echo "[ WARN ]  As this mountpoint already exists, its configuration file too. Do you want to override it ?"
    read OVERRIDE
    if [[ ${OVERRIDE} =~ ^[yn]{1}$ ]]; then
      # Don't ask about settings if answered "no"
      [[ ${OVERRIDE} == y ]] && OK=1 || INFOS=0 && OK=1
    else echo "[ !ERR ]  I didn't understand your choice (y or n ?))"
    fi
  done
fi
# Printing information form if needed
if [[ ${INFOS} == 1 ]]; then
  echo "[  OK  ]  Now, we'll ask you a little more informations on the stream you want to create :)"
  # Asking for Stream Name.
  echo "Starting with your stream's name : (if blank, default name is \"default-local\")"
  read NAME
  [[ -n "${NAME}" ]] && echo "[  OK  ]  Name registered." || NAME="default-local"
  # Asking for Description.
  echo "Now, add an optionnal description :"
  read DESC
  [[ -n "${DESC}" ]] && echo "[  OK  ]  Description registered." || DESC="No description"
  # Asking for Genre.
  echo "Now, add an optionnal genre :"
  read GENRE
  [[ -n "${GENRE}" ]] && echo "[  OK  ]  Genre registered." || GENRE="Undefined"
  echo "[  OK  ]  Infos successfully collected."
fi
# Now all our parameters are set and verified. We can create files.
# We create the forlder and exit if it fails.
if [[ ${BACKUP} == 0 ]]; then
  mkdir "${MOUNTPOINT_PATH}" 2> /dev/null
  [[ $? != 0 ]] && echo "[ FATAL ]  Something wrong happened during the mountpoint directory creation. Exiting ..." && exit 1
fi
# We create the infos.liq file
echo -e "name = \"${NAME}\"\n desc = \"${DESC}\"\n genre = \"${GENRE}\"\n mountpoint = \"${MOUNTPOINT}\"" > "${MOUNTPOINT_PATH}/infos.liq"
# Checking ...
if [[ ! -f "${MOUNTPOINT_PATH}/infos.liq" ]]; then
  # If file doesn't exists, we restore backup and exit
  echo "[ FATAL ]  Something Wrong happened creating the source information file. Exiting..."
  rm -rf "${MOUNTPOINT_PATH}"
  [[ ${BACKUP} == 1 ]] && rm -rf "${MOUNTPOINT_PATH}.bak"
  exit 1
else echo "[  OK  ]  File \"${MOUNTPOINT_PATH}/infos.liq\" have been successfully created."
fi

# now we fill the playlist.m3u with all the files found in our SOURCE_PATH directory
SOURCE_LIST=$(find "${SOURCE_PATH}" -type f)
REPLACEMENT="~/audio/"
# Asking to override or append
if [[ -f "${MOUNTPOINT_PATH}/playlist.m3u" ]]; then
  APPEND=o
  echo "[ WARN ]  The file ${MOUNTPOINT_PATH}/playlist.m3u already exists. Do you want to append it or override it ? Type 'a' to append, else to override"
  read APPEND
  if [[ ${APPEND} == a ]]; then
    echo -e "\n${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" >> "${MOUNTPOINT_PATH}/playlist.m3u"
  else echo -e "#EXTM3U \n${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > "${MOUNTPOINT_PATH}/playlist.m3u"
  fi
else echo -e "#EXTM3U \n${SOURCE_LIST//${SOURCE_PATH}/${REPLACEMENT}}" > "${MOUNTPOINT_PATH}/playlist.m3u"
fi
# Checking file ...
if [[ ! -f "${MOUNTPOINT_PATH}/playlist.m3u" ]]; then
  echo "[ FATAL ]  Something Wrong happened creating the playlist file."
  # Checking for backup file
  rm -rf "${MOUNTPOINT_PATH}"
  if [[ ${BACKUP} == 1 ]];then
     echo "[ WARN ]  Restoring infos and playlist backups..."
     mv "${MOUNTPOINT_PATH}.bak" "${MOUNTPOINT_PATH}"
     echo "[  OK  ]  Backup successfully restored."
   fi
  echo "Exiting ..."
  exit 1

  else echo "[  OK  ]  Playlist file is ready."
fi

# --------------- INSERT HERE ICECAST CONFIGURATION TREATMENT ---------
# As  explicited above, we must add a little piece of code in our radiobretzel/icecast/icecast.xml file.
# in order to be sure our new stream listenners are authenticated  to the app
# to connect to the icecast server.
# might look like this :
# <mount>
#   <mount-name>/${MOUNTPOINT}</mount-name>
#   <authentication type="url">
#     <option name="listener_add" value="${AUTH_URL}"/>
#     <option name="auth_header" value="icecast-auth-test: 1"/>
#   </authentication>
# </mount>

# Don't forget to reload the icecast server configuration :
# docker container restart "radiobretzel_icecast_${INSTANCE_ID}"


# If the mountpoint already exists, we must stop its container.
if [[ ${BACKUP} == 1 ]]; then
  OK=0
  until [[ ${OK} == 1 ]]; do
    STOP=n
    echo "[ WARN ]  In Order to create new stream, the old one must be stopped. Continue ? (y/n)"
    read STOP
    if [[ ${STOP} =~ ^[yn]{1}$ ]]; then
      # Don't ask about settings if answered "no"
      if [[ ${STOP} == y ]]; then
        docker container rm -f "radiobretzel_source-${MOUNTPOINT}_${INSTANCE_ID}"
        if [[ $? != 0 ]]; then
          echo "[ FATAL ]  Container radiobretzel_source-${MOUNTPOINT}_${INSTANCE_ID} was too powerful and couldn't be stopped.. He did conquire the entire world and galaxy, and now, we all live under his reign of suffering and despair ... Exiting ..."
          rm -rf "${MOUNTPOINT_PATH}.bak"
          exit 1
        else
          sed "/radiobretzel_source-${MOUNTPOINT}_${INSTANCE_ID}/d" ./system/${INSTANCE_ID}/source_ct_list > /dev/null 2>&1
          OK=1
        fi
      else
        echo "[ FATAL ]  You refused to stop previous named '${MOUNTPOINT}' mountpoint. Exiting ..."
        rm -rf "${MOUNTPOINT_PATH}.bak"
        exit 1
      fi
    else echo "[ !ERR ]  I didn't understand your choice (y or n ?))"
    fi
  done
fi
# Everything seems to be ok, now let's run the container !
echo "[  OK  ]  Mountpoint successfully created ! Starting container ..."

# The big Docker Command :| Using "Pool" as value.
docker_output=$(docker run -v "${MOUNTPOINT_PATH}/:/home/liquy/var/" \
  -v "${SOURCE_PATH}:/home/liquy/audio/" \
  -h "source-${MOUNTPOINT}.bretzel" \
  --name "radiobretzel_source-${MOUNTPOINT}_${INSTANCE_ID}" \
  --network radiobretzel_main \
  --network-alias "source-${MOUNTPOINT}.bretzel" \
  -d source-bretzel)

# Checking container is running
# If not, throw error and exit script
if [[ $? != 0 ]]; then
  echo "[ FATAL ]  Container creation failed. docker return status : ${DOCKER_RETURN_STATUS}. Error output :"
  echo -e ${docker_output}
  echo "Aborting ..."
  # Checking for backup files ...
  if [[ ${BACKUP} == 1 ]]; then
     rm -rf "${MOUNTPOINT_PATH}"
     echo "[ WARN ]  Restoring infos and playlist backups..."
     mv "${MOUNTPOINT_PATH}.bak" "${MOUNTPOINT_PATH}"
     echo "[  OK  ]  Backup successfully restored."
   fi
  echo "Exiting ..."
  exit 1
else
  echo "[  OK  ]  Your new stream is up !! Here's your source container id : ${docker_output}"
  mkdir -p ./system/${INSTANCE_ID}/ 2> /dev/null
  if [[ ${BACKUP} == 1 ]]; then
    rm -rf "${MOUNTPOINT_PATH}.bak"
    echo "Removing backup files ...";
  # Adding the container to the list file if not already present
  else echo -e "radiobretzel_source-${MOUNTPOINT}_${INSTANCE_ID}\n" >> ./system/${INSTANCE_ID}/source_ct_list
  fi
  echo "Thank you, come again ! =|"
  exit 0
fi
