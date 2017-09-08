# Radio bretzel
Someday we had this idea about an online space where we could stayed tuned with friends, listening to the same music at the same time, and messaging about it in real time. A space where we could all push music, and make it play on a 24/7 web radio where only the people you want could join and enjoy. A or some web radios. Depending on the style, the years, or the will of your users. Making us able to pop and manage private web radio streams in a second.

Find more information about this project on the [Documentation](https://github.com/radio-bretzel/radio-bretzel-doc) !
Ynov Students, if you want to apply, don't forget to tell me what a good fisherman you are.

# Server
## Requirements
* [Docker](https://www.docker.com/ "Docker Official Website") : docker, dockerd and docker-compose v2 binaries
* Any web browser. Test feedbacks are welcome :)

Think about the storage and network resources. The needed amount will depend on how much clients you'll got.

## Installation

So easy !
* `git clone https://github.com/radio-bretzel/radio-bretzel.git`
* `cd radio-bretzel`
* `git submodule init`
* `git submodule update`
* `docker-compose up -d`


### /!\\
> _In order to develop this project more confortably, we chose to mount api's source code 
> directly in the container, which overrides node_modules and cause "module not found" errors. 
> To bypass this, install the modules in the project directory on your host, like if you were 
> going to run it locally._
### /!\\  

# Client

* Your web browser (tested with Chromium and Firefox) should do the work !
* http://localhost !
