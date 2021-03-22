#!/bin/bash

# Tun run only once
# cd ~/mogp_with_spots
# $ ./mogp_training.bash 1 4 4 2 69 0.7 0.03 /home/cecilia/repos/borrar2/corridas_$(date +%F_%H-%M-%S) 1 0

# topic read from dir /topics

#<Objective_combination>
    # 1 for Co1
    # 2 for Co2
    # 3 for Co3
    # 4 for Co4
    # 5 for Co5

if [ $# != 11 ]
then
    echo "10 arguments needed"
    echo "usage: MOGP.bash <Number_of_Runs><Number_of_generations><Population_Size><Objective_combination><Initial_Random_Seed><p_cross><p_mut><saving_directory><hadoop_sub_folder><run_local><overlapped_entities>" 
    echo ""
    echo "Topic files must be in 'topics' directory from current dir"
    echo "Objective_combination: 1 for Co1. 2 for Co2 ... "
    echo "WARNING: Population_Size must be multiple of 4"
    echo "WARNING: Saving Dir must start with /"
    echo ""
    
fi

NRUN=$1
NGEN=$2
POPSIZE=$3
Obj_combination=$4
#TOPIC_ID=$6
P_CROSS=$6
P_MUT=$7
FOLDER=$8
hadoop_sub_folder=$9
# flag to run in local machine. Defaltvalue: 0 (remote)
run_local="${10:-0}"
overlapped_ent="${11:-0}" # the default is with labeled relevants (not overlapped)

#### LEE LOS TOPICOS DEL DIR /topics y los carga en un arreglo
dir_to_read_from="./index/topics/"
cant=0
topicos=()

for dir in $(ls $dir_to_read_from); 
do 
   
    temp="${dir:${#dir}-4}"
    ends_with=".txt"
    
    if [ $temp == $ends_with ] ; then 
      echo "$dir" 
      topicos[$cant]=$dir
      cant=$((cant + 1))     
      #cant tiene la cantidad de topicos en el directorio
    fi

done
####


### por cada TOPICO, repito corridas de MOGP
for item in ${topicos[*]}
do
    printf "  %s\n" $item
    
    #topic_number="${item:${#item}-4}"
    
    topic_number=$(echo $item | cut -d "." -f 1)    
    
    printf "topico numero %s\n" $topic_number

    TOPIC_ID=$item

    if [ $Obj_combination = 1 ] 	
	    then SAVE_DIR=$FOLDER"/Co1/"$topic_number    
		 echo "Combination selected Co1: Precision@10 & Recall"
	    elif [ $Obj_combination = 2 ] 	
		then SAVE_DIR=$FOLDER"/Co2/"$topic_number	
		     echo "Combination selected Co2: Precision@10 & Entropic Recall"
		elif [ $Obj_combination = 3 ] 	
		      then SAVE_DIR=$FOLDER"/Co3/"$topic_number	
			   echo "Combination selected Co3: Entropic Precision@10 & Entropic Recall"
		      elif [ $Obj_combination = 4 ] 	
			  then SAVE_DIR=$FOLDER"/Co4/"$topic_number			 
			       echo "Combination selected Co4: Precision@10 & Recall & Jaccard Index Similarity Index"
			    elif [ $Obj_combination = 5 ] 	
			      then SAVE_DIR=$FOLDER"/Co5/"$topic_number			  
				   echo "Combination selected Co5: Precision@10 & Entropic Recall & Jaccard Index Similarity Index"
				elif [ $Obj_combination = 6 ] 	
				    then SAVE_DIR=$FOLDER"/Co6/"$topic_number			
				         echo "Combination selected Co6: Precision@10 & Jaccard Index Similarity Index"
				    elif [ $Obj_combination = 7 ] 	
				      then SAVE_DIR=$FOLDER"/Co7/"$topic_number
				           echo "Combination selected Co7: Precision@10 & Jaccard Index Similarity Index & Maximum Docs Retrieved"				    
					else echo "WRONG PARAMETER <Objective_combination>"	
					     exit 0 # corta la ejecucion
    fi

    # Call to Python MOGP.py
    echo "Number of Run = "$NRUN
    echo "Number of GEN = "$NGEN
    echo "Number of POP Size = "$POPSIZE
    echo "Everlapped Entities = "$overlapped_ent
    echo "Run local= "$run_local
    echo "Save Dir = "$SAVE_DIR
    
    n=1
    TEMP=$SAVE_DIR

    while [ -d "$TEMP" ]; do
      # Control will enter here if $TEMP exists.
      echo "save dir exists"
      TEMP=$SAVE_DIR"_"$n
      let n=$n+1;
    done

    SAVE_DIR=$TEMP
    RANDOM=$5 #usa el quinto parametro como semilla
    seed=$RANDOM #primera semilla aleatoria para DEAP
    
    for run in `seq 1 $NRUN`;
    do
	    	
	python MOGPqueryReformulation.py $run $NGEN $POPSIZE $Obj_combination $seed $TOPIC_ID $P_CROSS $P_MUT $SAVE_DIR $overlapped_ent
	
	#almacena el log.log en el dir actual
	from_filename="last_dir_created"      
	
	# MODIFICA SEED para DEAP =)
	seed=$RANDOM
	
    done  

    #luego de ejecutar todas las corridas, junta la info de los fitness en un solo archivo

    if [ $Obj_combination = 1 ] || [ $Obj_combination = 2 ] || [ $Obj_combination = 3 ] || [ $Obj_combination = 6 ]
      then objective_num=2 
      elif [ $Obj_combination = 4 ] || [ $Obj_combination = 5 ] || [ $Obj_combination = 7 ]
	then objective_num=3 
    fi
      
    python joinFitnessAllRunByObjective.py $objective_num	    
    echo "Join all fitness made successfully"  
    
    zero=0

    if [ $run_local -eq $zero ]; then
      # Copy in hadoop the results for the topic
      echo "Copying results from Evolution to Hadoop.."
      /usr/local/hadoop/bin/hadoop fs -copyFromLocal $SAVE_DIR $hadoop_sub_folder
    fi
    
done
# Los paretos se generan y grafican desde el modulo PLOTTER