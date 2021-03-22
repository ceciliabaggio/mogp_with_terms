#!/bin/bash

# Para una sola corrida:
# cd ~/MOGP_local_EVALUATION_lucene
# $ ./MOGP_EVALUATION.bash dir_to_read_from  


# Evalua la ULTIMA GENERACION DE CONSULTAS DE CADA CORRIDA
if [ $# != 1 ]
then
    echo "One argument needed"
    echo "usage: MOGP_EVALUATION.bash <dir_to_read_from>"
    echo ""
    echo "WARNING: <dir_to_read_from> must start and finish with /"
    echo " "
    echo "debe ser el directorio que contiene las combinacioes: Co1, Co2, etc"
    echo " "
    exit 1
fi

# Directorio actual
#CURRENT=`pwd`

for comb in $(ls $1) #POR CADA DIRECTORIO COMBINACION: Co1, Co2, ...
do
   
    combination="$1$comb"     #Ruta absoluta a variable 
	
    if [[ -d "$combination" ]]
    then
        python join_all_mean_from_first_and_last_gen_into_file.py $combination    
  fi
done
