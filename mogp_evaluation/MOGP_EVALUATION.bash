#!/bin/bash

# Para una sola corrida:
# cd ~/mogp_with_spots/mogp_evaluation
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

echo "estoy en $(pwd)"

for comb in $(ls $1) #POR CADA DIRECTORIO COMBINACION: Co1, Co2, ...
do
   
    combination="$1$comb"     #Ruta absoluta a variable 
	
    if [[ -d "$combination" ]]
    then

	echo $combination
	let CANT=0
	
	for topic_folder in $(ls $combination) # POR CADA TOPICO DENTRO DE Co1, Co2 ...
	do  

	    dir_to_read_from="$combination/$topic_folder/"

	    echo "Current directory: "$dir_to_read_from
	    #RECUPERA TODOS LOS ARCHIVOS DE UN DIRECTORIO CON CONSULTAS DE LAS PRIMERAS GENERACIONES
	    #Y LOS EVALUA
	    for dir in $(ls $dir_to_read_from); 
	    do 	  
		temp="${dir:${#dir}-21}"
		ends_with="queries_first_gen.txt"
		
		if [ $temp == $ends_with ] ; then 	   
		  python "$(pwd)"/mogp_evaluation/MOGP_evaluation_first_gen.py $dir_to_read_from $dir		
		fi
	    done

	    #RECUPERA TODOS LOS ARCHIVOS DE UN DIRECTORIO CON CONSULTAS DE ULTIMAS GENERACIONES
	    #Y LOS EVALUA
	    for dir in $(ls $dir_to_read_from); 
	    do 
	      
		temp="${dir:${#dir}-20}"
		ends_with="queries_last_gen.txt"

		if [ $temp == $ends_with ] ; then       	      
		  python "$(pwd)"/mogp_evaluation/MOGP_evaluation_last_gen.py $dir_to_read_from $dir				  
		fi
	    done

	    #GENERA ARCHIVOS DE PROMEDIO DE PRECISION / GLOBAL RECALL / JACCARD PARA PRIMERA GENERACION
	    echo 'ENTRO A MOGP_evaluation_mean_Pr_GRec_Jind_GEN_1.py '
	    python "$(pwd)"/mogp_evaluation/MOGP_evaluation_mean_Pr_GRec_Jind_GEN_1.py $dir_to_read_from	    
	    echo 'SALI DE MOGP_evaluation_mean_Pr_GRec_Jind_GEN_1.py '

	    #GENERA ARCHIVOS DE PROMEDIO DE PRECISION / GLOBAL RECALL / JACCARD PARA ULTIMA GENERACION
	    python "$(pwd)"/mogp_evaluation/MOGP_evaluation_mean_Pr_GRec_Jind.py $dir_to_read_from	    	    
	    
	done      

    #GENERA ARCHIVO DE PROMEDIOS GENERALES POR COMBINACION.
    #SE EXTRAE EL PROMEDIO DE LAS CORRIDAS DE CADA TOPICO (EJ: MEAN_GLOBAL_RECALL_FROM_TESTING_GEN_1.txt)
    #Y LOS PONE EN UN ARCHIVO
    python "$(pwd)"/mogp_evaluation/join_all_mean_from_first_and_last_gen_into_file.py $combination    
  fi
done

	