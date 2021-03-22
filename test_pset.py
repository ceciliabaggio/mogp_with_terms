'''
Created on May 24, 2018

@author: cecilia
'''

from deap import gp

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
pset.addPrimitive(AND,[str, str], str)
pset.addPrimitive(OR,[str, str], str)
pset.addPrimitive(NOT,[str, str], str)

pset.addTerminal("pepe", str)

pset.addTerminal("pepe", str)

print pset.terminals


lista = [1,2,43,4,5,3,6,76]
print lista
print lista[0:3]

