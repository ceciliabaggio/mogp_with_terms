'''
Created on May 13, 2016

@author: cecilia
'''

""" 
Por cada archivo:
*_EVALUATION_globalRecall: ya es el promedio de la generacion
*_EVALUATION_meanJaccardIndex: ya es el promedio de la generacion
*_EVALUATION_fitness: contiene precision a 10 y Recall de cada individuo 
de la Gen

Recuperar los datos - hacer el promedio y almacenar en archivos correspondientes

"""
import os
import numpy as np
import tabulate
import sys

dir_from = str(sys.argv[1])

#dir_from="/home/cecilia/Desktop/Corridas_JAIIO/lucene_10000_docs/Cross(0.7)_Mut(0.03)/N100/Co2/295/"


#file_from = open(dir_from, "r")
file_fitness = []
file_jaccard = []
file_globalrecall = []

for dirs in os.walk(dir_from):    
    for d in dirs[2]:
        #print d.split("_")[-5:]
        if (d.split("_")[-5:] == ['EVALUATION', 'GEN', '1', '', 'globalRecall.txt']):            
            file_globalrecall.append(d)
        if (d.split("_")[-5:] == ['EVALUATION', 'GEN', '1', '', 'meanJaccardIndex.txt']):            
            file_jaccard.append(d)
        if (d.split("_")[-5:] == ['EVALUATION', 'GEN', '1', '', 'fitness.txt']):            
            file_fitness.append(d)


                        
 
GR = []
Pr = []
JI = [] 
        
#print file_globalrecall

f_mean = open(dir_from + "MEAN_JACCARD_INDEX_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
for f in file_jaccard:
    fi = open(dir_from + f, "r" )
    num = float(str(fi.readline()))
    #print num
    JI.append(num)
    f_mean.write(str(num) + '\n')
    fi.close()
f_mean.close()

f_mean = open(dir_from + "MEAN_PRECISION@10_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
for f in file_fitness:
    fi = open(dir_from + f, "r" )
    temp_array=[]
    for line in fi:
        num = float(str(line).split()[0])
        temp_array.append(num)
    
    f_mean.write(str(np.mean(temp_array)) + '\n')        
    Pr.append(np.mean(temp_array))
    fi.close()    
f_mean.close()    

f_mean = open(dir_from + "MEAN_GLOBAL_RECALL_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
for f in file_globalrecall:
    fi = open(dir_from + f, "r" )
    #print f
    l = str(fi.readline()) 
    num = float(l)
    GR.append(num)
    f_mean.write(str(num) + '\n')    
    #print num
    fi.close()
f_mean.close()
             
#f_mean = open(dir_from + "MEAN_GLOBAL_RECALL_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
#------------------------------ #f_mean.write("mean_globalRecall_ = " + str(GR))
#------------------------------------------------------------------------------ 
#--------------------------------------------------------- temp_table.append(GR)
#-------------------------- f_mean.write(tabulate(temp_table, tablefmt="plain"))
#-------------------------------------------------------- #f_mean.write(str(GR))
#---------------------------------------------------------------- f_mean.close()
#------------------------------------------------------------------------------ 
#----------------------------------------------------------------- temp_table=[]
# f_mean = open(dir_from + "MEAN_JACCARD_INDEX_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
#------------------------------------ #f_mean.write("mean_jaccard_ = "+ str(JI))
#--------------------------------------------------------- temp_table.append(JI)
#-------------------------- f_mean.write(tabulate(temp_table, tablefmt="plain"))
#-------------------------------------------------------- #f_mean.write(str(JI))
#---------------------------------------------------------------- f_mean.close()
#------------------------------------------------------------------------------ 
#----------------------------------------------------------------- temp_table=[]
# f_mean = open(dir_from + "MEAN_PRECISION@10_FROM_TESTING_GEN_1_array_of_mean.txt", "w")
#--------------------------------------------------------- temp_table.append(Pr)
#-------------------------- f_mean.write(tabulate(temp_table, tablefmt="plain"))
#---------------------------------- #f_mean.write("mean_precision_ = "+ str(Pr))
#-------------------------------------------------------- #f_mean.write(str(Pr))
#---------------------------------------------------------------- f_mean.close()
 
 
print "Global Rec", GR 
print  "Global Recision", Pr
print  "Jaccard", JI


 
 
print "Mean Precision Generacion_1 on Testing Set = ", np.mean(Pr)    
print "Mean Jaccard Index Generacion_1 on Testing Set = ", np.mean(JI)    
print "Mean Global Recall Generacion_1 on Testing Set = ", np.mean(GR)    
 
f = open(dir_from + "MEAN_GLOBAL_RECALL_FROM_TESTING_GEN_1.txt", "w")
f.write(str(np.mean(GR)))
f.close()
 
f = open(dir_from + "MEAN_JACCARD_INDEX_FROM_TESTING_GEN_1.txt", "w")
f.write(str(np.mean(JI)))
f.close()
 
f = open(dir_from + "MEAN_PRECISION@10_FROM_TESTING_GEN_1.txt", "w")
f.write(str(np.mean(Pr)))
f.close()
