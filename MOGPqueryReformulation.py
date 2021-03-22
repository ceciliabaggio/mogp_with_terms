'''
Created on Mar 6, 2018

@author: cecilia

@param nRun:
@param nGen:
@param popSize:
@param objectiveCombination:
@param seed:
@param topicId:
@param p_crossover:
@param p_mutac:
@param runDirectory:

'''

import random
import re
import os
import sys

from sets import Set
from tabulate import tabulate

from deap import base
from deap import creator
from deap import tools
from deap import gp


import phrase_pool
import fitness_functions

from index import SearchFiles
from datetime import datetime
import performance_metrics

from random import randint

from multiprocessing.dummy import Pool as ThreadPool 
from functools import partial  

#from plot_single_tree import plot

def time_starting(texto):
    print datetime.now(), texto
    return datetime.now()
  
def time_finishing(t, texto):
    delta = datetime.now() - t
    print delta, texto

debug=True

INDEX_DIR = "mogp_with_terms/index/Set12_utf8_term.index"

#===============================================================================
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "                 CHANGE DATASET TO SET 12                   "
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
#===============================================================================

#INDEX_DIR = "mogp_with_terms/index/Set3_utf8_term.index"



print "***********************************************"
print "*     Multi Objective Genetic Programming     *"
print "*      Web Mining Research Group @ DCIC       *"
print "***********************************************"


RUN_NUMBER = str(sys.argv[1])
NGEN = int(sys.argv[2])
POPSIZE = int(sys.argv[3])
OBJ_COMBINATION = sys.argv[4]
SEED = int(sys.argv[5])
TOPIC = str(sys.argv[6])
TOPIC_ID = TOPIC.split(".")[0]
CXPB= float(sys.argv[7])
MUTPB = float(sys.argv[8])
SAVE_DIR = str(sys.argv[9])
OVERLAPPED_ENTITIES=int(sys.argv[10])

IND_SIZE = "XX" # No usado en GP - dado por el tamanio de la expresion

sys.path.insert(0, os.getcwd())

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

pool = phrase_pool.phrase_pool()

#Extract the SPOTS from the tagged XML of the topic description
topic_desc_terms = pool.getTopicDescriptionTerms("index/topics/"+TOPIC_ID+".txt")

print "Terms from topic description = ",topic_desc_terms

OBJ_NUMBER = 0

if (str(OBJ_COMBINATION) == '1'): #Co1
    OBJ_NUMBER = 2
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+"_prec@10-Recall_nGen("+\
            str(NGEN)+")_popSize("+str(POPSIZE)+")_indSize("+str(IND_SIZE)+\
            ")_cross("+ str(CXPB)+")_mut(" +str(MUTPB)+")_seed(" +str(SEED)
elif (str(OBJ_COMBINATION) == '2'): #Co2
    OBJ_NUMBER = 2
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+"_prec@10-EntropicRecall_nGen("+\
            str(NGEN)+")_popSize("+str(POPSIZE)+")_indSize("+str(IND_SIZE)+\
            ")_cross("+str(CXPB)+")_mut(" +str(MUTPB)+")_seed(" +str(SEED)
elif (str(OBJ_COMBINATION) == '3'): #Co3
    OBJ_NUMBER = 2
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+\
            "_EntropicPrec@10-EntropicRecall_nGen("+ str(NGEN)+")_popSize("+\
            str(POPSIZE)+")_indSize("+str(IND_SIZE)+")_cross("+str(CXPB)+\
            ")_mut(" +str(MUTPB)+")_seed(" +str(SEED)
elif (str(OBJ_COMBINATION) == '4'): #Co4
    OBJ_NUMBER = 3
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+\
            "_Prec@10-Recall-Jaccard_nGen("+ str(NGEN)+")_popSize("+\
            str(POPSIZE)+")_indSize("+str(IND_SIZE)+")_cross("+str(CXPB)+\
            ")_mut(" +str(MUTPB)+")_seed(" +str(SEED)
elif (str(OBJ_COMBINATION) == '5'): #Co5
    OBJ_NUMBER = 3
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+\
            "_Prec@10-EntropicRecall-Jaccard_nGen("+ str(NGEN)+")_popSize("+\
            str(POPSIZE)+")_indSize("+str(IND_SIZE)+")_cross("+str(CXPB)+\
            ")_mut(" +str(MUTPB)+")_seed(" +str(SEED)
elif (str(OBJ_COMBINATION) == '6'): #Co6
    OBJ_NUMBER = 2
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+\
            "_Prec@10-Jaccard_nGen("+ str(NGEN)+")_popSize("+\
            str(POPSIZE)+")_indSize("+str(IND_SIZE)+")_cross("+str(CXPB)+\
            ")_mut(" +str(MUTPB)+")_seed(" +str(SEED)

elif (str(OBJ_COMBINATION) == '7'): #Co7
    OBJ_NUMBER = 3
    ruta=SAVE_DIR+"/"+TOPIC_ID+"_"+RUN_NUMBER+\
            "_Prec@10-Jaccard-MaxDocs_nGen("+ str(NGEN)+")_popSize("+\
            str(POPSIZE)+")_indSize("+str(IND_SIZE)+")_cross("+str(CXPB)+\
            ")_mut(" +str(MUTPB)+")_seed(" +str(SEED)

file_fitness_url = ruta+")_fitness.txt"
#file_allQueryInfo_url = ruta+")_all_info.txt"
file_queries_url = ruta+")_queries.txt"
#===============================================================================
# file_pareto_url = ruta+")_paretoFront_best_of_evolution.txt"
# file_pareto_last_gen_url = ruta+")_paretoFront_last_gen.txt"
# file_pareto_first_gen_url = ruta+")_paretoFront_first_gen.txt"
#===============================================================================
file_globalRecall_url = ruta+")_globalRecall.txt"
file_retrieved_that_are_relevant_url = ruta+")_relevantRetrievedDocs.txt"
file_jaccard_index_url= ruta+")_meanJaccardIndex.txt"
file_queries_last_gen_url= ruta+")_queries_last_gen.txt"
file_queries_first_gen_url= ruta+")_queries_first_gen.txt"
file_precision_url = ruta + ")_precision.txt"
file_entropic_precision_url = ruta + ")_entropicPrecision.txt"
file_recall_url = ruta + ")_recall.txt"
file_entropic_recall_url = ruta + ")_entropicRecall.txt"
file_jaccard_index_indiv_url=ruta + ")_Indiv_JaccardIndex.txt"
file_globalRecall_sets_url = ruta + ")_globalRecall_sets.txt"
file_height_url = ruta + ")_height_in_evolution.txt"
file_fmeasure_url = ruta + ")_fmeasure.txt"

file_globalRecall_sets = open(file_globalRecall_sets_url, "w") 
file_queries = open(file_queries_url, "w")

#===============================================================================
# file_paretoFront_best_of_evol = open(file_pareto_url, "w")
# file_pareto_last_gen  = open(file_pareto_last_gen_url, "w")
# file_pareto_first_gen = open(file_pareto_first_gen_url, "w")
#===============================================================================


file_fitness = open(file_fitness_url, "w")
file_queries_last_gen = open(file_queries_last_gen_url, 'w')
file_queries_first_gen = open(file_queries_first_gen_url, 'w')
file_precision = open(file_precision_url, "w")
file_entropic_precision = open(file_entropic_precision_url, "w")
file_recall = open(file_recall_url, "w")
file_entropic_recall = open(file_entropic_recall_url, "w")
file_jaccard_index_indiv = open(file_jaccard_index_indiv_url, "w")
file_height = open(file_height_url, "w")
file_fmeasure = open(file_fmeasure_url, "w")

file_fmeasure.close()
file_height.close()
file_queries_last_gen.close()
file_queries_first_gen.close()
file_queries.close()
file_fitness.close()
file_precision.close()
file_entropic_precision.close()
file_recall.close()
file_entropic_recall.close()
file_jaccard_index_indiv.close()
file_globalRecall_sets.close()

#file_allQueryInfo = open(file_allQueryInfo_url, "w")
#file_allQueryInfo.close()

print 'SAVING DIRECTORY: ',SAVE_DIR
print 'TOPIC: ',TOPIC
print 'IND SIZE: ' ,IND_SIZE
print 'NGEN: ', NGEN
print 'POPSIZE: ', POPSIZE
print 'SEED: ', SEED
print 'CXPB: ', CXPB
print 'MUTPB: ', MUTPB

# Stores the last dir created to be retrieved then from bash for next run
file_lastDirCreated = open(os.getcwd() +"/last_dir_created", "w")
file_lastDirCreated.write(SAVE_DIR)
file_lastDirCreated.close()

#===============================================================================
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "                 CHANGE DATASET TO SET 12                   "
# relevants_per_topic = open("index/Set3.txt", "r")
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
# print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
#===============================================================================

relevants_per_topic = open("index/Set12.txt", "r")

# maxNodes that ever lived
maxNodes = 0

# maxHeight that ever lived
maxHeight = 0

# Maximum height permitted
heightLimit = 17

# number of cores for paralell exec
num_workers = 4

# Retrieves num of relevant docs in the chosen TOPIC_ID
CANT_DOCS_IN_TOPIC = 0
for line in relevants_per_topic:
    
    line = re.sub(r"[^a-zA-Z0-9 ]", "", line) # Removes /n
    num = line.split(" ")
    if (num[0] == TOPIC_ID):
        CANT_DOCS_IN_TOPIC = num[1]


if OVERLAPPED_ENTITIES:
    ###########################################################################
    ### A medida que se recuperan documentos se agregan al diccionario si no estaban

    print "hacer"

    ###########################################################################
else:

    #===========================================================================
    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # print "                 CHANGE DATASET TO SET 12                   "
    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # file_relevant_docs = open("index/relevantes_por_topico_Set3/"+ TOPIC, "r")
    #===========================================================================
    
    file_relevant_docs = open("index/relevantes_por_topico_Set12/"+ TOPIC, "r")
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


# Operators. Return Lucene's expected syntax
# example query = "'sun' OR ('orbit the Sun' AND ('Sun' AND 'Solar System'))"
# From https://lucene.apache.org/core/2_9_4/queryparsersyntax.html
def AND(spot1, spot2):
    return  '(' + spot1 + ' AND '+ spot2 + ')'

def OR(spot1, spot2):
    return '(' + spot1 + ' OR ' + spot2 + ')'

""" en Lucene el NOT es binario: diferencia de conjuntos"""
def NOT(spot1, spot2):
    return '(' + spot1 + ' NOT '+ spot2 + ')'

# Strongly Typed GP
pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
#pset.addPrimitive(AND,[str, str], str)
pset.addPrimitive(OR,[str, str], str)
#pset.addPrimitive(NOT,[str, str], str)

# For mutation the pset only has terminals
mut_pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)

# Terminals from topic description
temp_terms_set= Set([])

# used once for topic description 
def set_terms_as_terminal(): 
    
    global temp_terms_set   
    global mut_pset
    global pset  
    
    for s in temp_terms_set:
        pset.addTerminal(s, str)        
        mut_pset.addTerminal(s, str)        
   

# for PSET and MUTPSET are different because MUT does not need operators        
def replacePrimitiveSet():
    
    global temp_terms_set
    global pset
    
    del pset
    
    pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
    #pset.addPrimitive(AND,[str, str], str)
    pset.addPrimitive(OR,[str, str], str)
    #pset.addPrimitive(NOT,[str, str], str)
    
    for s in temp_terms_set:
        pset.addTerminal(s, str)  
    
    return pset
        
def replaceMutationPrimitiveSet():
    
    global temp_terms_set
    global mut_pset
    
    del mut_pset
    
    mut_pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
    
    for s in temp_terms_set:
        mut_pset.addTerminal(s, str)  
    
    return mut_pset

# weights: list that represents the number and sign of objectives
if (str(OBJ_COMBINATION) == '1') | (str(OBJ_COMBINATION) == '2') | (str(OBJ_COMBINATION) == '3'):
    print "2 objectives selected for maximization"
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,1.0))
elif (str(OBJ_COMBINATION) == '4') | (str(OBJ_COMBINATION) == '5'): # Co4 - Co5 con 3 obj
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,1.0,-1.0))
    print "3 objectives selected: 2 for max - 1 for min (Jaccard Index)"
elif (str(OBJ_COMBINATION) == '6'):
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0))
    print "2 objectives selected: 1 for max - 1 for min (Jaccard Index)"
elif (str(OBJ_COMBINATION) == '7'): # Co7 con 3 objetivos
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,-1.0,1.0))
    print "3 objectives selected: 2 for max - 1 for min (Jaccard Index)"

# retrieved_that_are_relevant: set that contains only the numbers of the docs
# that are relevant (belong to the topic)
# since DAL version:
# like Spots, Entities ,...
creator.create("Individual", 
               gp.PrimitiveTree, 
               fitness=creator.FitnessMulti,
               pset=pset, 
               number_retrieved_docs=int, 
               retrieved_that_are_relevant=Set,
               id=int, numb_of_terms_and_operands=int, 
               precision=float,
               recall=float,
               entropic_recall=float,
               entropic_precision=float,
               jaccard_index_indiv=float,
               father_1=int,
               father_2=int,
               mutated=int,
               first_10_retrieved=list,
               query=str,
               fmeasure=float)

# Attribute generator
toolbox = base.Toolbox()
# Lucene accepts at most 1024 clauses (internal nodes) --> height 9
# COMPLETE binary tree= 2^(h+1) - 1 ---> 2^10 -1 = 1023 NODES, not clause 
toolbox.register("expresion", gp.genHalfAndHalf, pset=pset, min_=1, max_=5)

# genHalfAndHalf: Generate an expression with a PrimitiveSet pset.
# Half the time, the expression is generated with genGrow(), the other half,
# the expression is generated with genFull().
toolbox.register("individual", tools.initIterate, creator.Individual,
                toolbox.expresion)

toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)



def areOverlapped(doc, topicEntities):
    
    entities=doc.getDocEntities()
    #print entities[1:10]
    overlap = [e for e in entities if e in topicEntities]
    #overlap = list(set(doc.getDocEntities()).intersection(set(topicEntities)))

    #if len(overlap):
    #    print "doc: ", doc.getDocId(), " of topic: ", doc.getDocTopic()
    #    print "entities in common: ", len(overlap)
    return len(overlap) > 0
#===============================================================================
# 
# def calculateRelevantsRetrieved_overlapping(retrieved_results):
#     """ Relevant Documents are those that have AT LEAST one entity in common
#     with the Topic Description or SEED"""
#     
#     global temp_terms_set
#     
#     retrieved_that_are_relevant = Set([])
#     relevant_docs = [doc for doc in retrieved_results if areOverlapped(doc,topic_desc_entity_set)]
# 
#     for r in relevant_docs:
#         retrieved_that_are_relevant.add(r.getDocId())
#         #set_terms_as_terminal(r.getDocSpots())
#         temp_terms_set.update(r.getDocEntities())
# 
#     return retrieved_that_are_relevant
#===============================================================================


def calculateRelevantsRetrieved(retrieved_results, TOPIC_ID):
    
    global temp_terms_set
    
    retrieved_that_are_relevant = Set([])

    relevants=[result_doc for result_doc in retrieved_results if result_doc.getDocTopic() == TOPIC_ID]
    #print "# Relevants: ", len(relevants)
    for r in relevants:
        retrieved_that_are_relevant.add(r.getDocId())
        #set_terms_as_terminal(r.getDocSpots())
        temp_terms_set.update(r.getDocTerms())
                
    return retrieved_that_are_relevant


def getRelevantsFrom10(retrieved_results_at_10, TOPIC_ID):
    relevants_from_10 = Set([])
    for result_doc in retrieved_results_at_10:
        if (result_doc.getDocTopic() == TOPIC_ID):
            relevants_from_10.add(result_doc.getDocId())
    return relevants_from_10


# Set the times a relevant doc has been retrieved by the pop
def setTimesRetrievedRelevantDoc(pop):
    global times_retrieved_relevant_doc
    global times_retrieved_relevant_doc_AT_10
    
    for i in pop:               
        
        for doc in i.retrieved_that_are_relevant:            
            times_retrieved_relevant_doc[doc]= 1 + int(times_retrieved_relevant_doc[doc])

        for result_doc in i.first_10_retrieved:
            if (result_doc.getDocTopic()==TOPIC_ID):
                times_retrieved_relevant_doc_AT_10[result_doc.getDocId()]= 1+ \
                int(times_retrieved_relevant_doc_AT_10[result_doc.getDocId()])
    return


# Performs the Evaluetion sending query to Lucene
def evaluate_query(individual, searcher, analyzer, info): 
    
    global maxNodes
    global maxHeight
    
    #print individual
    # Transform the tree expression to functional Python code - infix notation
    # the replace is for escaped quotes

    individual.query =  (toolbox.compile(individual)).replace('$#$','\\"')
    
    nodes = len(individual)
    #print "nodes: ", nodes
    
    height = getHeight(individual)
    #print "height: ", height
    
    # max Nodes that ever lived
    if maxNodes < nodes: 
        maxNodes= nodes  
    
    # max Height that ever lived
    if maxHeight < height: 
        maxHeight = height    
    
    # plot trees in pdf 
    #if getHeight(individual) > 3:
        #import plot_single_tree as pt
        #pt.plot(individual, str("tree_"+str(individual.id)+".pdf"))
    info = info + "\nheight " + str(height)
    retrieved_results = SearchFiles.searchWithLucene(searcher, analyzer, individual.query, info)
    
    
    length_retrieved_results = len(retrieved_results)

    #Los resultados devueltos por lucene, ya son una lista de <result>
    retrieved_results_at_10 = retrieved_results[0:10]   

    ## NEW @Ddal - comentar para usar la version vieja de MOGP
    if OVERLAPPED_ENTITIES:
        # retrieved_that_are_relevant = calculateRelevantsRetrieved_overlapping(
        #                            retrieved_results)
        print "Retrieved with overlapped entities: "
    else:
        retrieved_that_are_relevant = calculateRelevantsRetrieved(retrieved_results,
                                                              TOPIC_ID)

    retrieved_that_are_relevant_at_10=getRelevantsFrom10(retrieved_results_at_10
                                                           , TOPIC_ID)
    print "@@@@@@@ temp_terms_set ", len(temp_terms_set)
    print "\n"
    
    precision_at_10 = fitness_functions.precision_q(
                                            retrieved_that_are_relevant_at_10,
                                            retrieved_results_at_10)

    recall = fitness_functions.recall_q(retrieved_that_are_relevant, 
                                        CANT_DOCS_IN_TOPIC)

    fmeasure = fitness_functions.F_measure(precision_at_10, recall)
    
    return precision_at_10,recall,retrieved_results_at_10,retrieved_that_are_relevant, length_retrieved_results, fmeasure

# deprecated
def getHeight(individual):
    
    return individual.height

### Operator registering ###

toolbox.register("evaluate", evaluate_query)
toolbox.register("select_NSGA2", tools.selNSGA2)

# Crossover & Mutation


#many crossovers may in fact reduce to simply swapping two leaves. 
#To counter this, Koza ( 1992) suggested the widely used approach of choosing 
#functions 90% of the time and leaves 10% of the time.
#toolbox.register("mate", gp.cxOnePointLeafBiased)
toolbox.register("mate", gp.cxOnePoint)

# Replaces a leaf by a tree with height 0
toolbox.register("create_new_leaf", gp.genFull, min_=0, max_=0)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.create_new_leaf, pset=mut_pset)

# option 2
#toolbox.register("mutate", gp.mutEphemeral, mode="one")

# Decorate Crossover & Mutation
toolbox.decorate("mutate", gp.staticLimit(key=getHeight, max_value=17))
#toolbox.decorate("mutate", gp.staticLimit(key=len, max_value=180))
toolbox.decorate("mate", gp.staticLimit(key=getHeight, max_value=17))
#toolbox.decorate("mate", gp.staticLimit(key=len, max_value=180))

toolbox.register("select_parents", tools.selDoubleTournament)
#toolbox.register("select_parents", tools.selTournament)


def search(i, num_q, gen_number, searcher, analyzer):
    
    i.id = num_q
    
    debug=False
    if debug:   
        print "%%%%%% QUERY  ",num_q," GEN=",gen_number," RUN= ",RUN_NUMBER
    info =  "%%%%%% GEN=" + str(gen_number) + " RUN= " + str(RUN_NUMBER)
    
    temp=toolbox.evaluate(i, searcher, analyzer, info)
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
    
    # save the results in each individual
    i.precision = temp[0]
    i.recall = temp[1]
    #i.entropic_recall = 0.0
    i.fmeasure = temp[5]
    
    return


# Evaluates only INDIVIDUAL metrics that not depends on the population
# Linke precision a 10 - recall
def eval_and_calculate_individual_fitness(invalid_ind, num_q, gen_number, 
                                          searcher, analyzer):
    global num_workers
    
    # @param invalid_ind: list that has individuals not being evaluated yet
    # @param num_q: ID of last generated to be continue
  
    t1 = time_starting("start parallelism of GEN " + str(gen_number))
     
    # Make the Pool of workers
    pool = ThreadPool(num_workers) 
       
    function = partial(search, num_q=num_q, gen_number=gen_number, searcher=searcher, analyzer=analyzer)
    invalid_ind = pool.map(function, invalid_ind)
    
    # close the pool and wait for the work to finish 
    pool.close() 
    pool.join() 
    
    time_finishing(t1, "finishing paralelism of GEN " + str(gen_number) + "\n")

    #===========================================================================
    # t1 = time_starting("start sequential GEN " + str(gen_number))
    # # Using sequential For-loop
    # for i in invalid_ind:
    #      
    #     search(i, num_q, gen_number, searcher, analyzer)
    #      
    # time_finishing(t1, "finishing sequential GEN " + str(gen_number))    
    #===========================================================================
    
    return 

def eval_poblational(i, popu):
    
    global times_retrieved_relevant_doc_AT_10
    global times_retrieved_relevant_doc
    
    i.entropic_recall = fitness_functions.entropicRecall_q(
                                    i.retrieved_that_are_relevant,                                        
                                    CANT_DOCS_IN_TOPIC,
                                    popu,
                                    times_retrieved_relevant_doc)

    i.entropic_precision = fitness_functions.entropicPrecision_q(
                                    i.first_10_retrieved,
                                    TOPIC_ID,
                                    popu,
                                    times_retrieved_relevant_doc_AT_10)

    i.jaccard_index = 0.0

    if (str(OBJ_COMBINATION) == '4') | (str(OBJ_COMBINATION) == '5') | (str(OBJ_COMBINATION) == '6') | (str(OBJ_COMBINATION) == '7') :
        i.jaccard_index_indiv = fitness_functions.jaccardSimilarity_q(
                                                        i,
                                                        popu)

    # Fitness loaded based on the objectives selected
    if (str(OBJ_COMBINATION) == '1'):
        i.fitness.values = (i.precision, i.recall)
    elif (str(OBJ_COMBINATION) == '2'):
        i.fitness.values = (i.precision, i.entropic_recall)
    elif (str(OBJ_COMBINATION) == '3'):
        i.fitness.values = (i.entropic_precision, i.entropic_recall)
    elif (str(OBJ_COMBINATION) == '4'):
        i.fitness.values = (i.precision, i.entropic_recall,
                            i.jaccard_index_indiv)
    elif (str(OBJ_COMBINATION) == '5'):
        i.fitness.values = (i.precision, i.recall, i.jaccard_index_indiv)
    elif (str(OBJ_COMBINATION) == '6'):
        i.fitness.values = (i.precision, i.jaccard_index_indiv)
    elif (str(OBJ_COMBINATION) == '7'):
        i.fitness.values = (i.precision, i.jaccard_index_indiv,
                            i.number_retrieved_docs)
    
    return


# Evaluate the POBLATIONAL metrics: entropic precision/recall and Jaccard
def eval_and_calculate_poblational_fitness(pop, gen_number):
    
    global num_workers
    
    t1 = time_starting("start GLOBAL parallelism of GEN " + str(gen_number))
     
    #for i in pop:
    #    eval_poblational(i, pop)
    
    
      
    # Make the Pool of workers
    pool = ThreadPool(num_workers)
     
    function = partial(eval_poblational, popu=pop)
    pop = pool.map(function, pop)
           
    # close the pool and wait for the work to finish 
    pool.close() 
    pool.join() 
      
    time_finishing(t1, "finishing GLOBAL parallelism of GEN " + str(gen_number) + "\n")
    
    
    #===============================================================================
    #     
    #         
    #     for i in invalid_ind + pop:
    # 
    #         i.entropic_recall = fitness_functions.entropicRecall_q(
    #                                         i.retrieved_that_are_relevant,                                        
    #                                         CANT_DOCS_IN_TOPIC,
    #                                         invalid_ind + pop,
    #                                         times_retrieved_relevant_doc)
    # 
    #         i.entropic_precision = fitness_functions.entropicPrecision_q(
    #                                         i.first_10_retrieved,
    #                                         TOPIC_ID,
    #                                         invalid_ind + pop,
    #                                         times_retrieved_relevant_doc_AT_10)
    # 
    #         i.jaccard_index = 0.0
    # 
    #         if (str(OBJ_COMBINATION) == '4') | (str(OBJ_COMBINATION) == '5') | (str(OBJ_COMBINATION) == '6') | (str(OBJ_COMBINATION) == '7') :
    #             i.jaccard_index_indiv = fitness_functions.jaccardSimilarity_q(
    #                                                             i,
    #                                                             invalid_ind + pop)
    # 
    #         # Fitness loaded based on the objectives selected
    #         if (str(OBJ_COMBINATION) == '1'):
    #             i.fitness.values = (i.precision, i.recall)
    #         elif (str(OBJ_COMBINATION) == '2'):
    #             i.fitness.values = (i.precision, i.entropic_recall)
    #         elif (str(OBJ_COMBINATION) == '3'):
    #             i.fitness.values = (i.entropic_precision, i.entropic_recall)
    #         elif (str(OBJ_COMBINATION) == '4'):
    #             i.fitness.values = (i.precision, i.entropic_recall,
    #                                 i.jaccard_index_indiv)
    #         elif (str(OBJ_COMBINATION) == '5'):
    #             i.fitness.values = (i.precision, i.recall, i.jaccard_index_indiv)
    #         elif (str(OBJ_COMBINATION) == '6'):
    #             i.fitness.values = (i.precision, i.jaccard_index_indiv)
    #         elif (str(OBJ_COMBINATION) == '7'):
    #             i.fitness.values = (i.precision, i.jaccard_index_indiv,
    #                                 i.number_retrieved_docs)
    #===============================================================================

    return

def pruneHeight(ind):
    
    global heightLimit    
    
    try: 
        temp = toolbox.clone(ind)
        if getHeight(ind) > heightLimit:
            print "VIOLATING HEIGHT = ", getHeight(ind)
            
            while (getHeight(ind)>= heightLimit):
                # replace tree by random subtree (left or right)
                print "replacing tree " 
                #print temp1                                
                slice1 = ind.searchSubtree(randint(1, 2))
                # find the root                                
                slice2 = ind.searchSubtree(0)                                
                ind[slice2] = ind[slice1]
                
                print "slice of tree ",  ind
                
        del temp
        
    except Exception as error:

        print "\n"
        print('Caught: ' + repr(error))
        print "could not replace individual that violated height"
        
        #restore
        ind = temp
                              
    return ind

def mate_and_mutate(population, offsp_size, cxpb, mutpb):
    
    assert (cxpb + mutpb) <= 1.0, ("The sum of the crossover and mutation "
    "probabilities must be smaller or equal to 1.0.")
    
    offspring = []
    for _ in xrange(offsp_size):
        # random.random() chooses between 0 and 1
        op_choice = random.random()
        if op_choice < cxpb:            # Apply crossover            
            ind1, ind2 = map(toolbox.clone, toolbox.select_parents(population, 
                            k=2, fitness_size=10, parsimony_size=1.3, 
                            fitness_first=False))
            print "selected for CX"
            print "ind 1 = ", ind1
            print "ind 2 = ", ind2            
            ind1, ind2 = toolbox.mate(ind1, ind2)
            del ind1.fitness.values
            offspring.append(ind1)
        elif op_choice < cxpb + mutpb:  # Apply mutation

            ind = toolbox.clone(random.choice(population))
            print "selected for MUT"
            print "ind = ", ind
            ind, = toolbox.mutate(ind)
            print "new = ", ind
            del ind.fitness.values
            offspring.append(ind)
        else:                           # Apply reproduction
            offspring.append(random.choice(population))
    
    return offspring


def main():
    
    global pset
    global mut_pset
    global temp_terms_set
    global maxNodes
    global maxHeight
    global heightLimit
    global times_retrieved_relevant_doc
    global times_retrieved_relevant_doc_AT_10
    
    
    start = datetime.now()
    
    random.seed(SEED)

    # Terminals from topic description
    temp_terms_set.update(topic_desc_terms)
    
    set_terms_as_terminal()    
        
    # First population (random)
    pop = toolbox.population(n=POPSIZE)
    
    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]

    searcher, analyzer = SearchFiles.createAnalyzer(INDEX_DIR)

    #num_q mantiene un numero correlativo de los IDs de las consultas
    num_q = 0
    
    eval_and_calculate_individual_fitness(invalid_ind, num_q, 0, 
                                            searcher, analyzer)
    setTimesRetrievedRelevantDoc(invalid_ind)
    eval_and_calculate_poblational_fitness(invalid_ind, 0)
    
    # After the gen is evaluated are added to pset from temp_terms_set
    set_terms_as_terminal()
        
    if len(temp_terms_set)>10000:        
        temp_terms_set = set(random.sample(temp_terms_set, 10000))
        print "DELETING RANDOM TERMS ---------------------------------------------- NOW: ", len(temp_terms_set)
        pset = replacePrimitiveSet()
        mut_pset = replaceMutationPrimitiveSet()    

    # Assign the crowding distance to the indiv. No actual selection is done
    pop[:] = toolbox.select_NSGA2(invalid_ind, len(pop))

    #table_allQueryInfo = []
    table_fitness = []
    table_queries = []
    table_globalrecall = []
    table_retrieved_that_are_relevant=[]
    table_meanJaccard = []
    table_queries_last_gen = []
    table_queries_first_gen = []
    table_precision =[]
    table_entropic_precision=[]
    table_recall=[]
    table_entropic_recall=[]
    table_jaccard_indiv=[]
    table_height = []
    table_fmeasure = []
    
    # Save in separate file the queries from 1st gen - for testing
    
    file_queries_first_gen = open(file_queries_first_gen_url, 'w')
    for i in pop:        
        #print  q.__class__
        #q = q.encode('utf-8') # Unicode => ASCII       
         
        #table_queries_first_gen.append([str(i).encode('ascii', 'ignore')])
        table_queries_first_gen.append([str(i).replace("u'\"", "'\"")]) 
    file_queries_first_gen.write((tabulate(table_queries_first_gen, 
                                                    tablefmt="plain")))
    del table_queries_first_gen
    file_queries_first_gen.close()

    # Eliminates Lucene Analyzer to start clean another gen
    #SearchFiles.eliminateAnalyzer(searcher, analyzer)

    # Begin the generational process
    for gen in range(1, NGEN+1):
        
        print "##############################   GEN = ", gen, " ##############"
        
        # Creates Lucene Analyzer to start clean another gen
        #searcher, analyzer = SearchFiles.createAnalyzer(INDEX_DIR)

        for index, i in enumerate(pop):
                                    
            table_retrieved_that_are_relevant.append(
                                        [str(sorted(i.retrieved_that_are_relevant))])
            #table_queries.append([str(i.query.encode('utf-8'))])
            table_queries.append([str(i).replace("u'\"", "'\"")])
            if (OBJ_NUMBER)==2:
                table_fitness.append([str(i.fitness.values[0]) ,
                                      str(i.fitness.values[1])])
            else: # more than 2 objectives
                table_fitness.append([str(i.fitness.values[0]),
                                      str(i.fitness.values[1]),
                                      str(i.fitness.values[2])])
            table_precision.append([str(i.precision)])
            table_recall.append([str(i.recall)])
            table_entropic_precision.append([str(i.entropic_precision)])
            table_entropic_recall.append([str(i.entropic_recall)])
            table_jaccard_indiv.append([str(i.jaccard_index_indiv)])
            table_fmeasure.append([str(i.fmeasure)])
            try:
                table_height.append([getHeight(i)])
            except:
                if (len(i)==1):
                    table_height.append([str(0)])
                else:
                    table_height.append([str(sys.maxint)])

        # Save in separate file the queries from Last gen - for testing
        if gen==NGEN:
            file_queries_last_gen = open(file_queries_last_gen_url, 'w')
            for i in pop:
                table_queries_last_gen.append([str(i).replace("u'\"", "'\"")])
            file_queries_last_gen.write((tabulate(table_queries_last_gen, 
                                                            tablefmt="plain")))
            file_queries_last_gen.close()

        # Calculate Performance metric - GLobal Recall
        global_recall =  performance_metrics.calculateGlobalRecall(
                                                    pop, 
                                                    CANT_DOCS_IN_TOPIC,
                                                    file_globalRecall_sets_url)        

        table_globalrecall.append([str(global_recall)])
        table_globalrecall.append([" "])
        table_queries.append([" "])
        table_height.append([" "])

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
        
        # Calculate Performance metric - Jaccard Index
        mean_jaccard_index = performance_metrics.calculateMeanJaccardIndex(pop, 
                                                                        POPSIZE)

        table_meanJaccard.append([str(mean_jaccard_index)])
        table_meanJaccard.append([" "])

        file_queries = open(file_queries_url, "a+")
        file_fitness = open(file_fitness_url, "a+")
        file_globalRecall = open(file_globalRecall_url, "a+")
        file_retrieved_that_are_relevant = open(
                                    file_retrieved_that_are_relevant_url, "a+")
        file_jaccard_index=open(file_jaccard_index_url, "a+")
        file_precision = open(file_precision_url, "a+")
        file_entropic_precision = open(file_entropic_precision_url, "a+")
        file_recall = open(file_recall_url, "a+")
        file_entropic_recall = open(file_entropic_recall_url, "a+")
        file_jaccard_index_indiv= open(file_jaccard_index_indiv_url, "a+")        
        file_height = open(file_height_url, "a+")
        file_fmeasure = open(file_fmeasure_url, "a+")
        
        # Concat current gen in each file
        file_queries.write(tabulate(table_queries, tablefmt="plain"))
        file_fitness.write(tabulate(table_fitness,tablefmt="plain"))
        file_globalRecall.write(tabulate(table_globalrecall, tablefmt="plain"))
        file_jaccard_index.write(tabulate(table_meanJaccard, tablefmt="plain"))
        file_retrieved_that_are_relevant.write(tabulate(
                        table_retrieved_that_are_relevant, tablefmt="plain"))
        file_precision.write(tabulate(table_precision, tablefmt="plain"))
        file_recall.write(tabulate(table_recall, tablefmt="plain"))
        file_entropic_precision.write(tabulate(table_entropic_precision, 
                                                            tablefmt="plain"))
        file_entropic_recall.write(tabulate(table_entropic_recall, 
                                                            tablefmt="plain"))
        file_jaccard_index_indiv.write(tabulate(table_jaccard_indiv, 
                                                            tablefmt="plain"))
        file_height.write(tabulate(table_height, tablefmt="plain"))
        file_fmeasure.write(tabulate(table_fmeasure, tablefmt="plain"))
        
        file_fmeasure.close()
        file_height.close()
        file_retrieved_that_are_relevant.close()
        file_jaccard_index.close()
        file_globalRecall.close()
        file_queries.close()
        file_fitness.close()
        file_precision.close()
        file_entropic_precision.close()
        file_recall.close()
        file_entropic_recall.close()
        file_jaccard_index_indiv.close()
        
        table_fmeasure = []
        table_height = []
        table_fitness = []
        table_queries = []
        table_globalrecall = []
        table_retrieved_that_are_relevant=[]
        table_meanJaccard = []
        table_queries_last_gen = []       
        table_precision =[]
        table_entropic_precision=[]
        table_recall=[]
        table_entropic_recall=[]
        table_jaccard_indiv=[]

        table_meanJaccard.append([" "])
        table_globalrecall.append([" "])
        table_queries.append([" "])
        table_height.append([" "])
        table_fmeasure.append([" "])
        
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
        
        # Apply crossover and mutation on the population
        # returned in a new list of offsprings
        offspring = mate_and_mutate(pop, POPSIZE, CXPB, MUTPB)
        
        print "start offsping prune"        
        offspring = list(map(pruneHeight, offspring))        
        print "end offsping prune"
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        
        # reset to 0 the times a doc is retrieved by population
        resetTimesRetrievedRelevantDoc(times_retrieved_relevant_doc)
        resetTimesRetrievedRelevantDoc(times_retrieved_relevant_doc_AT_10)
        
        # Calculate individual & global metrics
        eval_and_calculate_individual_fitness(invalid_ind, 
                                            num_q, gen, searcher, analyzer)
        setTimesRetrievedRelevantDoc(offspring + pop)
        eval_and_calculate_poblational_fitness(offspring + pop, gen)

        # Select the next generation population
        pop[:] = toolbox.select_NSGA2(offspring + pop, POPSIZE)

        # Eliminates Lucene Analyzer to start clean another gen
        #SearchFiles.eliminateAnalyzer(searcher, analyzer)
        
        # After the gen is evaluated are added to pset from temp_terms_set
        set_terms_as_terminal()
            
        if len(temp_terms_set)>10000:                    
            temp_terms_set = set(random.sample(temp_terms_set, 10000))
            print "DELETING RANDOM TERMS --------------------------------------- NOW: ", len(temp_terms_set)
            pset = replacePrimitiveSet()
            mut_pset = replaceMutationPrimitiveSet()    
    # Eliminates Lucene Analyzer to start clean another gen
    SearchFiles.eliminateAnalyzer(searcher, analyzer)                
    print "END OF EVOLUTION"
    print "maximum nodes ever lived: ", maxNodes
    print "maximum height ever lived: ", maxHeight
    duration = datetime.now() - start
    print "Duration of evolution: ", duration




if __name__ == "__main__":

    main()

