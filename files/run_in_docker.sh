#!/bin/bash


XAUTH=${XAUTHORITY:-$HOME/.Xauthority}
DOCKER_XAUTHORITY=${XAUTH}.docker
cp --preserve=all $XAUTH $DOCKER_XAUTHORITY.$$
xauth nlist $DISPLAY | sed -e 's/^..../ffff/' | xauth -f $DOCKER_XAUTHORITY.$$ nmerge -
mv $DOCKER_XAUTHORITY.$$ $DOCKER_XAUTHORITY

X11_XAUTH="-e XAUTHORITY=$DOCKER_XAUTHORITY "
X11_XAUTH+="-v $DOCKER_XAUTHORITY:$DOCKER_XAUTHORITY:ro "

X11_DISPLAY="-e DISPLAY=unix$DISPLAY "
X11_DISPLAY+="-v /tmp/.X11-unix:/tmp/.X11-unix:ro "

X11_DISPLAY_RW="-e DISPLAY=unix$DISPLAY "
X11_DISPLAY_RW+="-v /tmp/.X11-unix:/tmp/.X11-unix:rw "

X11_FLAGS=$X11_XAUTH$X11_DISPLAY
X11_FLAGS_RW=$X11_XAUTH$X11_DISPLAY_RW

docker build -t {{ project_name }}_image .
docker run -it --rm --user=$UID -e USER=$USER \
       $X11_FLAGS \
       --volume="$HOME:$HOME" \
	     --volume="/etc/group:/etc/group:ro" \
	     --volume="/etc/passwd:/etc/passwd:ro" \
	     --volume="/etc/shadow:/etc/shadow:ro" \
	     --volume="/etc/sudoers.d:/etc/sudoers.d:ro" --name {{ project_name }}_container {{ project_name }}_image /bin/bash
