'''
Created on Apr 8, 2016

@author: cecilia
'''

class result:
    
    ## new instance of result
    def __init__(self, topic, doc_id, snippet, url, spots, entities, scores, 
                                                                    doc_terms):
        self.topic = topic
        
        """ el ID es de la forma 123.txt y se almacena como 123 """        
        self.doc_id = doc_id.split(".")[0]
        self.snippet = snippet        
        self.url = url
        self.spots = spots
        self.entities = entities
        self.scores = scores
        self.document_terms = doc_terms

    def getDocTerms(self):
        return self.document_terms
                     
    def getDocId(self):
        return self.doc_id
    
    def getDocTopic(self):
        return self.topic
    
    def getDocSnippet(self):
        return self.snippet
    
    def getDocUrl(self):
        return self.url
    
    def getDocSpots(self):
        return self.spots
    
    def getDocEntities(self):
        return self.entities
    
    def getDocScores(self):
        return self.scores
    