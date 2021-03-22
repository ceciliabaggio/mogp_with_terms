'''
Created on May 23, 2018

@author: cecilia
'''
from math import log

# fitness function
def precision_q(retrieved_that_are_relevant, retrieved_results):

    if (len(retrieved_results)>0):
        precision = float(len(retrieved_that_are_relevant))/len(retrieved_results)
    else:
        print "No se han recuperado documentos para la consulta realizada"
        precision = 0.0

    return precision

# fitness function
def recall_q(retrieved_that_are_relevant, CANT_DOCS_IN_TOPIC):

    if (CANT_DOCS_IN_TOPIC != 0):
        recall = len(retrieved_that_are_relevant)/float(CANT_DOCS_IN_TOPIC)
    else:
        print "No existen documentos relevantes para la consulta realizada"
        recall = 0.0

    return recall

def F_measure(precision_at_10, recall):
    
    fmeasure = 0.0
    
    if (precision_at_10 != 0 and recall != 0):
         fmeasure = float(2 * (precision_at_10 * recall)/(precision_at_10 + recall))
    
    return fmeasure
  
# uses Natural Log
def inverseEntropy(doc, pop, times_retrieved_relevant_doc):
    
    # pop sometimes is size POPSIZE or POPSIZE + OFFSPRING    
    popsize = len(pop)    
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
        print  "times_retrieved_relevant_doc[%s] = %d" %(doc,
                                        int(times_retrieved_relevant_doc[doc]))

    return result

##fitness function
def entropicRecall_q(retrieved_that_are_relevant, CANT_DOCS_IN_TOPIC, pop, 
                                                times_retrieved_relevant_doc):
    suma = 0
    for doc in retrieved_that_are_relevant:
        i_entropy = inverseEntropy(doc, pop, times_retrieved_relevant_doc)
        suma=suma + i_entropy

    return float(suma)/float(CANT_DOCS_IN_TOPIC)


def inverseEntropy_AT_10(doc, pop, times_retrieved_relevant_doc_AT_10):

    # pop sometimes is size POPSIZE or POPSIZE + OFFSPRING
    popsize = len(pop)
    result = 0.0
    
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


##fitness function
def entropicPrecision_q(first_10_retrieved, TOPIC_ID, pop, 
                                        times_retrieved_relevant_doc_AT_10):

    # in prec@10 the retrieved and the relevants retrieved are 10 at most
    suma = 0

    # if no docs retrieved, precision = 0.0
    if (len(first_10_retrieved)==0):
        result = 0.0
    else:
        for doc in first_10_retrieved:
            if (doc.getDocTopic() == TOPIC_ID): #es relevante
                i_entropy = inverseEntropy_AT_10(doc.getDocId(), pop, 
                                            times_retrieved_relevant_doc_AT_10)
                suma=suma + i_entropy
        result = float(suma)/float(len(first_10_retrieved))

    return result

##fitness function
def jaccardSimilarity_q(query_i, pop):
    
    # similarty mean of a query against the others. Used as Objective
    suma = 0
    compraciones = 0
    relevantes_query_i = query_i.retrieved_that_are_relevant
    for query_j in pop:        
        if (query_i.id != query_j.id):
            #print "comparando ", query_i.id, " con ", query_j.id
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
        
    # si toda la poblacion es igual - los ids son los mismos porque pasan
    # de gen en gen sin CX            
    if (compraciones==0):
        return 1.0
    # si no, retorna por defecto la cuenta..          
    return float(suma)/compraciones #comparaciones deberia ser: |pop| - 1
