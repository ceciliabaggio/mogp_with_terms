Para ejecutar el módulo de evaluación sobre el test-set (SET 3 de DMOZ):


cd ~/MOGP_local_EVALUATION_lucene
$ ./MOGP_EVALUATION.bash dir_to_read_from  

*********RECORDAR************
sacar todos los .eps de los directorios Co1, Co2, etc

donde:

* dir_to_read_from es el directorio que contiene las combinaciones Co1 - Co2 - Co3 ...
* En cada directorio combinacion (Co1 - ..) se leen los archivos correspondientes a los resultados de 
evaluar la primera y la ultima generacion de consultas (DE CADA CORRIDA) sobre el test-set. Estos son:

  - 1_1_Prec@10-Recall-Jaccard_nGen(150)_popSize(100)_indSize(10)_cross(0.7)_mut(0.03)_seed(18289)_EVALUATION_GEN_1__precision.txt
    ...
  - 1_5_Prec@10-Recall-Jaccard_nGen(150)_popSize(100)_indSize(10)_cross(0.7)_mut(0.03)_seed(18289)_EVALUATION_GEN_1__precision.txt
  
  - 1_1_Prec@10-Recall-Jaccard_nGen(150)_popSize(100)_indSize(10)_cross(0.7)_mut(0.03)_seed(30254)_EVALUATION_GEN_1__entropicRecall.txt
    ...
  - 1_5_Prec@10-Recall-Jaccard_nGen(150)_popSize(100)_indSize(10)_cross(0.7)_mut(0.03)_seed(30254)_EVALUATION_GEN_1__entropicRecall.txt
  
Luego, se calcula el promedio de dichos valores, y se almacenan en

  Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt
  Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt
  ...

Estos archivos contienen las medias para cada uno de los tópicos de una combinación. Es decir, si la combinación tiene 25 tópicos,
el archivo constará de 25 líneas, cada linea es el promedio de un tópico.

Luego, copiar en @monster los archivos anteriores,y ejecutar en Matlab los scripts:

NORMFIT_CI_1st_and_last_gen_GLOBAL_RECALL.m
NORMFIT_CI_1st_and_last_gen_JACCARD.m
NORMFIT_CI_1st_and_last_gen_PRECISION.m

que calculan los IC y grafica error bars, basado en los archivos anteriores







