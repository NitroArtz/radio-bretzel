#!/bin/bash

[[ $(pwd | rev | cut -d"/" -f1 | rev) != "source" ]] && "u must run this frmo source dir" && exit 1

# Contains all "ls" named containers
existing_containers=$(docker inspect $(docker ps -q ) | grep -i traefik.backend | cut -d":" -f2 | cut -d'"' -f2)

increment=2
container_prefix="ls"

possible_container_name=${container_prefix}${increment}

while [[ ${existing_containers} == *"${possible_container_name}"*  ]]
do
  echo "${possible_container_name} is already taken." 
  increment=$((${increment}+1))
  possible_container_name=${container_prefix}${increment}
done

echo "${possible_container_name} is free :o"

docker run -v $(pwd)/../_data/audio/ok:/audio -v $(pwd)/scripts:/scripts   --hostname ${possible_container_name}.traefik -l "traefik.backend=${possible_container_name}" -l "traefik.port=8080" -l "traefik.frontend.rule=Host:${possible_container_name}.traefik" --network source_radiobretzel -d radiobretzel/source:dev ./test.liq
