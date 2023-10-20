#!/usr/bin/env bash

# dir to store the combinations in hadoop
hadoop_saving_dir="/user/ubuntu/mogp/results/mogp-run_$(date +%F_%H-%M-%S)"

hadoop_folder="${1:-$hadoop_saving_dir}"
nruns="${2:-5}"
ngen="${3:-150}"
popsize="${4:-100}"
max_combination=${5:-7}
random_seed="${6:-69}"
cxp="${7:-0.7}"
mutp="${8:-0.03}"

# create the folder in hadoop
hadoop fs -mkdir $hadoop_folder

# image version of container
image_version="ceciliabaggio/mogp:0.0.24"

# memory aasignment
memory=40g

## TEMPORAL
nruns=2
ngen=4
popsize=4

function run_container () {
    declare combination="${1:-1}"
    
    mesos-execute \
      --master="192.168.244.10:5050" \
      --name=mogp-co$combination \
      --resources="cpus:4;mem:40960" \
      --command="bash -l -c '
	docker pull $image_version;
	#change for -t because mesos doesnt have TTY
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
	--name=mogp-co$combination \
	$image_version \
	bash -l -c \"./run-combination.bash $hadoop_folder $combination $nruns $ngen $popsize;\"
	docker rmi $image_version || echo \"The image could no be removed. Maybe got already removed.\";
     '" & # Send it to background to execute them in parallel.
}

for ((i=1;i<=$max_combination;i++)) ; do
    run_container "$i";
done