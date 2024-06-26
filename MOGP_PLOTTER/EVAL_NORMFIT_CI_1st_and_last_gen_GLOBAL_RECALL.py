'''
Created on Jun 8, 2017

@author: cecilia
'''

import sys
import os
import fnmatch
from numpy import loadtxt
import numpy as np
###
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
# Turn interactive plotting off
plt.ioff()
###

import math
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)




def NORMFIT_CI_1st_and_last_gen_GLOBAL_RECALL(directory):
      
    # Get a list of all folders in this folder --> TOPICS        
    files_in_dir= os.listdir(directory)
    files_in_dir.sort()
    
    if ('Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)
        print (globalRecall_by_topic)        
        mean = np.mean(globalRecall_by_topic)               
        """ Usando desvio estandar -->  FORMULA DE ANA """        
        desvio = np.std(globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))          
        co1_first = plt.errorbar(1, mean, yerr=error,  c='#007FAE', 
                    marker = 'o', linewidth = 1, fillstyle='none', capsize=4, markersize=15)  
                    #capsize: ancho de barras de error

    if ('Co2_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co2_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)
        mean = np.mean(globalRecall_by_topic)            
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))
        co2_first = plt.errorbar(2 , mean, yerr=error, c='#00BDBD', 
                    marker = 'd', linewidth = 1, fillstyle='none', capsize=4, markersize=15)

    if ('Co3_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co3_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))
        co3_first = plt.errorbar(3 , mean, yerr=error, c='#FF6600', 
                    marker = '>', linewidth = 1, fillstyle='none', capsize=4, markersize=15)
        
    if ('Co4_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co4_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co4_first = plt.errorbar(4 , mean, yerr=error,  c='#8BAD00',
                    marker = 's', linewidth = 1, fillstyle='none', capsize=4, markersize=15)
        
    if ('Co5_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co5_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co5_first = plt.errorbar(5 , mean, yerr=error,   c='#7F3300',
                    marker = r'$\clubsuit$', linewidth = 1, fillstyle='none', capsize=4, markersize=15)

    if ('Co6_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co6_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co6_first = plt.errorbar(6 , mean, yerr=error,  c='#006400',        
                    marker = 'X', linewidth = 1, fillstyle='none', capsize=4, markersize=15)
        
    if ('Co7_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co7_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_GEN_1.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co7_first = plt.errorbar(7 , mean, yerr=error,  c='#ff6347',
                    marker = '*', linewidth = 1, fillstyle='none', capsize=4, markersize=15)

    """ PARA PRUEBA """
    #co6_first = plt.errorbar(6 , mean, yerr=error,  c='green', marker = r'$\bowtie$', linewidth = 1,  fillstyle='none', capsize=4, markersize=15)
            
    #===========================================================================
    # LAST_GEN
    #===========================================================================
         
    if ('Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory + 
                    'Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)
        print (globalRecall_by_topic)        
        mean = np.mean(globalRecall_by_topic)               
        """ Usando desvio estandar -->  FORMULA DE ANA """        
        desvio = np.std(globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))          
        co1_last = plt.errorbar(1, mean, yerr=error,  c='#007FAE', 
                    marker = 'o', linewidth = 1, alpha=1, capsize=4, markersize=15)  
                    #capsize: ancho de barras de error

    if ('Co2_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co2_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)
        mean = np.mean(globalRecall_by_topic)            
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))
        co2_last = plt.errorbar(2 , mean, yerr=error, c='#00BDBD', 
                    marker = 'd', linewidth = 1, alpha=1, capsize=4, markersize=15)

    if ('Co3_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co3_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))
        co3_last = plt.errorbar(3 , mean, yerr=error, c='#FF6600', 
                    marker = '>', linewidth = 1, alpha=1, capsize=4, markersize=15)
        
    if ('Co4_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co4_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co4_last = plt.errorbar(4 , mean, yerr=error,  c='#8BAD00',
                    marker = 's', linewidth = 1, alpha=1, capsize=4, markersize=15)
        
    if ('Co5_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co5_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))             
        co5_last = plt.errorbar(5 , mean, yerr=error,   c='#7F3300',
                    marker = r'$\clubsuit$', linewidth = 1, alpha=1, capsize=4, markersize=15)

    if ('Co6_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co6_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))     
        co6_last = plt.errorbar(6 , mean, yerr=error,  c='#006400',
                    marker = 'X', linewidth = 1, alpha=1, capsize=4, markersize=15)
        
    if ('Co7_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt' in files_in_dir):
        globalRecall_by_topic = loadtxt(directory+ 
                    'Co7_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN.txt', 
                    unpack=False)         
        mean = np.mean(globalRecall_by_topic)        
        desvio = np.std(globalRecall_by_topic)
        print (globalRecall_by_topic)
        print (desvio)
        error =  desvio * 1.96 / math.sqrt(len(globalRecall_by_topic))             
        co7_last = plt.errorbar(7 , mean, yerr=error,  c='#ff6347', marker = '*', linewidth = 1, alpha=1, capsize=4, markersize=15)
    """ PARA PRUEBA """
    #co6_last = plt.errorbar(6 , mean, yerr=error,  c='green', marker = r'$\bowtie$', linewidth = 1,  alpha=1, capsize=4, markersize=15)
            
         
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.axis([0, 8, 0, 1])
    plt.grid(True)  
    labels = ['Co1', 'Co2', 'Co3', 'Co4', 'Co5', 'Co6', 'Co7']
    #plt.legend([(co1_first, co1_last), (co2_first, co2_last), 
    #            (co3_first, co3_last), (co4_first, co4_last), 
    #            (co5_first, co5_last), (co6_first, co6_last),
    #            (co7_first, co7_last)], labels)

     # Set the legend font size
    plt.rc('legend', fontsize=14)
        
    # Set the font size of xticks
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)          
    
    plt.xlabel(r'$$\textit{Combinations}$$', fontsize=20)
    plt.ylabel(r'$$\overline{\textit{Global-Recall}}$$', fontsize=20)       
    plt.xticks([1, 2, 3, 4, 5, 6, 7], labels, rotation='horizontal') 
    
    return

# Invocacion del script    
if len(sys.argv) == 2:        
    save_dir= str(sys.argv[1])    
    fig = plt.figure()    
    NORMFIT_CI_1st_and_last_gen_GLOBAL_RECALL(save_dir)                
    plt.savefig(save_dir+ "TESTING_CI_Global_Recall-mixed.svg")
    #plt.show()
                  
else:
    print ("debe ingresar los directorios de donde leer. Debe contener los archivos")
    print ("del tipo Co1_MEAN_GLOBAL_RECALL_FROM_TESTING_ALL_TOPICS_LAST_GEN")
    print (" ")
    print ("Ejemplo: python NORMFIT_CI_1st_and_last_gen_GLOBAL_RECALL \
    </home/cecilia/workspace/MOGP_multiple_op_AND_OR_NOT_results>")
     
    sys.exit()
