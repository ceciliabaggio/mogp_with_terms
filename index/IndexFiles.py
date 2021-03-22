#!/usr/bin/env python

#INDEX_DIR = "IndexFiles.index"
INDEX_DIR = "Set12_utf8_term.index"
#INDEX_DIR = "set_temp_term_englishAnalyzer.index"

import sys, os, lucene, threading, time
from datetime import datetime
#import xml.etree.ElementTree as ET

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.en import EnglishAnalyzer
#from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.document import Document, Field, StringField, TextField
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.document import FieldType

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk 

from bs4 import BeautifulSoup
import enchant

#nltk.download()
#from nltk.corpus import wordnet

from sets import Set
import string


#####################################
######## INDEXES DMOZ WITH ##########
########    LUCENE 6.5.0   ##########
#####################################

# searches documensts by terms
# stemming done 
# index is: Term - > DocId, Topic, TermsInDoc

"""
This class is loosely based on the Lucene (java implementation) demo class
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""
    
    files_without_spots=0

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(Paths.get(storeDir))
        
        analyzer = StandardAnalyzer()
        #analyzer = EnglishAnalyzer()
        #analyzer = LimitTokenCountAnalyzer(analyzer, 10000)
        config = IndexWriterConfig(analyzer)
        
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        print "%d docs in index" % writer.numDocs()
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'
        #print "File WITHOUT SPOTS = ", self.files_without_spots

    def checkIntegrity(self, original_list, text, sep, error):
        #chequea que los Spots al hacer split sean igual que los del indice  
        
        if (original_list==[]):
            self.files_without_spots+=1
        
        else:
            list_text = text.split(sep)   
                              
            for i in list_text:
                if not(i in original_list):
                    error_docs = open(error, "a+")                
                    error_docs.write(i + " is not in original list")
                    error_docs.close()
                    return False 
                        
        return True
     
    def indexDocs(self, root, writer):
        
        
        nltk.download('stopwords')             
        stopWords = set(stopwords.words('english')).union(set(string.punctuation))
        
        dict = enchant.Dict("en_US")

        
        t1 = FieldType()
        t1.setStored(True)
        t1.setTokenized(True)
        t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
                
        #t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        #t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        #t2 = FieldType()
        #t2.setIndexed(False)
        #t2.setStored(True)
        #t2.setTokenized(True)
        #t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        #t3 = FieldType()
        #t3.setIndexed(False)
        #t3.setStored(True)
        #t3.setTokenized(False)
        #t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        for root_dir, dirnames, filenames in os.walk(root):
            print "root=", root_dir
                            
            error_docs = open(root + "errors_indexing.txt", "a+")
            error_docs.close()
            
            for filename in filenames:
                #print filename
                
                if filename.endswith('.txt'):
                    try:
                        path = os.path.join(root_dir, filename)
                        f = open(path)                       
                        contents = unicode(f.read(), 'utf-8')
                                                                    
                        f.close()
                        
                        soup = BeautifulSoup(contents, 'html.parser')
                        content_without_html = soup.get_text()
                        
                        #El ultimo elemento del arreglo de la url, es el topico
                        topic = root_dir.split("/")[-1]
                        
                        print "adding", topic, " ", filename
                        
                        doc = Document()                 
                        doc.add(Field("dmoz_id", topic.encode("ascii","replace")+"_"+str(filename), StringField.TYPE_STORED))
                        doc.add(Field("dmoz_url", root_dir.encode("ascii","replace"), StringField.TYPE_STORED))
                        doc.add(Field("dmoz_topic", topic.encode("ascii","replace"), StringField.TYPE_STORED))   
                        #now Snippet is INDEXED
                        doc.add(Field("dmoz_content", content_without_html.encode("ascii","replace"), t1))
      
                             
                        # OBTENER LISTA DE TERMINOS! 

                        words = word_tokenize(content_without_html)                                            
                        wordsFiltered = Set([])
                        
                        #words_not_filtered =Set([])
                        #english_word = Set([])
                        
                        for w in words:
                            if (w not in stopWords) and dict.check(w):                            
                                wordsFiltered.add(w.lower())                                
                            
                            #if (w not in stopWords):
                            #    words_not_filtered.add(w.lower())                                 
                            
                            #if (w not in stopWords) and wordnet.synsets(w.lower()):                             
                            #    english_word.add(w.lower())
                                                        
                        #print "english words in wordnet"
                        #print sorted(english_word)  
                            
                        #print "\nenglish words by enchant"
                        #print wordsFiltered
                        
                        
                        sep = "$#$"
                        
                        wordsFiltered = list(wordsFiltered)[:1000]
                        
                        term_list= sep.join(wordsFiltered)                    
                        
                        if (self.checkIntegrity(wordsFiltered, term_list, sep, root + "errors_indexing.txt")):

                            doc.add(Field("document_terms",   term_list, StringField.TYPE_STORED))                            
                        else:
                            raise Exception('Error indexing terms for file ' +filename)       
                            
                            
                        #print "\nenchant: not-filtered diff. Filtered"                            
                        #print sorted(words_not_filtered.difference(wordsFiltered))
                        
                        print '------------------------------------------------'
                                                                                                                        
                        """ Use StringField for a field with an atomic value that 
                        should not be tokenized. Use TextField for a field that
                        needs to be tokenized into a set of words."""                   
                                        
                        writer.addDocument(doc)  

                        #print doc.getFields("dmoz_content")
                                      
                        if len(contents) <= 0:                      
                            print "warning: no content in %s" % filename                                                   
                    except Exception, e:
                        error_docs = open(root + "errors_indexing.txt", "a+")
                        error_docs.write(root_dir +"/" + filename + "\n")
                        error_docs.write(str(e))
                        error_docs.close()
                        print "Failed in indexDocs:", filename
                        print e
                        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))        
        docs_to_index_directory = sys.argv[1] 
        #the index will be saved in the current DIR of the IndexeFiles.py
        IndexFiles(docs_to_index_directory, os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer)
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
