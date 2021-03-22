#/bin/bash

for topic in $(ls $1) #POR CADA DIRECTORIO COMBINACION: Co1, Co2, ...
do

    combination="$1$topic"     #Ruta absoluta a variable (La verdad es que esto mas bien sobra)

    echo $combination         #Muestro la ruta absoluta del directorio por pantalla

    for topic_folder in $(ls $combination) # POR CADA TOPICO DENTRO DE Co1, Co2 ...
    do  
	dir_to_read_from="$combination/$topic_folder"
	echo $(pwd)
	
	
	
	cd ..                #Salgo del directorio
	#echo $(pwd)
    done      

done

cd ..
cd ..
