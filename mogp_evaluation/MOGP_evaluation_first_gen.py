'''
Created on May 13, 2016

@author: cecilia
'''

import re
import os
import sys
import gc

from sets import Set
from math import log
from tabulate import tabulate

from deap import base
from deap import creator
from deap import tools
from deap import gp

import gp_extended

# Bring index package onto the path
dirname=os.path.dirname
parent_dir= dirname(dirname(os.path.abspath(__file__)))

sys.path.insert(0,parent_dir)
sys.path.append(os.path.abspath(os.path.join('..', 'index')))

from index import SearchFiles
import result

debug=True
INDEX_DIR = "mogp_with_terms/index/Set3_utf8_term.index"

print "***********************************************"
print "*                 EVALUATION                  *"
print "*         Random Queries (1st Gen)            *"
print "*                                             *"
print "*     Multi Objective Genetic Programming     *"
print "*      Web Mining Research Group @ DCIC       *"
print "***********************************************"

SAVE_DIR = str(sys.argv[1])
fileName_queries = str(sys.argv[2])

if not os.path.exists(SAVE_DIR + fileName_queries):
    print "File ", fileName_queries, " not found"
   

file_url = SAVE_DIR + fileName_queries.replace("_queries_first_gen.txt",
                                               "_EVALUATION_GEN_1_")

temp = fileName_queries.split("_")
 
print temp 

if (str(temp[2])== 'prec@10-Recall'):
    COMBINATION = 'Co1'
    OBJ_COMBINATION = 1
    OBJ_NUMBER = 2
    PRECISION_AND_ENTROPIC_RECALL = 0    
elif (str(temp[2])== 'prec@10-EntropicRecall'):       
    COMBINATION = 'Co2'
    OBJ_COMBINATION = 2
    OBJ_NUMBER = 2
    PRECISION_AND_ENTROPIC_RECALL = 1
elif (str(temp[2])== 'EntropicPrec@10-EntropicRecall'):       
    COMBINATION = 'Co3'
    OBJ_COMBINATION = 3
    OBJ_NUMBER = 2
elif (str(temp[2])== 'Prec@10-Recall-Jaccard'):       
    COMBINATION = 'Co4'
    OBJ_COMBINATION = 4
    OBJ_NUMBER = 3
elif (str(temp[2])== 'Prec@10-EntropicRecall-Jaccard'):       
    COMBINATION = 'Co5'
    OBJ_COMBINATION = 5
    OBJ_NUMBER = 3
elif (str(temp[2])== 'Prec@10-Jaccard'):       
    COMBINATION = 'Co6'
    OBJ_COMBINATION = 6
    OBJ_NUMBER = 2
elif (str(temp[2])== 'Prec@10-Jaccard-MaxDocs'):      
    COMBINATION = 'Co7'
    OBJ_COMBINATION = 7
    OBJ_NUMBER = 3     



print "Objective Combination: ", COMBINATION

RUN_NUMBER = str(temp[1])
TOPIC_ID = temp[0]
NGEN =int(str(str(temp[3]).split("(")[1]).split(")")[0])
POPSIZE = int(str(str(temp[4]).split("(")[1]).split(")")[0])

#file_EVAL_queries = open(file_url +"_queries_last_gen.txt", "w")
file_allQueryInfo = open(file_url +"_all_info.txt", "w")
file_entropic_recall=open(file_url+"_entropicRecall.txt", "w")    
file_entropic_precision=open(file_url+"_entropicPrecision.txt", "w")    
file_precision=open(file_url+"_precision.txt", "w")    
file_recall=open(file_url+"_recall.txt", "w")
file_fitness = open(file_url +"_fitness.txt", "w")  
file_globalRecall = open(file_url+"_globalRecall.txt", "w")    
file_retrieved_that_are_relevant = open(file_url+"_relevantRetrievedDocs.txt","w")
file_jaccard_index=open(file_url+"_meanJaccardIndex.txt", "w")    
file_jaccard_index_indiv=open(file_url+"__Indiv_JaccardIndex.txt", "w")


relevants_per_topic = open("index/Set3.txt", "r")

 
''' Recupera la cantidad de docs relevantes en el topico TOPIC_ID'''
CANT_DOCS_IN_TOPIC = 0
for line in relevants_per_topic:
    ''' Elimino los /n  '''    
    line = re.sub(r"[^a-zA-Z0-9 ]", "", line)
    num = line.split(" ")
    if (num[0] == TOPIC_ID): 
        CANT_DOCS_IN_TOPIC = num[1]
        print "relevantes en topico ",TOPIC_ID, ": ",  CANT_DOCS_IN_TOPIC
             

''' 
Diccionario dict = {'doc_id': cant_veces_recuperado}
Para calcular luego el recall Entropico
Cada vez que se recupera un documento relevante, se le suma 1 a la cantidad 
de veces recuperado
Es POR GENERACION. Al terminar una generacion se pone en 0
'''
file_relevant_docs = open("index/relevantes_por_topico_Set3/"+ TOPIC_ID+ ".txt", "r")  
times_retrieved_relevant_doc = {}
times_retrieved_relevant_doc_AT_10 = {}
for line in file_relevant_docs:
    #now each doc Id is the topic and doc number
    line = TOPIC_ID +"_"+line.split(".")[0]     
    #times_retrieved_relevant_doc[line]=0
    times_retrieved_relevant_doc.update({line:0})
    #print times_retrieved_relevant_doc
    times_retrieved_relevant_doc_AT_10.update({line:0})    

docs_retrieved_in_gen = []

def resetTimesRetrievedRelevantDoc(times_retrieved_relevant_doc):
    for k in times_retrieved_relevant_doc.iterkeys():
        times_retrieved_relevant_doc[k] = 0
        
    #print "times_retrieved_relevant_doc= ", times_retrieved_relevant_doc
 

""" OPERADORES: 
nodos internos del arbol. Retornan la sintaxis esperada 
por Lucene, para luego ser evaluada """

#query = "'sun' OR ('orbit the Sun' AND ('Sun' AND 'Solar System'))"

def AND(spot1, spot2):
    return  '(' + spot1 + ' AND '+ spot2 + ')'  
  
def OR(spot1, spot2):    
    return '(' + spot1 + ' OR ' + spot2 + ')' 
  
""" en Lucene el NOT es binario: diferencia de conjuntos"""
def NOT(spot1, spot2):
    return '(' + spot1 + ' NOT '+ spot2 + ')'

"""
VER --> https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
"""

"""Strongly Typed GP"""
pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
pset.addPrimitive(AND,[str, str], str)
pset.addPrimitive(OR,[str, str], str)
pset.addPrimitive(NOT,[str, str], str)
    
    
                             
def set_terms_as_terminals(set_of_terms):
    for t in set_of_terms:
        pset.addTerminal(t, str)    
    #print "NUEVOS TERMINALES: ", set_of_terms
        

if (OBJ_NUMBER==2) and (OBJ_COMBINATION==1 or OBJ_COMBINATION==2
                        or OBJ_COMBINATION==3 ):
    print "2 objectives selected for maximization"
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,1.0))
elif (OBJ_NUMBER==2) and (OBJ_COMBINATION==6):
    print "2 objectives selected 1 for maximization - 1 for minimization"
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
elif((OBJ_NUMBER==3) and (OBJ_COMBINATION==4 or OBJ_COMBINATION==5)): # Co4 - Co5 
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,1.0,-1.0))
    print "3 objectives selected: 2 for maximization - 1 for minimization (Jaccard Index)"
elif (OBJ_NUMBER==3) and (OBJ_COMBINATION==7): #Co7
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0,1.0))
    print "3 objectives selected: 2 for maximization - 1 for minimization (Jaccard Index)"     

#retrieved_that_are_relevant: set that contains only the numbers of the docs
#that are relevant (belong to the topic)
#since DAL version:
#retrieved_docs: list of type <result> now need to store info for each DOC
#like Spots, Entities,...
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMulti, 
            pset=pset, number_retrieved_docs=int, retrieved_that_are_relevant=set, 
            id=int, numb_of_terms_and_operands=int, precision=float, 
            recall=float, entropic_recall=float, entropic_precision=float, 
            jaccard_index_indiv=float, father_1=int, father_2=int, mutated=int,
            first_10_retrieved=list, query=str)

toolbox = base.Toolbox() 
# Attribute generator
toolbox.register("expresion", gp.genHalfAndHalf, pset=pset, min_=1, max_=6)

""" genHalfAndHalf: Generate an expression with a PrimitiveSet pset. 
    Half the time, the expression is generated with genGrow(), the other half, 
    the expression is generated with genFull().
    pset =Primitive set from which primitives are selected.
    min = Minimum height of the produced trees.
    max = Maximum Height of the produced trees. 
    log2 (cant_hojas) = altura ---> para altura=6 tendriamos 64 hojas
    type = The type that should return the tree when called, 
    when None (default) the type of :pset: (pset.ret) is assumed."""
toolbox.register("individual", tools.initIterate, creator.Individual, 
                 toolbox.expresion)

""" A BAG  population is the most commonly used type. It has no particular 
ordering although it is generally implemented using a list.
"""
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
# deap.tools.initRepeat(container, func, n)

toolbox.register("compile", gp.compile, pset=pset)


def precision_q(retrieved_that_are_relevant, retrieved_results, TOPIC_ID):
    
    if (len(retrieved_results)>0):
        precision = float(len(retrieved_that_are_relevant))/len(retrieved_results)        
    else:
        print "No se han recuperado documentos para la consulta realizada"
        precision = 0.0

    #print "retrieved_that_are_relevant = ", len(retrieved_that_are_relevant)
    #print "retrieved_results = ", len(retrieved_results)
    
    return precision 


def recall_q(retrieved_that_are_relevant, CANT_DOCS_IN_TOPIC):
    
    if (CANT_DOCS_IN_TOPIC != None):
        recall = len(retrieved_that_are_relevant)/float(CANT_DOCS_IN_TOPIC)        
    else:
        print "No existen documentos relevantes para la consulta realizada"
        recall = 0.0
            
    return recall
'''
usa LOGARITMO NATURAL PARA LOS CALCULOS
'''
def inverseEntropy(doc, pop): 
    """ depende con que param se llame. pop a veces es de tamanio POPSIZE o
    POPSIZE + OFFSPRING """
    popsize = len(pop)       
    #print "en recall entropico popsize = ", popsize
    result = 0.0
       
    try:
        #print "int(times_retrieved_relevant_doc[doc]) = ",int(times_retrieved_relevant_doc[doc])
        num = log(float((popsize+1))/float(times_retrieved_relevant_doc[doc]))
        #print "num = ", num 
        den = log(float(popsize+1))        
        #print "den = ", den 
        result = num/den 
                    
    except ZeroDivisionError:
        print "No se puede calcular entropia inversa-division por cero:"
        print  "times_retrieved_relevant_doc[%s] = %d" %(doc, int(times_retrieved_relevant_doc[doc]))

    return result    


def entropicRecall_q(retrieved_that_are_relevant,number_of_retrieved_results, 
                     CANT_DOCS_IN_TOPIC, TOPIC_ID, pop):
    suma = 0    
    for doc in retrieved_that_are_relevant:
        i_entropy = inverseEntropy(doc, pop) 
        suma=suma + i_entropy       
    
    #print "suma de entropias", suma
    
    return float(suma)/float(CANT_DOCS_IN_TOPIC)


def inverseEntropy_AT_10(doc, pop): 
    """ depende con que param se llame. pop a veces es de tamanio POPSIZE o
    POPSIZE + OFFSPRING """
    popsize = len(pop)
         
    try:
        #print "int(times_retrieved_relevant_doc[doc]) = ",int(times_retrieved_relevant_doc[doc])
        num = log(float((popsize+1))/float(times_retrieved_relevant_doc_AT_10[doc]))
        #print "num = ", num 
        den = log(float(popsize+1))        
        #print "den = ", den 
        result = num/den 
                    
    except ZeroDivisionError:
        print "No se puede calcular entropia inversa-division por cero:"
        print  "times_retrieved_relevant_doc[%s] = %d" %(doc, 
                                int(times_retrieved_relevant_doc_AT_10[doc]))

    return result    

"""
como en realidad es precision @10, los recuperados, y los relevantes recuperados
son como maximo 10. De forma que la funcion quede generica.
"""
def entropicPrecision_q(first_10_retrieved, 
                     CANT_DOCS_IN_TOPIC, TOPIC_ID, pop):
    suma = 0            
    
    """ Si no se recuperan docs, la precision es 0"""          
    if (len(first_10_retrieved)==0):
        result = 0.0
    else: 
        for doc in first_10_retrieved:
            if (doc.getDocTopic() == TOPIC_ID): #es relevante
                i_entropy = inverseEntropy_AT_10(doc.getDocId(), pop) 
                suma=suma + i_entropy         
        result = float(suma)/float(len(first_10_retrieved))
         
    return result

""" promedio de similitud de una consulta respecto a todas las demas
USADA COMO OBJETIVO"""
def jaccardSimilarity_q(query_i, pop):
    suma = 0
    compraciones = 0
    relevantes_query_i = query_i.retrieved_that_are_relevant
    for query_j in pop:
        if (query_i.id != query_j.id):        
            #print "comparando ", query_i.id, " con ", i.id     
            compraciones = compraciones + 1
            relevantes_query_j = query_j.retrieved_that_are_relevant
            inter = relevantes_query_j.intersection(relevantes_query_i)
            union = relevantes_query_j.union(relevantes_query_i)
            ''' si ambos conjuntos son vacios, la similitud es 1 '''                
            if (len(relevantes_query_j)==0) and (len(relevantes_query_i)==0):
                jaccard_index=1.0
            else:
                jaccard_index = float(len(inter))/float(len(union))
            
            suma = suma + jaccard_index     
    
    
    return float(suma)/compraciones #comparaciones deberia ser: |pop| - 1 

    
'''
Calculates wich from the retrieve docs are relevant for the topic TOPIC_ID
'''
def calculateRelevantsRetrieved(retrieved_results, TOPIC_ID):
    retrieved_that_are_relevant = Set([])
    
    relevants= [result_doc for result_doc in retrieved_results if result_doc.getDocTopic() == TOPIC_ID]
    
    for r in relevants:
        retrieved_that_are_relevant.add(r.getDocId())
        #set_spots_as_terminals(r.getDocSpots())
    
    return retrieved_that_are_relevant 
        

def getRelevantsFrom10(retrieved_results_at_10, TOPIC_ID):
    relevants_from_10 = Set([])
    for result_doc in retrieved_results_at_10:
        if (result_doc.getDocTopic() == TOPIC_ID):
            relevants_from_10.add(result_doc.getDocId())
            #print "********** relevante de los primeros 10 ="
            #print result_doc.getDocId()
    #if len(relevants_from_10)==0:
        #print "Ninguno relevante recuperado"        
    return relevants_from_10

"""
setea la cantidad de veces que un documento fue recuperado en una poblacion 
"""
def setTimesRetrievedRelevantDoc(pop):
    for i in pop:
        for doc in i.retrieved_that_are_relevant:
            times_retrieved_relevant_doc[doc]= 1 + \
                int(times_retrieved_relevant_doc[doc])                 
    
        for result_doc in i.first_10_retrieved:              
            if (result_doc.getDocTopic()==TOPIC_ID):
                times_retrieved_relevant_doc_AT_10[result_doc.getDocId()]= 1+ \
                int(times_retrieved_relevant_doc_AT_10[result_doc.getDocId()])    
    return
  
'''
Evalua la expresion (individuo) segun PRECISION Y RECALL y luego calcula 
el RECALL ENTROPICO
'''
def evaluate_query(individual, searcher, analyzer):
    
    
    print individual
    
    
    #Transform the tree expression to functional Python code - infix notation     
    individual.query =  toolbox.compile(individual)
    
    #print individual.query
       
    retrieved_results = SearchFiles.searchWithLucene_evaluation(searcher, analyzer, individual.query)
    
    length_retrieved_results = len(retrieved_results)
    
    #Los resultados devueltos por lucene, ya son una lista de <result>    
    retrieved_results_at_10 = retrieved_results[0:10]
    
    ## NEW @Ddal - comentar para usar la version vieja de MOGP
    #retrieved_overlapped_entities=getDocsWithOverlappingEntities(retrieved_results) 
    ##
    #print "Retrieved with overlapped entities: ", len(retrieved_overlapped_entities)
    
    retrieved_that_are_relevant=calculateRelevantsRetrieved(retrieved_results, 
                                                              TOPIC_ID)
    retrieved_that_are_relevant_at_10=getRelevantsFrom10(retrieved_results_at_10
                                                           , TOPIC_ID)
    """ 
    - Run the generated routine
    - Ask for retrieved  documents and calculate if they are relevant
    - buscador.search(individual) """    
    precision_at_10 = precision_q(retrieved_that_are_relevant_at_10, 
                                  retrieved_results_at_10, TOPIC_ID)
    
    recall = recall_q(retrieved_that_are_relevant, CANT_DOCS_IN_TOPIC)
    print "\n"
    
    #FREE MEMORY OF NON RELEVANT DOCS
    #del retrieved_results
    gc.collect()
    
    """ The returned value must be an iterable of length equal to the number 
    of objectives (weights). """    
    return precision_at_10,recall,retrieved_results_at_10,retrieved_that_are_relevant, length_retrieved_results


def getHeight(individual):  
    
    return individual.height


""" Operator registering """
#toolbox.register("evaluate_PreRec", eval_Precision_and_Recall)
toolbox.register("evaluate", evaluate_query)
toolbox.register("select_NSGA2", tools.selNSGA2)
toolbox.register("mate", gp.cxOnePoint)


toolbox.register("expr_mut", gp.genGrow, min_=0, max_=0)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

toolbox.decorate("mutate", gp.staticLimit(key=getHeight, max_value=10))
toolbox.decorate("mate", gp.staticLimit(key=getHeight, max_value=10))

#toolbox.decorate("mate", gp.staticLimit(key=OR .attrgetter("height"), max_value=5))
#toolbox.decorate("mutate", gp.staticLimit(key=OR.attrgetter("height"), max_value=5))

""" 
Evalua las metricas que dependen solo de cada individuo, y no tienen en cuenta 
el resto de la poblacion: precision y recall ordinarios
"""
def eval_and_calculate_individual_fitness(invalid_ind, num_q, gen_number, searcher, analyzer):
    """
    Por cada INDIVIDUO generado de la poblacion,
    se evalua precision a 10 - recall 
        
    @param invalid_ind: lista que contiene indiiduos que no han sido evaluados
    @param num_q: el ID de la ultima consulta generada, de modo que sea 
    continuo
     
    """
    
    for i in invalid_ind:        
        i.id = num_q
        if debug:   print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% QUERY  ", num_q        
        temp=toolbox.evaluate(i, searcher, analyzer)
        # temp[0]= precision @ 10
        # temp[1]= recall
        # temp[2]= retrieved_results at 10 (lista de objetos <result>)
        # temp[3]= retrieved_that_are_relevant (conjunto de IDs de Docs)        
        # temp[4]= len(retrieved_results)
                        
        #store the results with the query. New @Dal
        #ver si solo guardo los que tienen una entity en comun con el topico!!!!!!!!!!!!!!!!!!!!!!!!        
        #i.retrieved_docs = temp[2]
        
        i.number_retrieved_docs = temp[4]        
        i.first_10_retrieved = temp[2]
        i.retrieved_that_are_relevant = temp[3]                     
        if (gen_number==-1): # LA POBLACION INICIAL NO TIENE PADRES
            i.father_1 =-1 
            i.father_2 =-1
        
        num_q=num_q + 1                     
        
        i.numb_of_terms_and_operands = len(i)        
        
        '''en cada individuo guardo las 3 metricas,
        independientemente de las usadas como objetivo'''
        i.precision = temp[0]
        i.recall = temp[1]        
        #i.entropic_recall = 0.0    
    return num_q

""" 
Evalua las metricas que dependen de la poblacion a la que pertenece el individ. 
NO solo de cada individuo en si: precision entropica y recall entropica
"""
def eval_and_calculate_poblational_fitness(invalid_ind, pop, num_q, gen_number):
    ''' Por cada individuo, de la POBLACION evaluo el recall entropico & JACCARD 
    ya que son poblacionales! '''     
    for i in invalid_ind + pop:
        
        i.entropic_recall = entropicRecall_q(i.retrieved_that_are_relevant, 
                                           i.number_retrieved_docs, 
                                           CANT_DOCS_IN_TOPIC, TOPIC_ID,
                                           invalid_ind + pop)
        
        i.entropic_precision = entropicPrecision_q(i.first_10_retrieved, 
                                        CANT_DOCS_IN_TOPIC, TOPIC_ID,
                                        invalid_ind + pop)   
         
        i.jaccard_index = 0.0           
        
        if (str(OBJ_COMBINATION) == '4') | (str(OBJ_COMBINATION) == '5') | (str(OBJ_COMBINATION) == '6') | (str(OBJ_COMBINATION) == '7') :
            i.jaccard_index_indiv = jaccardSimilarity_q(i, invalid_ind + pop)
                     
        '''dependiendo del objetivo seleccionado, se carga el fitness''' 
        if (str(OBJ_COMBINATION) == '1'):                    
            i.fitness.values = (i.precision, i.recall)            
        elif (str(OBJ_COMBINATION) == '2'):
            i.fitness.values = (i.precision, i.entropic_recall)
        elif (str(OBJ_COMBINATION) == '3'):
            i.fitness.values = (i.entropic_precision, i.entropic_recall)
        elif (str(OBJ_COMBINATION) == '4'):
            i.fitness.values = (i.precision, i.entropic_recall, i.jaccard_index_indiv)
        elif (str(OBJ_COMBINATION) == '5'):
            i.fitness.values = (i.precision, i.recall, i.jaccard_index_indiv)
        elif (str(OBJ_COMBINATION) == '6'):
            i.fitness.values = (i.precision, i.jaccard_index_indiv)
        elif (str(OBJ_COMBINATION) == '7'):                    
            i.fitness.values = (i.precision, i.jaccard_index_indiv, i.number_retrieved_docs)                                    
                            
    return 0

'''
Metrica poblacional. Calcula el recall Global de una poblacion
Global_REcall(P,t) = numero de docs recuperados por todas las consultas 
(que son relevantes) / nro docs relevantes para el topico
'''
def calculateGlobalRecall(POP, CANT_DOCS_IN_TOPIC, GEN):
    
    relevant_docs_retrieved_in_gen = Set([])
       
    for ind in POP:
        ''' los recuperados que son relevantes de cada consulta van en un Set 
        para evitar repetidos - INTERSECCION '''
        relevant_docs_retrieved_in_gen.update(ind.retrieved_that_are_relevant)      
    #print "Global Recall GEN: ", GEN, " --> ", str(float(len(relevant_docs_retrieved_in_gen)/int(CANT_DOCS_IN_TOPIC)))
    return float(float(len(relevant_docs_retrieved_in_gen))/float(CANT_DOCS_IN_TOPIC))

""" Indice de Jaccard - metrica poblacional
mide que tan similares son las consultas de TODA la poblacion
"""
def calculateMeanJaccardIndex(pop):
    jaccard_index_matrix = [[0.0 for row in range(POPSIZE)] for col in range(POPSIZE)]
    suma=0.0
    '''Imprime la matriz de ceros '''
    #for row in range(POPSIZE):
    #    print jaccard_index_matrix[row]
        
    for i in range(0, POPSIZE):
        #En la diagonal, lo que recupera cada consulta es similar a si misma
        jaccard_index_matrix[i][i]=1
        for j in range(i+1, POPSIZE):
            relevantes_query_i = pop[i].retrieved_that_are_relevant
            relevantes_query_j = pop[j].retrieved_that_are_relevant
            
            inter = relevantes_query_i.intersection(relevantes_query_j)
            union = relevantes_query_i.union(relevantes_query_j)
            ''' si ambos conjuntos son vacios, la similitud es 1 '''                
            if (len(relevantes_query_i)==0) and (len(relevantes_query_j)==0):
                jaccard_index_matrix[i][j]=1
            else:
                jaccard_index_matrix[i][j] = float(len(inter))/float(len(union))
            
            suma = suma + jaccard_index_matrix[i][j]     
            
    comparaciones = (POPSIZE*(POPSIZE-1))/2    
                    
    return float(suma/comparaciones)


def main():    
       
    pop = []
    #with open(SAVE_DIR + fileName_queries, "r") as ins:
    lines = [line.rstrip('\n') for line in open(SAVE_DIR + fileName_queries, "r")] 

    for query in lines:                  
        prim_tree = gp_extended.PrimitiveTree.from_string(str(query), pset=pset)       
        i = creator.Individual(prim_tree)                     
        pop.append(i)
        
 
    searcher, analyzer = SearchFiles.createAnalyzer(INDEX_DIR)
    
    #num_q mantiene un numero correlativo de los IDs de las consultas
    num_q = 0           
    num_q = eval_and_calculate_individual_fitness(pop, num_q,-1, searcher, analyzer)
    setTimesRetrievedRelevantDoc(pop)
   
    
    eval_and_calculate_poblational_fitness(pop, [], num_q, 0)
    
    #pop = toolbox.select_NSGA2(pop, len(pop))
    
    table_allQueryInfo = []
    table_fitness = []    
    #table_queries = []    
    table_globalrecall = []
    table_retrieved_that_are_relevant=[]
    table_meanJaccard = []
    table_precision =[]
    table_entropic_precision=[]
    table_recall=[]
    table_entropic_recall=[]
    table_jaccard_indiv=[] 
                            
    for i in pop:
        #ex = toolbox.compile(i)
        #ex = eval(str(i))             
        table_allQueryInfo.append([str(i.id), str(i.precision), 
                           str(i.recall),
                           str(i.entropic_recall), 
                           str(i.numb_of_terms_and_operands),
                           str(int(i.number_retrieved_docs)),
                           str(len(i.retrieved_that_are_relevant)),
                           str(i.father_1), 
                           str(i.father_2),
                           str(i.mutated),
                           str(i.entropic_precision),
                           str(i.jaccard_index_indiv)])#jaccard de c/ind                                            
        table_retrieved_that_are_relevant.append([str(i.retrieved_that_are_relevant)])
        #table_queries.append([str(i)])
        if (OBJ_NUMBER)==2:
            table_fitness.append([str(i.fitness.values[0]) , 
                                  str(i.fitness.values[1])])
        else: #mas de 2 objetivos
            table_fitness.append([str(i.fitness.values[0]), 
                                  str(i.fitness.values[1]),
                                  str(i.fitness.values[2])])
        table_precision.append([str(i.precision)])
        table_recall.append([str(i.recall)])
        table_entropic_precision.append([str(i.entropic_precision)])
        table_entropic_recall.append([str(i.entropic_recall)])                      
        table_jaccard_indiv.append([str(i.jaccard_index_indiv)])               
                   
        
    global_recall =  calculateGlobalRecall(pop, CANT_DOCS_IN_TOPIC, 1)
    mean_jaccard_index = calculateMeanJaccardIndex(pop)
              
    table_meanJaccard.append([str(mean_jaccard_index)])        
    table_meanJaccard.append([" "])       
                    
    ''' Despues se calcula SOLO para la primera y ultima generacion '''
    mean_jaccard_index = calculateMeanJaccardIndex(pop)
          
    table_globalrecall.append([str(global_recall)])
    table_globalrecall.append([" "])                       
    table_allQueryInfo.append([" "," ", " ", " ", " ", " "," ", " "
                               , " ", " ", " ", " "])
    #table_queries.append([" "])
    
    if (OBJ_NUMBER)==2:
        table_fitness.append([ " ", " "])
    else:
        table_fitness.append([ " ", " ", " "])
         
    table_retrieved_that_are_relevant.append([" "])
    table_precision.append([" "])
    table_recall.append([" "])
    table_entropic_precision.append([" "])
    table_entropic_recall.append([" "])       
    table_jaccard_indiv.append([" "])
    
    """ Concatena en cada archivo la generacion actual """
    file_allQueryInfo.write(tabulate(table_allQueryInfo, tablefmt="plain"))
    #file_EVAL_queries.write(tabulate(table_queries, tablefmt="plain"))
    file_fitness.write(tabulate(table_fitness,tablefmt="plain"))
    file_globalRecall.write(tabulate(table_globalrecall, tablefmt="plain"))
    file_jaccard_index.write(tabulate(table_meanJaccard, tablefmt="plain"))
    file_retrieved_that_are_relevant.write(tabulate(table_retrieved_that_are_relevant, tablefmt="plain"))        
    
    file_precision.write(tabulate(table_precision, tablefmt="plain"))
    file_recall.write(tabulate(table_recall, tablefmt="plain"))
    file_entropic_precision.write(tabulate(table_entropic_precision, tablefmt="plain"))
    file_entropic_recall.write(tabulate(table_entropic_recall, tablefmt="plain"))
    file_jaccard_index_indiv.write(tabulate(table_jaccard_indiv, tablefmt="plain"))       
    
    file_retrieved_that_are_relevant.close()
    file_jaccard_index.close()
    file_globalRecall.close()        
    file_allQueryInfo.close()   
    file_fitness.close()
    file_precision.close()
    file_recall.close()
    file_entropic_precision.close()
    file_entropic_recall.close()
    file_jaccard_index_indiv.close()
    
    resetTimesRetrievedRelevantDoc(times_retrieved_relevant_doc)
    resetTimesRetrievedRelevantDoc(times_retrieved_relevant_doc_AT_10)                            
  
    SearchFiles.eliminateAnalyzer(searcher, analyzer)
        
    print "-END OF EVALUATION (first gen)-"

if __name__ == "__main__":
    main()

