#!/bin/sh

export http_proxy=sjc1-prxy.sdi.trendnet.org:8080
#curl -fsSL https://get.docker.com -o get-docker.sh
#sh get-docker.sh
#systemctl start docker

mkdir -p /etc/systemd/system/docker.service.d
cp http_proxy.conf /etc/systemd/system/docker.service.d/http_proxy.conf
cat /etc/systemd/system/docker.service.d/http_proxy.conf
systemctl daemon-reload
systemctl restart docker

docker network create --driver overlay crcmonNet

docker image pull orangefolder/crcmon_flask:1.0
docker image pull orangefolder/crcmon_nginx:1.0
