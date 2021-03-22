# Go to mogp_with_spots
#cd mogp_with_spots

############################

echo "JVM HEAP 8-GB - RETRIEVED DOCS 1000"

###########################
# copy indexes from Hadoop
echo "Copying from Hadoop Set12_utf8.index.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/Set12_utf8.index.tar.gz" "$(pwd)/index"

echo "Extracting Set12_utf8.index"
tar -xvzf "$(pwd)/index/Set12_utf8.index.tar.gz" -C "$(pwd)/index/"

echo "Removing Set12_utf8.index.tar.gz"
rm "$(pwd)/index/Set12_utf8.index.tar.gz"

echo "Copying from Hadoop Set3_utf8.index.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/Set3_utf8.index.tar.gz" "$(pwd)/index"

echo "extracting Set3_utf8.index"
tar -xvzf "$(pwd)/index/Set3_utf8.index.tar.gz" -C "$(pwd)/index/"

echo "Removing Set3_utf8.index.tar.gz"
rm "$(pwd)/index/Set3_utf8.index.tar.gz"

echo "Copying from Hadoop relevants12.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/relevants12.tar.gz" "$(pwd)/index"

echo "extracting relevants12.tar.gz"
tar -zxvf "$(pwd)/index/relevants12.tar.gz" -C "$(pwd)/index/"

echo "Removing relevants12.index.tar.gz"
rm "$(pwd)/index/relevants12.tar.gz"

echo "Copying from Hadoop relevants3.tar.gz"
/usr/local/hadoop/bin/hadoop fs -copyToLocal "/user/ubuntu/mogp/relevants3.tar.gz" "$(pwd)/index"

echo "extracting relevants3.tar.gz"
tar -zxvf "$(pwd)/index/relevants3.tar.gz" -C "$(pwd)/index/"

echo "Removing relevants3.tar.gz"
rm "$(pwd)/index/relevants3.tar.gz"


# Evolve the 7 combinations oer set12
folder="$(pwd)/runs/mogp-run_"$(date +%F_%H-%M-%S)

for run in {1..7}
do
  ##########
  # ------------------------>>>> WARNINg searcher retrieves 1000
  ##########
  ./mogp_training.bash 5 150 100 $run 69 0.7 0.03 $folder
  #./mogp_training.bash 2 4 4 $run 69 0.7 0.03 $folder  
  # Move Results to Hadoop
  echo "Copying results from Evolution to Hadoop"
  /usr/local/hadoop/bin/hadoop fs -copyFromLocal $folder "/user/ubuntu/mogp/results"
done

# Plot Evolution
./MOGP_PLOTTER/MOGP_PLOTTER_EVOLUTION.bash $folder"/Co1/" $folder"/Co2/" $folder"/Co3/" $folder"/Co4/"  $folder"/Co5/"  $folder"/Co6/"  $folder"/Co7/" $folder"/"

# Move Results to Hadoop
echo "Copying results from Evolution to Hadoop"
/usr/local/hadoop/bin/hadoop fs -copyFromLocal $folder "/user/ubuntu/mogp/results"

# Test evolution with set3
./mogp_evaluation/MOGP_EVALUATION.bash $folder"/"

# Plot Test
./MOGP_PLOTTER/MOGP_PLOTTER_TESTING.bash $folder"/"

# Move Results to Hadoop
echo "Copying all results to Hadoop"
/usr/local/hadoop/bin/hadoop fs -copyFromLocal $folder "/user/ubuntu/mogp/results"
