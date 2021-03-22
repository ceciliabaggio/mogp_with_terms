'''
Created on May 23, 2018

@author: cecilia
'''

from sets import Set


# Poblational metrics
# Global_REcall(P,t) = #relevants retrieved by ALL queries/#relevants in topic
def calculateGlobalRecall(POP, CANT_DOCS_IN_TOPIC, file_globalRecall_sets_url):

    relevant_docs_retrieved_in_gen = Set([])

    for ind in POP:
        # to avoid repeated, the relevant retrieved do to a SET
        relevant_docs_retrieved_in_gen.update(ind.retrieved_that_are_relevant)
    #print "Global Recall GEN: ", GEN, " --> ", str(float(len(relevant_docs_retrieved_in_gen)/int(CANT_DOCS_IN_TOPIC)))
    file_globalRecall_sets = open(file_globalRecall_sets_url, "a+")
    file_globalRecall_sets.write(str(sorted(relevant_docs_retrieved_in_gen, key=str.lower)))
    file_globalRecall_sets.write('\n')
    file_globalRecall_sets.close()
    return float(float(len(relevant_docs_retrieved_in_gen))/float(CANT_DOCS_IN_TOPIC))


#Jaccard index: Poblational metric
#measures haw similar are all the queries in pop in terms of retrieved docs
def calculateMeanJaccardIndex(pop, POPSIZE):
    jaccard_index_matrix = [[0.0 for row in range(POPSIZE)] for col in range(POPSIZE)]
    suma=0.0
    # Imprime la matriz de ceros 
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
            # si ambos conjuntos son vacios, la similitud es 1
            if (len(relevantes_query_i)==0) and (len(relevantes_query_j)==0):
                jaccard_index_matrix[i][j]=1
            else:
                jaccard_index_matrix[i][j] = float(len(inter))/float(len(union))

            suma = suma + jaccard_index_matrix[i][j]

    # Imprime la matriz que seria SIMETRICA por eso calcula la mitad
    # print "============================== JACCARD MATRIX ========"

    # for row in range(POPSIZE):
        # print jaccard_index_matrix[row]

    comparaciones = (POPSIZE*(POPSIZE-1))/2

    return float(suma/comparaciones)