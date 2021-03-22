'''
Created on Jun 6, 2016

@author: cecilia

Solo para usar con archivos de JAIIO, que MOGP no generaba un archivo con todas 
las entropic_precision_all_run. Asi que lo extrae de *_all_run.txt
 
Cada archivo:

    RUN_1    RUN_2                RUN_N
---------------------------------------------------
    ind1    ind2                   ind1     GEN 1
    ind2    ind2                   ind2
    ...
    
    indM    indM                   indM     
    
    ind1    ind2                   ind1     GEN 2
    ind2    ind2                   ind2
    ...
    
    indM    indM                   indM            



'''

import sys
import os
import re
from tabulate import tabulate

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#if (len(sys.argv)!= 2):
    #print "Number of lines missing or Topic ID"

#file_path = open(os.getcwd()+"/last_dir_created", "r")
#path = str(file_path.readline())

'''de prueba'''
path = str('/home/cecilia/Desktop/Corridas_JAIIO/lucene_10000_docs/Cross(0.7)_Mut(0.03)/N100/Co2/528')

print "current path: ", path

nRuns = 0

files = os.listdir(path)

entropic_recall_files=[]



for filename in files:
    m = re.split('_', filename)
    if (len(m) == 11 and m[10]=="info.txt"):
        nRuns = nRuns + 1      
        objectives = m[2]
        nGen=m[3]
        popSize = m[4]
        indSize = m[5]
        cross = m[6]
        mut = m[7]
        seed = m[8]
        TOPIC = m[0]
        entropic_recall_files.append(filename)             
                    

"""CAntidad de lineas de un rchivo: NGEN*(POPSIZE+1) por las lineas en blanco"""
""" se obtiene del nombre del archivo el nro de generaciones y tamanio de la poblacion"""
G = (nGen.split("(")[1]).split(")")[0]
Pop = (popSize.split("(")[1]).split(")")[0] 

num_lines = int(G) * (int(Pop)+1)


"""ordena los archivos alfabeticamente """ 
entropic_recall_files= sorted(entropic_recall_files, key=lambda x: int(x.split('_')[1]))

print entropic_recall_files
    
#print globalRecall_files
#print jaccard_files
 


#===============================================================================
### PARA RECALL ENTROPICO


file_allRecallEntropic = open(path +"/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_entropicRecall_all_run.txt", "w")
   
opened_files = []
for F in entropic_recall_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_rec = []
table_recall = []


for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline())       
        l = linea.split()                 
        if l != []:
            print l[3]                     
            s_rec.append(l[3])            
        else:
            s_rec.append(" ")            
   
    table_recall.append(s_rec)
    s_rec = []  

       
file_allRecallEntropic.write(tabulate(table_recall,tablefmt="plain"))
file_allRecallEntropic.close()  
print "File created: *_entropicRecall_all_run.txt"
  
for f in opened_files:
    f.close() 
    

#===============================================================================
### PARA RECALL 


file_allRecallEntropic = open(path +"/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_recall_all_run.txt", "w")
   
opened_files = []
for F in entropic_recall_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_rec = []
table_recall = []


for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline())       
        l = linea.split()                 
        if l != []:
            print l[2]                     
            s_rec.append(l[2])            
        else:
            s_rec.append(" ")            
   
    table_recall.append(s_rec)
    s_rec = []  

       
file_allRecallEntropic.write(tabulate(table_recall,tablefmt="plain"))
file_allRecallEntropic.close()  
print "File created: *_recall_all_run.txt"
  
for f in opened_files:
    f.close()             


                


