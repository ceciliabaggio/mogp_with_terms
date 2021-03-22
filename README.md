##mogp_with_terms

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
4. Put the following arguments: **1 10 10 7 69 529.txt 0.7 0.03 /home/cecilia/repositories/borrar**
5. Be aware of having at least one topic file for the context in the directory. In this case "529.txt"
