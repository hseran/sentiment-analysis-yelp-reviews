'''
Created on Apr 6, 2013

@author: naresh
'''

class Dictionary(object):
    '''
    We pass an object of Corpus to Dictionary to create a unique list of tokens (dimensions in our feature vector)
    '''

    def __init__(self, corpus):
        '''
        Constructor
        '''
        self.tokens = set()
        if corpus:
            self.createDictionary(corpus)
        
            
    def getTerms(self):
        return self.tokens
    
    def createDictionary(self, corpus):
        i = 0
        self.tokens.clear()
        for review_feat in corpus.getCorpus():
            for word in review_feat.getTokens():
                temp = word.strip();
                '''
                if word starts with / then it has only POS tag and not the actual word. skip it
                '''
                if temp.startswith('/') or temp == '':
                    continue
                self.tokens.add(temp)
                i += 1
                
        print "Actual number of words " + str(i) + "|  created dictionary with size " + str(len(self.tokens))
