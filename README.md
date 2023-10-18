
Last working vesion of MOGP with terms.
It is configured to build queries using only the OR operator.
For AND, OR and NOT ops uncomment lines 303, 305, 334, 336

Functionality to control overlapped entities is not fully developed.

Ignore mesos* files from repo (these are for running the algorithm in the Compute Canada Cloud).


---

**CAll to MOGP from command line**

Open a console. 

1. Go to $ ~/repositories/mogp_with_terms
2. $ ./mogp_training.bash 5 150 100 7 69 0.7 0.03 ~/save_dir

The arguments needed are:
MOGP_TRAINING.bash <number_of_runs> <number_of_generations> <population_size> <objective_combination> <initial_random_seed> <p_cross> <p_mut> <saving_directory>



---

**CAll to MOGPqueryReformulation from Eclipse**


1. Go to Propertis of the file MOGPqueryReformulation.py
2. Run and Debug settings
3. Select 'Edit/Arguments'
4. Put the following arguments: **1 10 10 7 69 529.txt 0.7 0.03 /home/cecilia/repositories/runs**
5. Be aware of having at least one topic file for the context in the directory. In this case "529.txt"


The core of the system is in file: MOGPqueryReformulation.py

---

Lucene indexes and the DMOZ dataset are not on gitHub. 

You can rebuild the index using the Indexer code, that is in the Index directory.

The Dataset has been published here: https://data.mendeley.com/datasets/9mpgz8z257/1

Otherwise, please write me an email (cb@cs.uns.edu.ar) and I will be glad to send the index to you :)

---
PyLucene 4.9.0 - Java openjdk-7-jdk - 
