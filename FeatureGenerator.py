'''
Created on Mar 28, 2013
@author: naresh
'''

import nltk
from Corpus import Corpus
from Dictionary import Dictionary
from Review import Review
from TFIDFCalculator import TFIDFCalculator

class FeatureGenerator(object):
    '''
    This class generates features for reviews present in corpus based on terms in dictionary
    '''
    def __init__(self, corpus, dictionary, weightScheme, featureVectorFile):
        self.corpus = corpus
        self.output = featureVectorFile
        self.dictionary = dictionary
        self.weightScheme = weightScheme
        

    def generateFeatures(self):
        '''
        invoke this method to generate feature vector
        '''
        if (not self.output) or self.output.strip() == "":
            self.output = "output.txt"
        
        tfidfcalc = None
        
        if self.weightScheme != Feature.PRESENCE:
            tfidfcalc = self.getTFIDFCalculator()
                    
        dimensions = self.dictionary.getTerms()
        writer = open(self.output, "w")
        writer.write("doc_id," + ",".join(dimensions) + ",polarity\n")
        for rev_feat in self.corpus.getCorpus():
            arr = []
            for term in dimensions:
                weight = 0
                if term in rev_feat.getTokens():
                    weight = self.getWeight(rev_feat.getDocId(), term, tfidfcalc)
                arr.append(str(weight))
            writer.write(rev_feat.getDocId()+"," + ",".join(arr) + "," + rev_feat.getPolarity()+"\n")
        writer.close()
        del tfidfcalc
    
    def getWeight(self, docId, term, tfidfcalc):
        '''
        this method returns weights for the feature vector
        '''
        if self.weightScheme == Feature.PRESENCE or tfidfcalc == None:
            return 1
        if self.weightScheme == Feature.TF:
            return tfidfcalc.get_tf(docId, term)
        if (self.weightScheme == Feature.TFIDF):
            return tfidfcalc.get_tfidf(docId, term)
        #1 by default
        return 1


    def getTFIDFCalculator(self):
        '''
        initilizes a tf-idf generator and returns it
        '''
        docMap = {}
        for rev_feat in self.corpus.getCorpus():
            docMap[rev_feat.getDocId()] = rev_feat.getTokens()
        return TFIDFCalculator(docMap)    

class Feature:
    'This is enum to indicate which weights are to be used in feature vector'
    #binary 0 1 . just indicates presence
    PRESENCE = 1 
    #term frequency. number of times term occurs in document
    TF = 2 
    #tf-idf. term-frequency multiplied by inverse document frequency (http://en.wikipedia.org/wiki/Tf%E2%80%93idf)
    TFIDF = 3

if __name__ == '__main__':

    reviews = Review.readReviewsFromXML('../low-rating-reviews.xml')
    corpus = Corpus(reviews, nltk.WordNetLemmatizer(), POS_tagging = True)
    del reviews
    dictionary = Dictionary(corpus)
    generator = FeatureGenerator(corpus, dictionary, Feature.TFIDF, '../features-idf.txt')
    generator.generateFeatures()
