'''
Created on May 27, 2015

@author: cecilia
'''

from sets import Set
import os
import xml.etree.ElementTree as ET

import enchant
from bs4 import BeautifulSoup

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

import string

nltk.download('stopwords')
nltk.download('punkt')

class phrase_pool:

    ## new instance of spots_pool
    def __init__(self):
        self.words = set([]) 
        #self.StopWordSet = self.loadStopWords()

  
    #now the terminals are spots (phrases)
    #it extracts terminals from the topic description (not indexed in lucene)
    def getSpotsAndEntitiesFromXML(self, xml_doc):
       
        set_of_spots = []
        set_of_entities = []
        set_of_scores = []
        
        tree = ET.parse(xml_doc)
        raiz = tree.getroot()                                                  
        
        for tag in raiz.findall('annotation'):
            spot = tag.find('spot').text                
            entity = tag.find('entity').text            
            score = tag.find("score").text                                        
            set_of_spots.append(str('"' + spot + '"')) #lucene Fix to build queries 
            set_of_entities.append(str('"' + entity + '"'))
            set_of_scores.append(score)
        #print "entities= ", set_of_entities
        #print "spots", set_of_spots
        return set_of_spots, set_of_entities, set_of_scores
    
    def getTopicDescriptionTerms(self, topic_doc):
        
        
        
         
        stopWords = set(stopwords.words('english')).union(set(string.punctuation))
        
        dictio = enchant.Dict("en_US")
        
        f = open(topic_doc)                       
        #contents = unicode(f.read(), 'utf-8')
        contents = f.read()                                            
        f.close()
        
        soup = BeautifulSoup(contents, 'html.parser')            
        content_without_html = soup.get_text() 
        
        # OBTENER LISTA DE TERMINOS! 
            
        words = word_tokenize(content_without_html)                                            
        wordsFiltered = Set([])
        
        #words_not_filtered =Set([])
        #english_word = Set([])
        
        for w in words:
            if (w not in stopWords) and dictio.check(w):                          
                wordsFiltered.add('"' + w.lower() + '"') 
        
        return wordsFiltered               
    
    
# x = phrase_pool()
# TOPIC_ID = ["134", "187", "529", "537","538", "556", "561", "58"] 

# for i in TOPIC_ID:
#    l= x.getTopicDescriptionTerms("index/topics/"+i+".txt")
#    print l