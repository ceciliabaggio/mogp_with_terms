'''
Created on May 12, 2016

@author: cecilia
'''

""" dado un directorio, busca todos los archivos que terminen de alguna manera especificada, 
los abre, y reemplaza el:  u'number' por 'number' 

"""
import os
import sys

dir_from = str(sys.argv[1])

#dir_from="/home/cecilia/Desktop/Corridas_JAIIO/lucene_10000_docs/Cross(0.7)_Mut(0.03)/N100/Co2/295/"


#file_from = open(dir_from, "r")

for dirs in os.walk(dir_from):    
    print dirs[2]
    
    for file in dirs[2]:
        nombre =  file.split("_")
        print nombre[-3:]
        if ((nombre[-3:] ==  ['queries', 'last', 'gen.txt']) or 
            (nombre[-3:] ==  ['queries', 'first', 'gen.txt'])) :
            """por cada archivo de *queries_last_gen.txt y *queries_first_gen.txt
            hago el parsing"""                      
            print file
            
            f = open(dir_from + file, "r")
            lines = f.readlines() # lee todas las lineas en el archivo f
            f.close()
            
            f = open(dir_from + file, "w")
            for line in lines:
                line= line.replace("(u'", "('")
                line = line.replace(" u'", " '")
                f.write(line)                
                
                
            f.close()    
                
            
               
               
    #===========================================================================
    # f = open(file, "w")
    # 
    # docs = dirs[2]
    # 
    # print "topic: ",topic
    # print "docs: ",docs
    # 
    # for d in docs:
    #     f.write(d + "\n")
    #     print d
    # f.close()
    #===========================================================================