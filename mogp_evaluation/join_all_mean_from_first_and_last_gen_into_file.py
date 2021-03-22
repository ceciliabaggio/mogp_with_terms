'''
Created on Dec 14, 2016

@author: cecilia
'''
import sys, os

dir_from = str(sys.argv[1])
f_GR_gen_1 = open(dir_from + "_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt", "w")
f_PR_gen_1 = open(dir_from + "_MEAN_PRECISION@10_FROM_TESTING_ALL_TOPICS_GEN_1.txt", "w")
f_JI_gen_1 = open(dir_from + "_MEAN_JACCARD_INDEX_FROM_TESTING_ALL_TOPICS_GEN_1.txt", "w")

f_GR_gen_last = open(dir_from + "_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt", "w")
f_PR_gen_last = open(dir_from + "_MEAN_PRECISION@10_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt", "w")
f_JI_gen_last = open(dir_from + "_MEAN_JACCARD_INDEX_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt", "w")

topicos=[]
for base, dirs, files in os.walk(dir_from):
    if(dirs != []): #obtengo la lista de directorios(topicos) que contienen los archivos
        dirs.sort()
        topicos=dirs

print topicos
print len(topicos), " topicos"


for i in range(0,len(topicos)):
    for base, dirs, files in os.walk(dir_from+"/"+topicos[i]): #entro a cada topico
        print len(files), "archivos en topico: ", topicos[i]
        for f in files:
            #MEAN_GLOBAL_RECALL_FROM_TESTING_GEN_1.txt
            nombre = f.split("_")[-6:]
            if nombre == ['GLOBAL', 'RECALL', 'FROM', 'TESTING', 'GEN', '1.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_GR_gen_1.write(str(archivo.readline())+ "\n")
                archivo.close()
                
                
            elif nombre == ['GLOBAL', 'RECALL', 'FROM', 'TESTING', 'GEN', 'LAST.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_GR_gen_last.write(str(archivo.readline())+ "\n")
                archivo.close()
                
                
            elif nombre == ['JACCARD', 'INDEX', 'FROM', 'TESTING', 'GEN', '1.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_JI_gen_1.write(str(archivo.readline())+ "\n")
                archivo.close()
                
            elif nombre == ['JACCARD', 'INDEX', 'FROM', 'TESTING', 'GEN', 'LAST.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_JI_gen_last.write(str(archivo.readline())+ "\n")
                archivo.close()
                
            elif nombre == ['MEAN', 'PRECISION@10', 'FROM', 'TESTING', 'GEN', '1.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_PR_gen_1.write(str(archivo.readline())+ "\n")
                archivo.close()
                
            elif nombre == ['MEAN', 'PRECISION@10', 'FROM', 'TESTING', 'GEN', 'LAST.txt']:
                archivo = open(dir_from+"/"+topicos[i]+"/"+f, "r")
                f_PR_gen_last.write(str(archivo.readline())+ "\n")
                archivo.close()
                

f_GR_gen_1.close()
f_GR_gen_last.close()   
f_JI_gen_1.close()
f_JI_gen_last.close()
f_PR_gen_1.close()
f_PR_gen_last.close()

