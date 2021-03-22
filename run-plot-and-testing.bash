#!/usr/bin/env bash


### Should be run from a new container with an empty "/runs" folder
### After all combinations have beeen terminated

if [ $# != 1 ]
then
    echo "1 argument needed"
    echo "usage: run-plot-and-testing.bash <hadoop_dir_of_results> "     
    echo "example: ./run-plot-and-testing.bash  /user/ubuntu/mogp/results/mogp-run_2018-05-06_14-31-09"
    echo ""
    exit 1
fi

# copy from Hadoop the results to plot in directory /runs
hadoop_folder=$1
echo "Copying from Hadoop: "$hadoop_folder
echo "to local folder: "$(pwd)"/runs"
/usr/local/hadoop/bin/hadoop fs -copyToLocal $hadoop_folder"/*" "$(pwd)/runs"

mkdir $(pwd)"/plots"
plots_folder=$(pwd)"/plots"

# Plot Evolution
./MOGP_PLOTTER/MOGP_PLOTTER_EVOLUTION.bash $(pwd)"/runs/Co1/" $(pwd)"/runs/Co2/" $(pwd)"/runs/Co3/" $(pwd)"/runs/Co4/" $(pwd)"/runs/Co5/" $(pwd)"/runs/Co6/" $(pwd)"/runs/Co7/" $plots_folder"/"

# Move Results to Hadoop
echo "Copying plots from Evolution to Hadoop"
/usr/local/hadoop/bin/hadoop fs -copyFromLocal $plots_folder $hadoop_folder

# copy testing indexes from Hadoop
echo "Copying from Hadoop Set3_utf8_term.index.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/Set3_utf8_term.index.tar.gz" "$(pwd)/index"

echo "extracting Set3_utf8_term.index.tar.gz"
tar -xvzf "$(pwd)/index/Set3_utf8_term.index.tar.gz" -C "$(pwd)/index/"

echo "Removing Set3_utf8_term.index.tar.gz"
rm "$(pwd)/index/Set3_utf8_term.index.tar.gz"

echo "Copying from Hadoop relevants3.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/relevants3.tar.gz" "$(pwd)/index"

echo "extracting relevants3.tar.gz"
tar -zxvf "$(pwd)/index/relevants3.tar.gz" -C "$(pwd)/index/"

echo "Removing relevants3.tar.gz"
rm "$(pwd)/index/relevants3.tar.gz"


# Test evolution with set3
./mogp_evaluation/MOGP_EVALUATION.bash "$(pwd)/runs/"

# Plot Test
./MOGP_PLOTTER/MOGP_PLOTTER_TESTING.bash "$(pwd)/runs/"

# Move Results to Hadoop
echo "Copying all results inside /runs to Hadoop"
for f in runs/*; do
  #echo "File -> $f"; 
  /usr/local/hadoop/bin/hadoop fs -copyFromLocal $pwd$f $hadoop_folder
done