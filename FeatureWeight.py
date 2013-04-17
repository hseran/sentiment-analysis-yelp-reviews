'''
Created on Apr 10, 2013

@author: naresh
'''

class FeatureWeight:
    'This is enum to indicate which weights are to be used in feature vector'
    #binary 0 1 . just indicates presence
    PRESENCE = 1 
    #term frequency. number of times term occurs in document
    TF = 2 
    #tf-idf. term-frequency multiplied by inverse document frequency (http://en.wikipedia.org/wiki/Tf%E2%80%93idf)
    TFIDF = 3
