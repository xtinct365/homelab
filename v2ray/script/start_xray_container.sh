#!/bin/bash

docker network create -d macvlan \
  --subnet=192.168.30.0/24 \
  --gateway=192.168.30.1 \
  --aux-address="my-router=192.168.30.1" \
  -o parent=eth0 macvlan30

docker run -d \
#    --restart=always \
    --privileged \
    --name xray_jms_usa \
    -e TZ=Asia/Shanghai \
    -v /lib/modules:/lib/modules \
    -v /volume1/docker/v2ray/data/geoip.dat:/usr/local/share/xray/geoip.dat:ro \
    -v /volume1/docker/v2ray/data/geosite.dat:/usr/local/share/xray/geosite.dat:ro \
    -v /volume1/docker/v2ray/config/jms_usa.json:/etc/xray/config.json:ro \
    --ip=192.168.1.2
    mzz2017/v2raya


docker run -d \
    --privileged \
    --name v2ray_usa_tproxy \
    --restart=always \
    -e TZ=Asia/Shanghai \
    -v /lib/modules:/lib/modules \
    -v /volume1/docker/v2ray/data/geoip.dat:/usr/share/v2ray/geoip.dat:ro \
    -v /volume1/docker/v2ray/data/geosite.dat:/usr/share/v2ray/geosite.dat:ro \
    -v /volume1/docker/v2ray/config/jms_usa.json:/etc/v2ray/config.json:ro \
    --network=macvlan30 \
    --ip=192.168.30.251 \
    --workdir=/root \
    --log-driver=db \
    --runtime=runc \
    -t \
    teddysun/v2ray:4.45.2


docker run -d \
    --privileged \
    --name v2ray_usa_tproxy \
    --restart=always \
    -e TZ=Asia/Shanghai \
    -v /lib/modules:/lib/modules \
    -v /volume1/docker/v2ray/data/geoip.dat:/usr/share/v2ray/geoip.dat:ro \
    -v /volume1/docker/v2ray/data/geosite.dat:/usr/share/v2ray/geosite.dat:ro \
    -v /volume1/docker/v2ray/config/jms_usa.json:/etc/v2ray/config.json:ro \
    --network=macvlan30 \
    --ip=192.168.30.251 \
    --workdir=/root \
    --log-driver=db \
    --runtime=runc \
    -t \
    teddysun/v2ray:4.45.2


docker run -d --privileged --name=v2ray_hk_tproxy --restart=always -e TZ=Asia/Shanghai -v=/volume1/docker/v2ray/config/jms_hk.json:/etc/v2ray/config.json:ro -v=/lib/modules:/lib/modules -v=/volume1/docker/v2ray/data/geoip.dat:/usr/share/v2ray/geoip.dat:ro -v=/volume1/docker/v2ray/data/geosite.dat:/usr/share/v2ray/geosite.dat:ro --network=macvlan30 --ip=192.168.30.252 -t teddysun/v2ray:4.45.2 