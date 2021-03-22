'''
Created on May 12, 2016

@author: cecilia
'''

""" 
Por cada topico en el SetX genera un archivo por topico en el 
directorio <dir_to>. Cada archivo topico.txt contiene todos los documentos
bajo ese topico
"""
import os

dir_from="/home/cecilia/workspace/MOGP_local/DMOZ@monster-usr-work-DMOZ-Sets/Sets/SetMedioCorpus/"

dir_to="/home/cecilia/workspace/MOGP_local/relevantes_por_topico_SetMedioCorpus/"

#file_from = open(dir_from, "r")

for dirs in os.walk(dir_from):    
    topic = str(dirs[0]).split("/")[-1]
    f = open(dir_to + topic + ".txt", "w")
    
    docs = dirs[2]
    
    print "topic: ",topic
    print "docs: ",docs
    
    for d in docs:
        f.write(d + "\n")
        print d
    f.close()
        
