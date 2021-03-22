'''
Created on May 3, 2016

@author: cecilia

Genera archivos que contienen, para todas las GEN todas las CORRIDAS
* Precision@10 
* Recall (el que se tome como objetivo)
* Global Recall
* Similitud de consultas (Jaccard)

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

print 'Number of arguments:', len(sys.argv), 'arguments.'
#if (len(sys.argv)!= 2):
    #print "Number of lines missing or Topic ID"

file_path = open(os.getcwd()+"/last_dir_created", "r")
path = str(file_path.readline())

'''de prueba'''
#path = str('/home/cecilia/workspace/MOGP_local/corridas/test_entropic_precision')
#path = str('/home/cecilia/workspace/MOGP_local_Co4_lucene/corridas_10-31/Cross(0.7)_Mut(0.03)/N100/Co4/134')
print "current path: ", path

nRuns = 0

NUM_OBJECTIVES = sys.argv[1]


print "num objetivos: ", NUM_OBJECTIVES

files = os.listdir(path)
fitness_files = []
globalRecall_files = []
jaccard_files=[]
precision_files=[]
entropic_precision_files=[]
recall_files=[]
entropic_recall_files=[]
indiv_jaccard_files=[]

for filename in files:
    m = re.split('_', filename)
    if (len(m) == 10 and m[9]=="fitness.txt"):
        nRuns = nRuns + 1
        fitness_files.append(filename)
        objectives = m[2]
        nGen=m[3]
        popSize = m[4]
        indSize = m[5]
        cross = m[6]
        mut = m[7]
        seed = m[8]
        TOPIC = m[0]
    elif (len(m) == 10 and m[9]=="globalRecall.txt"):
        globalRecall_files.append(filename)
    elif (len(m) == 10 and m[9]=="meanJaccardIndex.txt"):
        jaccard_files.append(filename)        
    elif (len(m) == 10 and m[9]=="precision.txt"):
        precision_files.append(filename)          
    elif (len(m) == 10 and m[9]=="recall.txt"):
        recall_files.append(filename) 
    elif (len(m) == 10 and m[9]=="entropicRecall.txt"):
        entropic_recall_files.append(filename)
    elif (len(m) == 10 and m[9]=="entropicPrecision.txt"):
        entropic_precision_files.append(filename)         
    elif (len(m) == 10 and m[9]=="Indiv_JaccardIndex.txt"):
        indiv_jaccard_files.append(filename)                                     
        
            

"""CAntidad de lineas de un rchivo: NGEN*(POPSIZE+1) por las lineas en blanco"""
""" se obtiene del nombre del archivo el nro de generaciones y tamanio de la poblacion"""
G = (nGen.split("(")[1]).split(")")[0]
Pop = (popSize.split("(")[1]).split(")")[0] 

num_lines = int(G) * (int(Pop)+1)


"""ordena los archivos alfabeticamente """ 
fitness_files = sorted(fitness_files, key=lambda x: int(x.split('_')[1]))
globalRecall_files = sorted(globalRecall_files, key=lambda x: int(x.split('_')[1]))
jaccard_files = sorted(jaccard_files, key=lambda x: int(x.split('_')[1]))

precision_files= sorted(precision_files, key=lambda x: int(x.split('_')[1]))
recall_files= sorted(recall_files, key=lambda x: int(x.split('_')[1]))
entropic_recall_files= sorted(entropic_recall_files, key=lambda x: int(x.split('_')[1]))
entropic_precision_files= sorted(entropic_precision_files, key=lambda x: int(x.split('_')[1]))
indiv_jaccard_files = sorted(indiv_jaccard_files, key=lambda x: int(x.split('_')[1]))

print precision_files
print recall_files
print entropic_precision_files
print entropic_recall_files
    
#print globalRecall_files
#print jaccard_files
 
#===============================================================================
### PARA OBJETIVOS

#file_all_obj_1 = open(path + "/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_recall_all_run.txt", "w")
#file_all_obj_2 = open(path + "/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_precision_all_run.txt", "w")
file_all_obj_1 = open(path +"/"+ TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_objective_1_all_run.txt", "w")
file_all_obj_2 = open(path +"/"+ TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_objective_2_all_run.txt", "w")
if (NUM_OBJECTIVES == 3):
    file_all_obj_3 = open(path +"/"+ TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_objective_3_all_run.txt", "w")
           
opened_files = []
for F in fitness_files:
    opened_files.append(open(path+"/" + F, "r"))  
   
s_prec = []
s_rec = []
s_jac=[]
table_precision = []
table_recall = []
table_jaccard_individual=[]
 
prec=0
rec=1
jac=2
 
for x in range(0,num_lines):
    for i in range(0, len(opened_files)):    
        
        linea = str(opened_files[i].readline().strip())
        linea = linea.split()    
        if linea != []:
            s_prec.append(linea[prec])
            s_rec.append(linea[rec])
            if (NUM_OBJECTIVES == 3):
                s_jac.append(linea[jac])
        else:
            s_prec.append(" ")
            s_rec.append(" ")
            if (NUM_OBJECTIVES == 3):
                s_jac.append(" ")
   
    table_precision.append(s_prec)
    table_recall.append(s_rec)
    table_jaccard_individual.append(s_jac)
    s_prec = []  
    s_rec = []
    s_jac=[]
   
file_all_obj_1.write(tabulate(table_precision,tablefmt="plain"))    
print "File created: *_objective_1_all_run.txt (precision usada)"
file_all_obj_2.write(tabulate(table_recall,tablefmt="plain"))
print "File created: *_objective_2_all_run.txt (recall usado)"
if (NUM_OBJECTIVES == 3):
    file_all_obj_3.write(tabulate(table_recall,tablefmt="plain"))
    print "File created: *_objective_3_all_run.txt (jacard usado)"
  


#print tabulate(table_recall,tablefmt="plain")
  
for f in opened_files:
    f.close()           
# 
file_all_obj_2.close()     
file_all_obj_1.close()   
if (NUM_OBJECTIVES == 3):
    file_all_obj_3.close() 
#===============================================================================
### PARA GLOBAL RECALL  -- POBLACIONAL!!

file_globalRecall = open(path +"/"+ TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_globalRecall_all_run.txt", "w")
  
opened_files = []
for F in globalRecall_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_globRecall = []

table_glogRecall = []

prec=0
rec=1

num_lines = (int(G)*2 ) - 1
 
for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline().strip())
        s_globRecall.append(linea)
   
    table_glogRecall.append(s_globRecall)
    
    s_globRecall = []
   
file_globalRecall.write(tabulate(table_glogRecall,tablefmt="plain"))    

  
print "File created: *_globalRecall_all_run.txt"

  
for f in opened_files:
    f.close()           
 
file_globalRecall.close()    

#===============================================================================
### PARA SIMILITUD DE JACCARD -- POBLACIONAL!!

file_jaccard = open(path+"/" +TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_meanJaccardIndex_all_run.txt", "w")
  
opened_files = []
for F in jaccard_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_jaccard = []

table_jaccard = []

prec=0
rec=1

num_lines = (int(G)*2 ) - 1
 
for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline().strip())
        s_jaccard.append(linea)
   
    table_jaccard.append(s_jaccard)
    
    s_jaccard = []
   
file_jaccard.write(tabulate(table_jaccard,tablefmt="plain"))    

print "File created: *_meanJaccardIndex_all_run.txt"
  
for f in opened_files:
    f.close()           
 
file_jaccard.close()    


 
#===============================================================================
### PARA PRECISION


file_allPrecision = open(path +"/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_precision_all_run.txt", "w")
   
opened_files = []
for F in precision_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_prec = []
table_precision = []

num_lines = int(G) * (int(Pop)+1)

print "num_lines:", num_lines

for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline().strip())  
        if linea != []:
            s_prec.append(linea)            
        else:
            s_prec.append(" ")            
   
    table_precision.append(s_prec)
    s_prec = []  

       
file_allPrecision.write(tabulate(table_precision,tablefmt="plain"))
file_allPrecision.close(
                        )  
print "File created: *_precision_all_run.txt"
  
for f in opened_files:
    f.close()           

 
#===============================================================================
### PARA RECALL


file_allRecall = open(path+"/" +TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_recall_all_run.txt", "w")
   
opened_files = []
for F in recall_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_rec = []
table_recall = []

num_lines = int(G) * (int(Pop)+1)

for x in range(0,num_lines):
    for i in range(0, len(opened_files)):                
        linea = str(opened_files[i].readline())  
        if linea != []:
            s_rec.append(linea)            
        else:
            s_rec.append(" ")            
   
    table_recall.append(s_rec)
    s_rec = []  

       
file_allRecall.write(tabulate(table_recall,tablefmt="plain"))
file_allRecall.close()  
print "File created: *_recall_all_run.txt"
  
for f in opened_files:
    f.close()             

#===============================================================================
### PARA RECALL ENTROPICO


file_allRecallEntropic = open(path +"/"+TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_entropicRecall_all_run.txt", "w")
   
opened_files = []
for F in entropic_recall_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_rec = []
table_recall = []

num_lines = int(G) * (int(Pop)+1)

for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline()) 
        if linea != []:
            s_rec.append(linea)            
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
### PARA PRECISION ENTROPICA


file_allPrecisionEntropic = open(path+"/" +TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_entropicPrecision_all_run.txt", "w")
   
opened_files = []
for F in entropic_precision_files:
    opened_files.append(open(path+"/"+F, "r"))  
   
s_prec = []
table_prec = []

num_lines = int(G) * (int(Pop)+1)

for x in range(0,num_lines):
    for i in range(0, len(opened_files)):        
        linea = str(opened_files[i].readline()) 
        if linea != []:
            s_prec.append(linea)            
        else:
            s_prec.append(" ")            
   
    table_prec.append(s_prec)
    s_prec = []  

       
file_allPrecisionEntropic.write(tabulate(table_prec,tablefmt="plain"))
file_allPrecisionEntropic.close()  
print "File created: *_entropicPrecision_all_run.txt"
  
for f in opened_files:
    f.close()             



#===============================================================================
### PARA JACCARD INDIVIDUAL


file_allIndivJaccard = open(path+"/" +TOPIC +"_"+str(nRuns)+"_"+ objectives +"_"+ nGen+"_"+ popSize+ "_"+ indSize +"_" + cross +"_" + mut +"_individualjaccardIndex_all_run.txt", "w")

opened_files = []
for F in indiv_jaccard_files:
    opened_files.append(open(path+"/"+F, "r"))

s_jac = []
table_jac = []

num_lines = int(G) * (int(Pop)+1)

for x in range(0,num_lines):
    for i in range(0, len(opened_files)):
        linea = str(opened_files[i].readline())
        if linea != []:
            s_jac.append(linea)
        else:
            s_jac.append(" ")

    table_jac.append(s_jac)
    s_jac = []


file_allIndivJaccard.write(tabulate(table_jac,tablefmt="plain"))
file_allIndivJaccard.close()
print "File created: *_individualjaccardIndex_all_run.txt"

for f in opened_files:
    f.close()

