#!/usr/bin/python
'''
Created on May 22, 2017

@author: cecilia
@param directorio CoX: combinacion de objetivos

Ej: python generar_pretos_Pr_Rec.py <dir_Co1>
'''
''' Sirve para generar los frentes de pareto (ultima generacion) de corridas
generadas con anterioridad, donde no fueron calculados. Se extrae la Pr_Rec de 
los archivos precision_all_run y recall_all_run de todos los subdirectorios de
cada combinacion '''

import sys
import os

# Invocacion del script    
if len(sys.argv) == 4:
    
    directory = str(sys.argv[1])
    comb = sys.argv[2]
    popsize = int(sys.argv[3])
    print directory, 'combination  = ', comb
    
else:
    print "debe ingresar el directorio de la combinacion desde donde leer"
    print " "
    print "Ejemplo: python \
generar_pretos_Pr_Rec.py  /home/Cecilia/workspace/.../Co5/215/ <COMBINACION> <POPSIZE>"
    sys.exit()
    
subdir = os.listdir(directory)

###
### DESCOMENTAR SI SE QUIEREN LOS FRENTES DE TODOS LOS TOPICOS
###
#for topic in subdir:    
#    print topic
#    topic_url = directory + topic + '/' 
#    print "Generating Pareto front LAST Gen - ", topic_url
#    os.system('python pareto_PRECISION_RECALL.py %d "%s" "%s"'% (popsize, topic_url, comb))
#    print "Generating Pareto front FIRST Gen - ", topic_url
#    os.system('python pareto_PRECISION_RECALL_1st.py %d "%s" "%s"'% (popsize, topic_url, comb))  


###
### FRENTES DEL TOPICO 529 - SOLAR SYSTEM
###    
topic = '529'
topic_url = directory + topic + '/' 
print "Generating Pareto front LAST Gen - ", topic_url
os.system('python pareto_PRECISION_RECALL.py %d "%s" "%s"'% (popsize, topic_url, comb))
print "Generating Pareto front FIRST Gen - ", topic_url
os.system('python pareto_PRECISION_RECALL_1st.py %d "%s" "%s"'% (popsize, topic_url, comb))      