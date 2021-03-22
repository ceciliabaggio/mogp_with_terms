#!/usr/bin/env python

#INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time
from datetime import datetime
import xml.etree.ElementTree as ET

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard  import StandardAnalyzer
from org.apache.lucene.analysis.core import KeywordAnalyzer
from org.apache.lucene.document import Document, Field, FieldType, StringField, TextField
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig 
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version


###################################
####### LUCENE 4.9.0 ##############
###################################

sys.path.insert(0, os.getcwd())


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
    """Usage: python Index.py <doc_directory><save_index_folder>"""
    
    files_without_spots=0

    def __init__(self, root, storeDir, analyzer):
        
        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        #This Analyzer limits the number of tokens while indexing.
        #It is a replacement for the maximum field length setting inside 
        #IndexWriter.
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
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
        print "File WITHOUT SPOTS = ", self.files_without_spots
        
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

        t1 = FieldType("StringField")
        t1.setIndexed(True)
        t1.setStored(True)
        t1.setTokenized(False)        
        t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
        #t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        t2 = FieldType()
        t2.setIndexed(False)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        t3 = FieldType()
        t3.setIndexed(False)
        t3.setStored(True)
        t3.setTokenized(False)
        #t3.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)
                

       
        
        for root_dir, dirnames, filenames in os.walk(root):
            print "root=", root_dir
                            
            error_docs = open(root + "errors_indexing.txt", "a+")
            error_docs.close()
            
            for filename in filenames:
                #print filename
                
                if filename.endswith('.txt'):
                    
                    print "adding", filename
                    try:
                        path = os.path.join(root_dir, filename)
                        file = open(path)                       
                        contents = unicode(file.read(), 'utf-8')
                        file.close()                              
                        #read from XML                                
                        xml_doc_name = filename.replace("txt", "xml")
                        xml_doc = os.path.join(root_dir, xml_doc_name)                        
                        print xml_doc                                                           
                        #El ultimo elemento del arreglo de la url, es el topico
                        topic = root_dir.split("/")[-1]
                        doc = Document()
                        doc.add(Field("dmoz_id", str(topic)+"_"+str(filename), t1))
                        doc.add(Field("dmoz_url", root_dir, t1))
                        doc.add(Field("dmoz_topic", str(topic), t1))   
                        #now Snippet is NOT INDEXED
                        doc.add(Field("dmoz_snippet", contents, t2))                                             
                        tree = ET.parse(xml_doc)
                        raiz = tree.getroot()                                                  
                        #annotations = []
                        spot_list = []  #this lists are better when docuemnt is
                        entity_list= [] #retrieved. Doesnt have to loop again                       
                        score_list = [] #over Fields
                        for tag in raiz.findall('annotation'):
                            spot = tag.find('spot').text                                
                            entity = tag.find('entity').text                            
                            score = tag.find("score").text                                                    
                            #print spot, '-->', entity, '-->', score                            
                            doc.add(Field("spot", spot, t1))                            
                            doc.add(Field("entity", entity,t1))
                            doc.add(Field("score", score, t1))
                            spot_list.append(str(spot))
                            entity_list.append(str(entity))
                            score_list.append(str(score))                 
                                        
                        sep = "$#$"
                             
                        sl= sep.join(spot_list)
                        el= sep.join(entity_list)
                        scl= sep.join(score_list)
                        
                        if (self.checkIntegrity(spot_list, sl, sep, root + "errors_indexing.txt") and                        
                            self.checkIntegrity(entity_list, el, sep, root + "errors_indexing.txt") and                        
                            self.checkIntegrity(score_list, scl, sep, root + "errors_indexing.txt")):
                            
                            #si no falla ningna mas arriba...                    
                            doc.add(Field("spot_list", sl , t3))
                            doc.add(Field("entity_list", el, t3))
                            doc.add(Field("score_list", scl, t3))
                        else:
                            raise Exception('Error indexing Spots for file ' +filename)       
                                       
                        print '------------------------------------------------'
                                                                                                                        
                        """ Use StringField for a field with an atomic value that 
                        should not be tokenized. Use TextField for a field that
                        needs to be tokenized into a set of words."""                   
                                        
                        writer.addDocument(doc)                    
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
    
    if len(sys.argv) < 3:
        print IndexFiles.__doc__
        sys.exit(1)
        
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))        
        docs_to_index_directory = sys.argv[1] 
        save_index_folder = sys.argv[2]
        INDEX_DIR = save_index_folder        
        #IndexFiles(docs_to_index_directory, os.path.join(base_dir, INDEX_DIR),
        #           StandardAnalyzer(Version.LUCENE_CURRENT))
        
        IndexFiles(docs_to_index_directory, os.path.join(base_dir, INDEX_DIR),
                   StandardAnalyzer(Version.LUCENE_CURRENT))

        #https://stackoverflow.com/questions/5483903/comparison-of-lucene
        #-analyzers?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
        # KeywordAnalyzer
        """ Builds an analyzer with the default stop words (STOP_WORDS_SET).
        StopAnalyzer(Version matchVersion, File stopwordsFile)
        Builds an analyzer with the stop words from the given file."""
        
        end = datetime.now()
        
        print end - start

    except Exception, e:
        print "Failed: ", e
        raise e
