'''
Created on May 13, 2016

@author: cecilia
@param Directorio del cual extraer la primera generacion de TODAS las corridas:

Usage: 
    
    python recorte_gen_1.py  "/home/cecilia/.../dir_from/"

'''

""" Extrae la generacion 1 de cada corrida en un archivo separado"""

import os
import sys

dir_from = str(sys.argv[1])

#dir_from="/home/cecilia/Desktop/Corridas_JAIIO/lucene_10000_docs/Cross(0.7)_Mut(0.03)/N100/Co2/295/"


#file_from = open(dir_from, "r")

for dirs in os.walk(dir_from):    
    #print dirs[2]
    
    for file in dirs[2]:
        nombre =  file.split("_")
        #print nombre[-1:]
        if (nombre[-1:] ==  ['queries.txt']):
            """ por cada archivo de *queries.txt, hago el parsing"""            
            #print "iguales"
            print file
            file_copia = file
            
            f_origen = open(dir_from + file, "r") #archivo original de queries
            nuevo = str(file_copia).replace(".txt", "_first_gen.txt")
            f_destino = open(dir_from + nuevo , "w") #archivo con gen 1
            
            line = f_origen.readline() # lee una linea del archivo
            
            while (line != "\n"):               
                #elimina caracter 'u
                line= line.replace("(u'", "('")
                line = line.replace(" u'", " '")
                f_destino.write(str(line))
                line = f_origen.readline() # lee una linea del archivo 
           
            
            f_origen.close()
            f_destino.close()
            
                         
            