
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
from matplotlib import rc
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)

#font = {'family' : 'normal',
#        'weight' : 'bold',
#        'size'   : 20}

#rc('font', **font)

global lgd


def plot_avgAvgAvgPrecision_at_10(directory, combination):
    
    global lgd    
    
    print ("plotting: ",directory)
    print ("combination", combination)
    
    # Get a list of all folders in this folder --> TOPICS    
    
    topic_folders = os.listdir(directory)
    topic_folders.sort()
    
    print (topic_folders)
    print (len(topic_folders))
    
    topic_number = 0
    
    for topic in topic_folders:
        #topic = topic_folders[0]
        subfolder = os.listdir(directory + str(topic) + '/')
        
        # seleccionar los archivos _precision_all_run.txt de cada topico
        # en cada topico deberia haber uno solo, reune todas las precisiones        
        file_all_run = fnmatch.filter(subfolder, '*_recall_all_run.txt')[0]
        print (file_all_run)
        
        name = file_all_run.split('_')
        
        nRuns = int(name[1])
        nGen = int(((name[3]).split('(')[1]).split(')')[0])        
        popSize =  int(((name[4]).split('(')[1]).split(')')[0])
        print ("ngen: ", nGen)
        print ("popsize: ",popSize)
        
        objectives = name[2]
        print (objectives)
        
        lines = loadtxt(directory + str(topic) + '/' + file_all_run, unpack=False)
        print (lines)
        columns =  len(lines[0])
        rows = len(lines)
        
        print ("filas",rows, "colus", columns)
        
        avgPrecision_gen_by_run = np.zeros((nGen, nRuns))  
            
        # por cada columna
        for r in range (0, nRuns):
            base = 0
            for g in range(0,nGen):                
                top = base + popSize - 1       
                avgPrecision_gen_by_run[g,r] = np.mean(lines[base:top, r], dtype=np.float)
                base+=popSize
        
        print ("generaciones X corridas \n"       )
        print (avgPrecision_gen_by_run)
    
        avgAvgPrecision_by_gen_all_run = np.zeros(nGen)
        
        for gen in range(0,nGen):
            avgAvgPrecision_by_gen_all_run[gen] = np.mean(avgPrecision_gen_by_run[gen,:])
        
        print ("Precision de cada generacion en TODAS las corridas \n")
        print (avgAvgPrecision_by_gen_all_run)
        
        if (topic_number == 0): 
            #creo el arreglo cuando analizo el topico 0, para saber el nGen
            avgAvgAvgPrecision_Gen_x_Topic = np.zeros((nGen, len(topic_folders)))
            
            avgAvgAvgPrecision_Gen_x_Topic[:,topic_number] = avgAvgPrecision_by_gen_all_run[:]
        else:
            avgAvgAvgPrecision_Gen_x_Topic[:,topic_number] = avgAvgPrecision_by_gen_all_run[:]
        
        print ("precision generacion x topico")
        print (avgAvgAvgPrecision_Gen_x_Topic)    
        topic_number+=1
    
    #===========================================================================
    # """ Usando desvio estandar, formulita de Ana"""
    # Array_std = np.zeros(nGen);
    # 
    # for gen in range(0,nGen):
    #     #desvio estandar
    #     desvio = np.std(avgPrecision_gen_by_run[gen,:])
    #     print desvio
    #     Array_std[gen] =  desvio * 1.96 / math.sqrt(nRuns)
    #  
    # x = [i in range(0,nGen)] 
    # y = avgAvgPrecision_by_gen_all_run[:]
    #===========================================================================
    
    x = [i for i in range(0,nGen)]         
    
    #M_TopicxGen = avgAvgAvgPrecision_Gen_x_Topic.transpose()
    
    #list_of_mean: cada indice es una generacion. Promedio sobre todos los topicos
    
    list_of_mean = np.zeros(nGen)
    for g in range(0, nGen):
        
        list_of_mean[g] = np.mean(avgAvgAvgPrecision_Gen_x_Topic[g,:])
    
    print (len(list_of_mean))
    print (len(x))
    print (x)

    if (combination == 1):                
        plt.scatter(x[0::5], list_of_mean[0::5], c='#007FAE', marker = 'o', linewidth = 0.7, label= 'Co1', alpha=0.7)
        plt.plot(x, list_of_mean, c='#007FAE', linewidth = 0.7)       
    elif (combination == 2):                
        plt.scatter(x[0::5], list_of_mean[0::5], c='#00BDBD', marker = 'd',  linewidth = 0.7, label= 'Co2', alpha=0.7)
        plt.plot(x, list_of_mean, c='#00BDBD', linewidth = 0.7)          
    elif (combination == 3):
        plt.scatter(x[0::5], list_of_mean[0::5], c='#FF6600', marker = '<',  linewidth = 0.7, label= 'Co3', alpha=0.7)
        plt.plot(x, list_of_mean, c='#FF6600', linewidth = 0.7)
    elif (combination == 4):
        plt.scatter(x[0::5], list_of_mean[0::5], c='#8BAD00', marker = 's',  linewidth = 0.7, label= 'Co4', alpha=0.7)
        plt.plot(x, list_of_mean, c='#8BAD00', linewidth = 0.7)                
    elif (combination == 5):            
        plt.scatter(x[0::5], list_of_mean[0::5], c='#7F3300', marker =  r'$\clubsuit$' ,  linewidth = 0.7, label= 'Co5', alpha=0.7)        
        plt.plot(x, list_of_mean, c='#7F3300', linewidth = 0.7)
    elif (combination == 6):            
        plt.scatter(x[0::5], list_of_mean[0::5], c='green', marker = 'X' ,  linewidth = 0.7, label= 'Co6', alpha=0.7)    
        plt.plot(x, list_of_mean, c='green', linewidth = 0.7)         
    elif (combination == 7):            
        plt.scatter(x[0::5], list_of_mean[0::5], c='tomato', marker = '*' ,  linewidth = 0.7, label= 'Co7', alpha=0.7)    
        plt.plot(x, list_of_mean, c='tomato', linewidth = 0.7)         
        
        
    ax.axis([0, 150, 0, 1])    
    
    #plt.gca().set_ylim(bottom=0)
    
    ax.grid('on')    
    # Major ticks every 20, minor ticks every 5
    major_ticks = np.arange(0, 150, 20)
    minor_ticks = np.arange(0, 150, 5)
    
    ax.set_xticks(major_ticks)
    ax.set_xticks(minor_ticks, minor=True)
    
    major_ticks = np.arange(0, 1, 0.2)
    minor_ticks = np.arange(0, 1, 0.05)
    ax.set_yticks(major_ticks)
    ax.set_yticks(minor_ticks, minor=True)
     
    # # And a corresponding grid
    ax.grid(which='both')
    
    # Or if you want different settings for the grids:
    ax.grid(which='minor', alpha=0.2)
    ax.grid(which='major', alpha=0.5)
    
    #ax.legend((l2, l4), ('oscillatory', 'damped'), loc='upper right', shadow=True)


    # puede funcionar
    lgd = ax.legend(loc='center right', bbox_to_anchor=(1.18, 0.7), 
          ncol=1, fancybox=True, shadow=True)

    # Set the legend font size
    plt.rc('legend', fontsize=14)
        
    # Set the font size of xticks
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    
    #plt.legend(loc='upper center',
    #      ncol=1, fancybox=True, shadow=True)          
        
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')  
    plt.xlabel(r'$$\textit{Generations}$$', fontsize=20)
    plt.ylabel(r'$$\overline{\overline{\textit{Recall}}}$$', fontsize=20)
     
             
    return

# Invocacion del script    
if len(sys.argv) == 9:
    
    combinations_dir = []
    combinations_dir.append(str(sys.argv[1]))
    combinations_dir.append(str(sys.argv[2]))
    combinations_dir.append(str(sys.argv[3]))
    combinations_dir.append(str(sys.argv[4]))
    combinations_dir.append(str(sys.argv[5]))
    combinations_dir.append(str(sys.argv[6]))
    combinations_dir.append(str(sys.argv[7]))
    
    save_dir = str(sys.argv[8])
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    
    for i in range(0, len(combinations_dir)):
        if combinations_dir[i]:        
            plot_avgAvgAvgPrecision_at_10(combinations_dir[i], i+1)
                
    
    #plt.savefig(save_dir + "evolution_Recall-terms.svg" , bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.savefig(save_dir + "evolution_Recall-concepts.svg" , bbox_extra_artists=(lgd,), bbox_inches='tight')
    #plt.show()
                  
else:
    print ("debe ingresar los directorios de donde leer y el dir donde GUARDAR FIGURAS")
    print (" ")
    print ("Ejemplo: python plot_avgAvgAvgPrecision_at_10_Co1_Co2_Co3_Co4_Co5_Co6 \
    /home/.../Co1/ /home/.../Co2/  ... <SAVE_DIR>")
    print ('Si alguna combinacion no esta, ingresar "" (cadena vacia) en su lugar ' )

    sys.exit()
    

    
