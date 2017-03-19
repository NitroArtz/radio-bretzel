# Radio bretzel

This project is used to setup your own private and collaborative webradio instance.  
Invite friends, chat, upload music, and listen !
More information are available on the DOC.md file

# Server
## Requirements
* We highly recommend a Debian-based distro
* [Liquidsoap](http://savonet.sourceforge.net/download.html "Official LiquidSoap's repository (sourceforge)")
* [Icecast2](http://http://icecast.org/download/ "Official Icecast2 website")

Think about the storage and network resources. The needed amount will depend on how much clients you'll got.

## Installation

* Copy  "config/" folder in /etc renaming it as "icecast2"
* Restart Icecast service
* Run script/test.liq to see if it's working !

# Client

* Any compatible webradio-compatible player (Clementine, VLC, etc). Your web browser (tested with Chromium and Firefox) should do the work !


# Roadmap
## Development
* authentication service

## Infrastructure
* authentication backend
* elementary monitoring (storage/network)
* storage

## Dockerizing
Go checkout the [papyDocker branch](https://github.com/Clement-Ruiz/radio-bretzel/tree/papyDocker "RadioBretzel - papyDocker branch") for our containerised version of the app
