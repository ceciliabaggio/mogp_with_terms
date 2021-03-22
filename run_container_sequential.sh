#!/usr/bin/env bash

# Log in Docker-hub with shared collaborator username
#echo "computecanada" | docker login --username ccanadauser --password-stdin 

image_version="ceciliabaggio/mogp:0.0.18"

# Pull mogp image from Docker-hub
docker pull $image_version

#run the container
#docker run --rm -it \
#docjer run -it -d \
docker run -it \
    --memory=40g \
    --memory-swap=40g \
    --volume /usr/local/hadoop/:/usr/local/hadoop/ \
    --add-host=rumourflow-1:192.168.244.10        \
    --add-host=rumourflow-slave-1:192.168.244.29  \
    --add-host=rumourflow-slave-2:192.168.244.30  \
    --add-host=rumourflow-slave-3:192.168.244.31  \
    --add-host=rumourflow-slave-4:192.168.244.32  \
    --add-host=rumourflow-slave-5:192.168.244.72  \
    --add-host=rumourflow-slave-6:192.168.244.61  \
    --add-host=rumourflow-slave-7:192.168.244.62  \
    --add-host=rumourflow-slave-8:192.168.244.63  \
    --add-host=rumourflow-slave-9:192.168.244.64  \
    --add-host=rumourflow-slave-10:192.168.244.67 \
    --add-host=rumourflow-slave-11:192.168.244.73 \
    --add-host=rumourflow-slave-12:192.168.244.68 \
    --add-host=rumourflow-slave-13:192.168.244.66 \
    --add-host=rumourflow-slave-14:192.168.244.69 \
    --name=mogp_1000 \
    $image_version \
    bash -c "./RUN.bash;"