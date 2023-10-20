#!/usr/bin/env bash

if [ $# != 8 ]
then
    echo "2 arguments needed - optional parameters:"
    echo "usage: run_combination.bash <hadoop_saving_dir_of_combinations> <combination_number> <nruns> <ngen> <popsize> <random_seed> <cxp> <mutp>"
    echo "example: ./run_combination.bash '/mogp-run_'$(date +%F_%H-%M-%S) 1"
    echo ""
    #exit 1
fi

# Folder to save all combinations locally and then in Hadoop
hadoop_saving_dir="/user/ubuntu/mogp/results/mogp-run_$(date +%F_%H-%M-%S)"
hadoop_folder="${1:-$hadoop_saving_dir}"
combination=${2:-7}
nruns="${3:-5}"
ngen="${4:-150}"
popsize="${5:-100}"
random_seed="${6:-69}"
cxp="${7:-0.7}"
mutp="${8:-0.03}"
run_from_local=0
overlapped_ent=0


echo "Combination "$combination

saving_dir=$(pwd)'/runs'
echo "Saving dir: "$saving_dir

# copy indexes from Hadoop
echo "Copying from Hadoop Set12_utf8_term.index.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/Set12_utf8_term.index.tar.gz" "$(pwd)/index"

echo "Extracting Set12_utf8.index"
tar -xvzf "$(pwd)/index/Set12_utf8_term.index.tar.gz" -C "$(pwd)/index/"

echo "Removing Set12_utf8_term.index.tar.gz"
rm "$(pwd)/index/Set12_utf8_term.index.tar.gz"

echo "Copying from Hadoop relevants12.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/relevants12.tar.gz" "$(pwd)/index"

echo "extracting relevants12.tar.gz"
tar -zxvf "$(pwd)/index/relevants12.tar.gz" -C "$(pwd)/index/"

echo "Removing relevants12.index.tar.gz"
rm "$(pwd)/index/relevants12.tar.gz"

# create in Hadoop sub directory for the combination
hadoop_sub_folder="$hadoop_folder/Co$combination"
/usr/local/hadoop/bin/hadoop fs -mkdir $hadoop_sub_folder

# the current evolution
./mogp_training.bash $nruns $ngen $popsize $combination $random_seed $cxp $mutp $saving_dir $hadoop_sub_folder $run_from_local $overlapped_ent

error_file="Co"$combination"_evolution_errors.txt"

# rename file "evolution_errors.txt"
mv "evolution_errors.txt" $error_file

# upload the errors to hadoop
echo "copying "$error_file" to hadoop"
/usr/local/hadoop/bin/hadoop fs -copyFromLocal $error_file $hadoop_folder
