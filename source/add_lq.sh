#!/bin/bash

RB_image="zgueg"
# no i'm kidding
RB_repo="radiobretzel/source"
RB_tag="dev"
RB_image="${RB_repo}:${RB_tag}"

# bitch, wrong dir
[[ $(pwd | rev | cut -d"/" -f1 | rev) != "source" ]] && echo "u must run this from source dir" && exit 1

# Contains all "ls" named containers
existing_containers=$(docker inspect $(docker ps -q ) | grep -i traefik.backend | cut -d":" -f2 | cut -d'"' -f2)

# most ugly thing in the world. 
# but still, it works
increment=2
container_prefix="ls"

# concatenate previous variables
possible_container_name=${container_prefix}${increment}

# test if name already exists. If not, increment it and loop again.
while [[ ${existing_containers} == *"${possible_container_name}"*  ]]
do
  echo "${possible_container_name} is already taken." 
  increment=$((${increment}+1))
  possible_container_name=${container_prefix}${increment}
done

# omg, loop has exited, current name is free
free_name=${possible_container_name}
echo "${free_name} is free :o"

# we found a name. Nice. very nice. Everyone is happy. Everyone is smiling. The world is beautiful. Look at the sunshine bro, look at it. So beautiful. 
docker run \
	-v $(pwd)/../_data/audio/ok:/audio \
	-v $(pwd)/scripts:/scripts   \
	--hostname ${possible_container_name}.traefik \
	-l "traefik.backend=${possible_container_name}" \
	-l "traefik.port=8080" \
	-l "traefik.frontend.rule=Host:${possible_container_name}.traefik" \
	--network source_radiobretzel \
	-d \
	${RB_image} \
	./test.liq
