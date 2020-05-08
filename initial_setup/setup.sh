#!/bin/sh

export http_proxy=muc1-prxy.sdi.trendnet.org:8080

mkdir -p /etc/systemd/system/docker.service.d

cp http_proxy.conf /etc/systemd/system/docker.service.d/http_proxy.conf

cat /etc/systemd/system/docker.service.d/http_proxy.conf

systemctl daemon-reload
