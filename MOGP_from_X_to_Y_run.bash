#!/bin/bash

# Para una sola corrida:
# el directorio donde guardar se pasa directamente como parametro
# cd ~/workspace/MOGP_local 
# $ ./MOGP.bash 1 1 4 1 42 129.txt 0.7 0.03 /home/........./corridas/....

if [ $# != 10 ]
then
    echo "10 arguments needed"
    echo "usage: MOGP.bash <Hasta_corrida><Number_of_generations><Population_Size><Recall_Method><Initial_Random_Seed><Topic_File><p_cross><p_mut><saving_directory><desde_corrida>" 
    echo ""
    echo "WARNING: Population_Size must be multiple of 4"
    echo "WARNING: Saving Dir must start with /"
    echo ""
    exit 1
fi

# Directorio actual
CURRENT=`pwd`
#BASENAME=`basename "$CURRENT"`
NRUN_DESDE=${10}
NRUN=$1
NGEN=$2
POPSIZE=$3
RECALL=$4
TOPIC_ID=$6
P_CROSS=$7
P_MUT=$8
FOLDER=$9
#SAVE_DIR=$CURRENT$FOLDER"/Cross("$P_CROSS")_Mut("$P_MUT")/N"$POPSIZE"/Results_MOGP"

#if [ $RECALL = 1 ] 
#	then SAVE_DIR=$CURRENT$FOLDER"/Cross("$P_CROSS")_Mut("$P_MUT")/N"$POPSIZE"/Co2/Results_MOGP"
#	else SAVE_DIR=$CURRENT$FOLDER"/Cross("$P_CROSS")_Mut("$P_MUT")/N"$POPSIZE"/Co1/Results_MOGP"
#fi

SAVE_DIR=$FOLDER

echo $SAVE_DIR


n=1
#TEMP=$SAVE_DIR

#while [ -d "$TEMP" ]; do
  # Control will enter here if $TEMP exists.
#  echo "save dir exists"
#  TEMP=$SAVE_DIR"_"$n
#  let n=$n+1;
#done

#SAVE_DIR=$TEMP


RANDOM=$5 #usa el quinto parametro como semilla

for s in `seq 1 $NRUN_DESDE`;
do

  seed=$RANDOM #primera semilla aleatoria para DEAP
  echo $seed
  
done


# Call to Python MOGP.py
echo "Number of Run = "$NRUN
echo "Number of GEN = "$NGEN
echo "Number of POP Size = "$POPSIZE

if [ $RECALL = 1 ] 
	then echo "Recall method = Entropic Recall"
	else echo "Recall method = Ordinary Recall"
fi

for run in `seq $NRUN_DESDE $NRUN`;
do
	
	#echo "-----Call $i to MOGPqueryReformulation-----"
	#echo "Seed = "$seed

	python MOGPqueryReformulation_1_0.py $run $NGEN $POPSIZE $RECALL $seed $TOPIC_ID $P_CROSS $P_MUT $SAVE_DIR
	
	#almacena el log.log en el dir actual
	from_filename="last_dir_created"

	#for line in $(cat $from_filename); do echo "$line" ; done

	#mv "log.log" "$line/log_$run.log" 
	#echo "log.log has been moved to $line"
	#mv "errors.log" "$line/errors_$run.log" 
	#echo "errors.log has been moved to $line"	  
	
	# MODIFICA SEED para DEAP =)
	seed=$RANDOM
done  

#luego de ejecutar todas las corridas, junta la info de los fitness en un solo archivo

#for dir in $(cat $1); do echo "$dir" ; done
#echo "directorio de corridas $dir"

python joinFitnessAllRunByObjective.py    

echo "Join all fitness made successfully"
