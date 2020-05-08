#!/bin/sh

sh initial_setup/setup.sh

docker stack deploy -c crcmon_stack.yml crcmon

docker stack ls
