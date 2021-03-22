'''
Created on Jun 15, 2016

@author: cecilia
'''

from os import walk
import shutil
from random import randint
#shutil.copy2('/dir/file.ext', '/new/dir/newname.ext')

topics = []
for num in range(0,20):
    topics.append(randint(0,448))

dir_de_contextos = '/home/cecilia/workspace/MOGP_local/DMOZ@monster-usr-work-DMOZ-Sets/context/'
dir_dmoz =  '/home/cecilia/workspace/MOGP_local/DMOZ@monster-usr-work-DMOZ-Sets/'
dir_destino = '/home/cecilia/workspace/MOGP_local_1/topics_2/'

"""cargo todos los archivos de contextos en f_list """
f_list = []
for (dirpath, dirnames, filenames) in walk(dir_de_contextos):
    f_list.extend(filenames)
   
print f_list
print len(f_list)

selected = []
"""numero al azar que corresponde a la posicion del contexto en la lista """
for num in range(0,20):
    posicion = randint(0,448)
    shutil.copy2(dir_de_contextos + f_list[posicion], dir_destino + f_list[posicion])
    selected.append(f_list[posicion])
    print "topic selected = ", f_list[posicion]
    
"""copio url de los seleccionados """
topico = open(dir_destino + 'topics.topics', 'w')


for doc in selected:
    num = doc.split(".") [0]
    print num
    with open(dir_dmoz + "topics6S.txt", 'r') as origen:
        data = origen.readlines()
    
        for line in data:
            words = line.split()
            if (words[0] == num):
                print words
                topico.write(words[0] + "\t" + words[1] + "\n")   
    
topico.close()
origen.close()

        
