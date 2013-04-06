'''
Created on Mar 28, 2013

@author: naresh
'''
import math

class TFIDFCalculator(object):
    '''
    This class takes a list of documents (each document represented as list of tokens)
    computes tf-idf for all the tokens.
    Whatever lemmatization, tagging and tokenization is required should be done and the resulting tokens
    should be passed to this constructor 
    '''


    '''
    documents: map<docId,list<tokens>>
    '''
    def __init__(self, documents):
        self.doc_term_freq = {}
        self.collection_freq = {}
        self.tfidf_map = {}
        self.collection = documents
        self.calculate()

    '''
    initializes term-frequencies and collection frequencies for every token
    '''
    def initializeCount(self):
        for docId in self.collection:
            doc_tokens = self.collection[docId]
            token_freq_map = {}
            
            #calculate term frequencies for every token in document
            for token in doc_tokens:
                if token in token_freq_map:
                    token_freq_map[token] += 1
                else:
                    token_freq_map[token] = 1
            
            #increment the collection frequency for every unique token
            #in document by 1 
            for token in token_freq_map:
                if token in self.collection_freq:
                    self.collection_freq[token] += 1
                else:
                    self.collection_freq[token] = 1
 
            self.doc_term_freq[docId] = token_freq_map
    
    
    '''
    calculates tf-idf for every token for every document
    '''
    def calculate(self):
        self.initializeCount()
        for docId in self.doc_term_freq:
            if docId not in self.tfidf_map:
                self.tfidf_map[docId] = {}
                
            max_freq = 0
            for (token, freq) in self.doc_term_freq[docId].items():
                if freq > max_freq:
                    max_freq = freq
                
            for (token,freq) in self.doc_term_freq[docId].items():
                idf = math.log(float(1 + len(self.collection)) / float(1 + self.collection_freq[token]))
                token_map = self.tfidf_map[docId]
                #normalize by dividing with max_freq
                token_map[token] = float(freq) / float(max_freq) * float(idf)


    def get_tfidf(self, docId, token):
        ''' returns tf-idf value'''
        if docId in self.tfidf_map:
            if token in self.tfidf_map[docId]:
                return self.tfidf_map[docId][token]
        return 0
    
    def get_tf(self, docId, token):
        '''returns term frequency'''
        if docId in self.doc_term_freq:
            if token in self.doc_term_freq[docId]:
                return self.doc_term_freq[docId][token]
        return 0
    
if __name__ == '__main__':
    documents = {1:"hello i do not do like this".split(), 2:"world i like this this this this".split(), 3:"do you this".split()}
    tfidfc = TFIDFCalculator(documents)
    print tfidfc.get_tfidf(1, "hello")
    print tfidfc.get_tfidf(1, "do")
    print tfidfc.get_tfidf(1, "like")
    print tfidfc.get_tfidf(2, "like")
    