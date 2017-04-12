#!/bin/bash
# This turn off the entire application, removing every container attached to it.


# In Order to Work, this script will use of the ./system/${INSTANCE_ID}/source_ct_list
# From every line it'll find, run the docker command "docker container rm -f " for each.
# Finally, --> docker-compose down

declare INSTANCE_ID="1"                                       # This one will be dynamically handled later. Notify the quotes
