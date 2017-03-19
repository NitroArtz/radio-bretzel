# Radio bretzel

This project is used to setup your own private and collaborative webradio instance.  
Invite friends, chat, upload music, and listen !

# Server
## Requirements
* [Docker](https://www.docker.com/ "Docker Official Website") : docker-engine and docker-compose binaries
* Any web browser. Test feedbacks are welcome :)

Think about the storage and network resources. The needed amount will depend on how much clients you'll got.

## Installation

* `git clone https://github.com/Clement-Ruiz/radio-bretzel.git`
* `cd dockerizing`
* `docker-compose up -d`

# Client

* Your web browser (tested with Chromium and Firefox) should do the work ! 


# Roadmap
## Development
* authentication service

## Infrastructure
* authentication backend
* elementary monitoring (storage/network)
* storage
* containerizing environment (ease bootstrap and app lifecycle management)

## Future features
* chattyRadio timeline
* guests users
