#!/usr/bin/env python


#INDEX_DIR = "index/Set12.index"

import sys, os, lucene
from datetime import datetime
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version



#####################################
######## SEARCHES DMOZ WITH #########
########    LUCENE 6.5.0   ##########
#####################################

# searches documensts by terms
# stemming done 
# index is: Term - > DocId, Topic, TermsInDoc


# Bring index package onto the path
dirname=os.path.dirname
parent_dir= dirname(dirname(os.path.abspath(__file__)))

sys.path.insert(0,parent_dir)

from result import result

def time_starting(texto):
    print datetime.now(), texto
    return datetime.now()
  
def time_finishing(t, texto):
    delta = datetime.now() - t
    print delta, texto
    
"""
This script is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""

def escapeQuotes(s):
    # replace doble quotes inside spot for another symbol
    s = s.replace('"','\\"')
    return s

# for sequential TESTING search
def searchWithLucene_evaluation(searcher, analyzer, query):
       
    start = datetime.now()
    result_list=[] 
            
    query = QueryParser("dmoz_content", analyzer).parse(query)
    
    MAX_NUM_HITS = 10000
    
    scoreDocs = searcher.search(query, MAX_NUM_HITS).scoreDocs     
    
    c = 0
    for hit in scoreDocs:
        c+=1
        doc = searcher.doc(hit.doc)        
        
        sep = "$#$"
        
        links = []
        concepts = []
        rank = []
        
        doc_terms = doc.get("document_terms").encode("ascii", "replace")
        
        if (doc_terms != ""):
            doc_terms = doc_terms.split(sep)
        
        # agrega $#$ en lugar de "
        doc_terms_quoted=['"'+s.replace('"', sep)+'"' for s in doc_terms]
          
        r = result(doc.get("dmoz_topic").encode("utf-8"), 
                   doc.get("dmoz_id").encode("utf-8"),
                   "",  
                   doc.get("dmoz_url").encode("utf-8"), 
                   links, concepts, rank, doc_terms_quoted)
        
        result_list.append(r)

    duration = datetime.now() - start
    print repr(query), "\nDuration Search: ", duration, "\n# Retrieved Resuls: ", len(result_list), "\n-------"
    #result_list tendra a lo sumo 10.000 documentos    
    
    return result_list
                    

# for parallel TRAINING search           
def searchWithLucene(searcher, analyzer, query, info):
    
    # to work with threads
    vm_env = lucene.getVMEnv()
    vm_env.attachCurrentThread()
    
    start = datetime.now()
    result_list=[] 
    q1 = query        
    query = QueryParser("dmoz_content", analyzer).parse(query)
    
    MAX_NUM_HITS = 10000
    
    scoreDocs = searcher.search(query, MAX_NUM_HITS).scoreDocs     
    
    c = 0
    for hit in scoreDocs:
        c+=1
        doc = searcher.doc(hit.doc)        
        
        sep = "$#$"
        
        links = []
        concepts = []
        rank = []
        
        #doc_terms = doc.get("document_terms").encode("utf-8")
        doc_terms = doc.get("document_terms").encode("ascii", "replace")

        
        if (doc_terms != ""):
            doc_terms = doc_terms.split(sep)
        
        # agrega $#$ en lugar de "
        doc_terms_quoted=['"'+s.replace('"', sep)+'"' for s in doc_terms]
        
        f = open("terms.txt", "w+")
        f.write(str(doc_terms_quoted))
        f.close()
        #print doc_terms_quoted
          
        r = result(doc.get("dmoz_topic").encode("utf-8"), 
                   doc.get("dmoz_id").encode("utf-8"),
                   "",  
                   doc.get("dmoz_url").encode("utf-8"), 
                   links, concepts, rank, doc_terms_quoted)
        result_list.append(r)

    duration = datetime.now() - start
    print info, "\n", q1, "\n", repr(query), "\nDuration Search: ", duration, "\n# Retrieved Resuls: ", len(result_list), "\n-------"
    #result_list tendra a lo sumo 10.000 documentos    
    
    return result_list
                    

def createAnalyzer(INDEX_DIR):
    
    
    #print "INDEX = ", INDEX_DIR
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    base_dir = os.path.dirname(os.getcwd())
    directory = SimpleFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))    
    searcher = IndexSearcher(DirectoryReader.open(directory))

    # Whereas, StandardAnalyzer is just a StandardTokenizer, StandardFilter, 
    # LowercaseFilter, and StopFilter.  EnglishAnalyzer rolls in an 
    # EnglishPossesiveFilter, KeywordMarkerFilter, and PorterStemFilter.
    analyzer = StandardAnalyzer()
    #analyzer = EnglishAnalyzer()
      
    return searcher, analyzer

def eliminateAnalyzer(searcher, analyzer):
    
    del searcher
    del analyzer
    

lucene.initVM(vmargs=['-Djava.awt.headless=true -Xms2g -Xmx8g'])
print 'lucene', lucene.VERSION

#===============================================================================
#  
# #s,a = createAnalyzer("/home/cecilia/repos/mogp_with_terms/index/set_temp_term_standardAnalyzer.index")
# s,a = createAnalyzer("/home/cecilia/repos/mogp_with_terms/index/Set3_utf8_term.index")
#    
# q = "automorphic"
#    
# q = "Westminster" # no lo encuentra
# q = "westminster"# poner todo en minuscula =)
#    
# q = "princeton"
#    
# #q = "langlands"
#    
#    
# q = "'on-line'"
#  
# f = open("/home/cecilia/repos/mogp_with_terms/runs/mogp_2018-08-10_16-38-51/Co2/134/134_1_prec@10-EntropicRecall_nGen(4)_popSize(4)_indSize(XX)_cross(0.7)_mut(0.3)_seed(12803)_queries.txt", "r")
# q = f.readline()
# print  q.__class__ 
# print q.encode('utf-8') # Unicode => ASCII
# print  q.__class__
# f.close()  
#    
#    
# res = searchWithLucene(s, a, q, "")
#    
# docs = [x.getDocId() for x in res]
# print docs 
#     
#    
# eliminateAnalyzer(s, a)
#===============================================================================
