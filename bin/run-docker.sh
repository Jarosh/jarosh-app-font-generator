#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

docker run -p 8080:8080 -v $(realpath $DIR"/../../../lib/fonts"):/home/node/app/fonts -it $(docker build -q .)
