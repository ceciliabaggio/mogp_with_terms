#!/usr/bin/python

'''
Created on May 17, 2017

@author: cecilia
@param popSize
'''

from numpy import loadtxt
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


import sys
import os
import re

'''
Method to take two equally-sized lists and return just the elements which lie 
on the Pareto frontier, sorted into order.
Default behaviour is to find the maximum for both X and Y, but the option is
available to specify maxX = False or maxY = False to find the minimum for either
or both of the parameters.
'''
def pareto_frontier(Xs, Ys, Queries, maxX = True, maxY = True):
    # Sort the list in either ascending or descending order of X
    myList = sorted([[Xs[i], Ys[i]] for i in range(len(Xs))], reverse=maxX)
    # Start the Pareto frontier with the first value in the sorted list
    p_front = [myList[0]]    
    # Loop through the sorted list
    for pair in myList[1:]:
        if maxY:
            if pair[1] >= p_front[-1][1]: # Look for higher values of Y..
                # p_front[-1][1] es el Y del ultimo elemento. seria el que tiene 
                # mayor Y, porque estan ordenados segun X                
                p_front.append(pair) # ...and add them to the Pareto frontier
        else:
            if pair[1] <= p_front[-1][1]: # Look for lower values of Y...
                p_front.append(pair) # ... and add them to the Pareto frontier
    # Turn resulting pairs back into a list of Xs and Ys
    p_frontX = [pair[0] for pair in p_front]
    p_frontY = [pair[1] for pair in p_front]
    return p_frontX, p_frontY, Qs_queries


# Invocacion del script    
if len(sys.argv) == 4:
    popSize = int(sys.argv[1])
    directoryTopic = sys.argv[2]
    combination = str(sys.argv[3])
    print ("popSize = ", popSize)
    print ("directoryTopic = ", directoryTopic)
    print ("combination = ", combination)
    
    
else:
    print ("debe ingresar el numero de individuos de la poblacion y el \
directorio de donde leer")
    print (" ")
    print ("Ejemplo: python \
pareto_PRECISION_RECALL.py 100 /home/Cecilia/workspace/.../Co5/215/")
    sys.exit()
    
#por cada topico, entro al directorio y levantar precision_all_run y 
#recall_all_run y ya se generan los frentes de las 5 corridas
files = os.listdir(directoryTopic)
for filename in files:    
    m = re.split('_', filename)
    
    if "_precision_all_run.txt" in filename:
        base = filename[:-21]
        print (base)
        filename_prec = directoryTopic+ filename
        #filename_save_prec_rec_queries = open(directoryTopic + base + 
        #                            "queries_pareto_Pr-Rec_last_gen.txt", "w")
        
    elif "_recall_all_run.txt" in filename: #is_substring
        base = filename[:-18]
        print (base)
        filename_rec = directoryTopic +  filename
    #elif  "_queries.txt" in filename: #is_substring
        #base = filename[:-11]
        #print base
        #filename_q = directoryTopic + filename
                        
print ('\n',filename_prec)
print (filename_rec)


#filename_prec = directoryTopic + '215_5_Prec@10-EntropicRecall-Jaccard_\
#nGen(150)_popSize(100)_indSize(XX)_cross(0.7)_mut(0.03)_precision_all_run.txt'

#levanto el archivo de precisiones x corrida
lines = loadtxt(filename_prec, unpack=False)
#me quedo con la ultima generacion
first_gen_precision = lines[0:popSize] 
#la cantidad de corridas es la cant de columnas
nRuns = len(first_gen_precision[1])  

#print last_gen_precision
#print "nRuns = ", nRuns

#filename_rec = directoryTopic + '215_5_Prec@10-EntropicRecall-Jaccard_\
#nGen(150)_popSize(100)_indSize(XX)_cross(0.7)_mut(0.03)_recall_all_run.txt'
#levanto el archivo de recall x corrida
lines = loadtxt(filename_rec, unpack=False)
#me quedo con la ultima generacion
first_gen_recall = lines[0:popSize] 
#la cantidad de corridas es la cant de columnas de alguna lista (fila)
nRuns = len(first_gen_recall[1])  


#print last_gen_recall
#print "nRuns = ", nRuns
Qs_queries = []
for run in range(0,nRuns):
    print ("RUN = ", run+1)
    fig = plt.figure()
    
    filename_save_prec_rec_points = open(directoryTopic + base + 
                                             "points_Pr-Rec_first_gen_run_" +
                                              str(run+1) +".txt", "w")
    filename_save_prec_rec_pareto = open(directoryTopic + base + 
                                             "pareto_Pr-Rec_first_gen_run_" +
                                              str(run+1) +".txt", "w")
        
    Xs_precision = [fila[run] for fila in first_gen_precision]
        
    #print 'precision = ', Xs_precision
    
    Ys_recall = [fila[run] for fila in first_gen_recall]
        
    #print  'recall = ', Ys_recall
    
    p_front_Xs, p_front_Ys, p_front_Qs= pareto_frontier(Xs_precision, 
                                        Ys_recall, Qs_queries, True, True) 
                                        #Qs_queries unused por ahora
    
    print ("Frente de Pareto:")
    for i in range(0, len(p_front_Xs)):
        #print p_front_Xs[i] , p_front_Ys[i]
        filename_save_prec_rec_pareto.write(str(p_front_Xs[i]) + "\t" + str(p_front_Ys[i]) + "\n")
        
    for i in range(0, len(Xs_precision)):
        filename_save_prec_rec_points.write(str(Xs_precision[i]) + "\t" +
                                              str(Ys_recall[i]) + "\n")
    
    ''' las queries no las guardo porque dependen del numero de corrida, 
    no existe queries_all_info.txt. Dado el nro de corrida, habria que 
    buscar la que corresponde'''
            
    #for i in range(0, len(p_front_Qs)):
        #filename_save_prec_rec_queries.write(str(p_front_Qs[i]) + "\n")            
                    
    filename_save_prec_rec_pareto.close()
    filename_save_prec_rec_points.close()    
    #filename_save_prec_rec_queries.close()
    
    # for x,y in p_front:
    #    print x,y
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
        
    if (combination in ['1']):                
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='#007FAE', marker = 'o', s=65, linewidths = 1, alpha=0.5, facecolor = '#007FAE', label= 'Co1')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#007FAE')
    elif (combination in ['2']):
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='#00BDBD', marker = 'd', s=65,linewidths = 1,alpha=0.5, facecolor = '#00BDBD', label= 'Co2')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#00BDBD')
    elif (combination in ['3']):
        # Plot a scatter graph of all results
        #plt.scatter(Xs_precision, Ys_recall, c='#FF6600', marker = '<', s=65,linewidths = 1, alpha=0.5, facecolor = '#FF6600', label= 'Initial Population')
        plt.scatter(Xs_precision, Ys_recall, c='#FF6600', marker = '<', s=65,linewidths = 1, alpha=0.5, facecolor = '#FF6600', label= 'Co3')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#FF6600')
    elif (combination in ['4']):
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='#8BAD00', marker = 's', s=65, linewidths = 1, alpha=0.5, facecolor = '#8BAD00', label= 'Co4')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#8BAD00')            
    elif (combination in ['5']):            
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='#7F3300', marker = r'$\clubsuit$', s=65, linewidths = 1, alpha=0.5, facecolor = '#7F3300', label= 'Co5')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#7F3300' )
    elif (combination in ['6']):            
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='green', marker = 'X', s=65, linewidths = 1, alpha=0.5, facecolor = 'green', label= 'Co6')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='green' )
    elif (combination in ['7']):            
        # Plot a scatter graph of all results
        plt.scatter(Xs_precision, Ys_recall, c='#ff6347', marker = '*' , s=65,linewidths = 1, alpha=0.5, facecolor = '#ff6347', label= 'Co7')
        # Then plot the Pareto frontier on top
        plt.plot(p_front_Xs, p_front_Ys, c='#ff6347')                    
                
                    
     
    plt.axis([0, 1, 0, 1], )
    
    plt.grid(True)
    #plt.legend() 
    plt.legend()
    
    plt.ylabel(r'$$\textit{Recall}$$', fontsize=20)
    plt.xlabel(r'$$\textit{Precisi\'on@10}$$', fontsize=20)
    fig_directory = directoryTopic + base + 'pareto_Pr-Rec_first_gen_run_'+ str(run+1)+'.svg'
    
    print ("fig_dir:", fig_directory)
    
    plt.savefig(fig_directory)
    #plt.show()    
        

