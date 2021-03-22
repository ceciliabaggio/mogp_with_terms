'''
Created on May 18, 2018

@author: cecilia
'''
import pygraphviz as pgv
from mogp_evaluation import gp_extended
from deap import gp

# installation for requirements.txt
# pygraphviz==1.3.1 
#            --install-option="--include-path=/usr/include/graphviz" 
#            --install-option="--library-path=/usr/lib/graphviz/"

#example: plot(pop[0], "tree.pdf")
def plot(tree_exp, file_to_export="tree.pdf"):

    nodes, edges, labels = gp.graph(tree_exp)

    g = pgv.AGraph()
    g.node_attr['style']='filled'
    g.add_nodes_from(nodes, color="red")
    g.add_edges_from(edges)
    g.layout(prog="dot")
    
    print "number of nodes: ", len(nodes)
    
    for i in nodes:
        n = g.get_node(i)
        n.attr["label"] = labels[i]
        n.attr['color'] = '#FF6600'
        n.attr['fillcolor']="#ffb882"
        

    g.draw(file_to_export)
    
def AND(spot1, spot2):
    return  '(' + spot1 + ' AND '+ spot2 + ')'  
  
def OR(spot1, spot2):    
    return '(' + spot1 + ' OR ' + spot2 + ')' 
  
""" en Lucene el NOT es binario: diferencia de conjuntos"""
def NOT(spot1, spot2):
    return '(' + spot1 + ' NOT '+ spot2 + ')'     
        

# Like *_queries_last_gen.txt    
def plotFromFile(query_file):
    
    pset = gp.PrimitiveSetTyped("main",in_types=[], ret_type=str)
    pset.addPrimitive(AND,[str, str], str)
    pset.addPrimitive(OR,[str, str], str)
    pset.addPrimitive(NOT,[str, str], str)

    lines = [line.rstrip('\n') for line in open(query_file, "r")] 
    n=0
    for string_query in lines:                  
        print "original", string_query
        prim_tree = gp_extended.PrimitiveTree.from_string(str(string_query), pset=pset)  
        print gp_extended.PrimitiveTree(prim_tree).height                                      
        plot(prim_tree, "x.tree_"+ str(n)+ ".pdf")
        n+=1     
            
d = '/home/cecilia/repos/mogp_with_spots/runs/mogp_2018-05-18_14-26-24/Co6/529/'
f = '529_1_Prec@10-Jaccard_nGen(5)_popSize(20)_indSize(XX)_cross(0.7)_mut(0.3)_seed(12803)_queries_last_gen.txt'    
d = '/home/cecilia/Desktop/'
f = 'query.txt'        
plotFromFile(d+f) 
 
 