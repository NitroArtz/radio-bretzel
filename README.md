# Radio bretzel

This project is used to setup your own private and collaborative webradio instance.  
Invite friends, chat, upload music, and listen to it !

Find more information about this project on the [Wiki](https://github.com/Clement-Ruiz/radio-bretzel/wiki) !

# Server
## Requirements
* [Docker](https://www.docker.com/ "Docker Official Website") : docker, dockerd and docker-compose v2 binaries
* Any web browser. Test feedbacks are welcome :)

Think about the storage and network resources. The needed amount will depend on how much clients you'll got.

## Installation

* `git clone https://github.com/Clement-Ruiz/radio-bretzel.git`
* Make sure the docker daemon is stopped with `sudo systemctl stop docker`
* Add this line to the default config file of dockerd (ex : for Debian-based distros `/etc/default/docker`) : </br>
`DOCKER_OPTS="-H unix://var/run/docker -H http://18.18.19.1:12000`</br>
This file must be edited by root or an user belonging to the docker group.
You'll find more about it on the [Wiki](https://github.com/Clement-Ruiz/radio-bretzel/wiki/How-does-it-work-%3F---into-the-deeps#docker)
* start the docker daemon with `sudo systemctl start docker`
* `cd radio-bretzel/dockerizing`
* `docker-compose up -d`

# Client

* Your web browser (tested with Chromium and Firefox) should do the work !
* http://localhost !


## Infrastructure
* authentication backend
* elementary monitoring (storage/network)
* storage
* containerizing environment (ease bootstrap and app lifecycle management)
