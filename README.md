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

So easy !
* `git clone https://github.com/Clement-Ruiz/radio-bretzel.git`
* `cd radio-bretzel`
* `git submodule init`
* `git submodule update`
* `docker-compose up -d`


**/!\\** 
 _In order to develop this project more confortably, we chose to mount api's source code 
directly in the container, which overrides node_modules and cause "module not found" errors. 
To bypass this, install the modules in the project directory on your host, like if you were 
going to run it locally._
**/!\\**  

# Client

* Your web browser (tested with Chromium and Firefox) should do the work !
* http://localhost !
