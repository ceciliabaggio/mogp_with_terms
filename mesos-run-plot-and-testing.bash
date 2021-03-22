#!/usr/bin/env bash

# Folder from hadoop where are all the combinations
if [ $# != 2 ]
then
    echo "2 arguments needed"
    echo "usage: mesos-run-plot-and-testing.bash <hadoop_dir_of_results> <container_image_version>"     
    echo "example: ./mesos-run-plot-and-testing.bash /user/ubuntu/mogp/results/mogp-run_2018-05-06_14-31-0 ceciliabaggio/mogp:0.0.18"
    echo ""
    exit 1
fi

hadoop_folder=$1
echo "Hadoop folder: "$hadoop_folder

image_version=$2
echo "Docker image version: "$image_version

memory=40g

mesos-execute
      --master="192.168.244.10:5050" \
      --name=mogp-co$combination \
      --resources="cpus:4;mem:40960" \
      --command="bash -l -c '
	docker pull $image_version;
	docker run --rm -t \
	--memory=$memory \
	--memory-swap=$memory \
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
	--name=mogp-plot \
	$image_version \
	bash -l -c \"./run-plot-and-testing.bash $hadoop_folder;\"
	docker rmi $image_version || echo \"The image could no be removed. Maybe got already removed.\";
  '" &