'''
Created on Apr 8, 2016

@author: cecilia
'''

class result:
    
    ## new instance of wordsPool
    def __init__(self, topic, doc_id, snippet, url):
        self.topic = topic
        
        """ el ID es de la forma 123.txt y se almacena como 123 """        
        self.doc_id = doc_id.split(".")[0]
        self.snippet = snippet
        self.url = url
                    
    def getDocId(self):
        return self.doc_id
    
    def getDocTopic(self):
        return self.topic
    
    def getDocSnippet(self):
        return self.snippet
    
    def getDocUrl(self):
        return self.url
    