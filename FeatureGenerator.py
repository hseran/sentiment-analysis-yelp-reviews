'''
Created on Mar 28, 2013
@author: naresh
'''

import nltk
from Corpus import Corpus
from Dictionary import Dictionary
from Review import Review
from TFIDFCalculator import TFIDFCalculator
from FeatureWeight import FeatureWeight

class FeatureGenerator(object):
    '''
    This class generates features for reviews present in corpus based on terms in dictionary
    '''
    def __init__(self, corpus, dictionary, featureVectorFile, 
                 weightScheme = FeatureWeight.PRESENCE, 
                 includeRating = False, 
                 includeDocLength = False):
        self.corpus = corpus
        self.output = featureVectorFile
        self.dictionary = dictionary
        self.weightScheme = weightScheme
        self.includeRating = includeRating
        self.includeDocLength = includeDocLength

    def generateFeatures(self):
        '''
        invoke this method to generate feature vector
        '''
        if (not self.output) or self.output.strip() == "":
            self.output = "output.txt"
        
        tfidfcalc = None
        
        if self.weightScheme != FeatureWeight.PRESENCE:
            tfidfcalc = self.getTFIDFCalculator()
                    
        dimensions = self.dictionary.getTerms()
        writer = open(self.output, "w")
        #writer.write("doc_id," + ",".join(dimensions) + (",_rating_" if self.includeRating else "")+ ",_polarity_\n")
        writer.write(",".join(dimensions) + (",_rating_" if self.includeRating else "")+ (",_docLength_" if self.includeDocLength else "")+ ",_polarity_\n")
        for rev_feat in self.corpus.getCorpus():
            arr = []
            for term in dimensions:
                weight = 0
                if term in rev_feat.getTokens():
                    weight = self.getWeight(rev_feat.getDocId(), term, tfidfcalc)
                arr.append(str(weight))
            #writer.write(rev_feat.getDocId()+"," + ",".join(arr) + 
            #             ("," + str(rev_feat.getDocId()) if self.includeRating else "") + "," + self.getPolarityString(rev_feat.getPolarity())+"\n")
            writer.write(",".join(arr) + ("," + str(rev_feat.getRating()) if self.includeRating else "") +  ("," + str(rev_feat.getDocLength()) if self.includeDocLength else "") + "," + self.getPolarityString(rev_feat.getPolarity())+"\n")

        writer.close()
        del tfidfcalc

    def getPolarityString(self, polarity):
        '''
        if we pass 1,-1, 0 to machine learning algos they are treating 
        our task as regression instead of classification. So using strings for representing polarity
        '''
        temp = str(polarity)
        if temp == '0':
            return 'neutral'
        if temp == '1':
            return 'positive'
        if temp == '-1':
            return 'negative'
        return '?'

    def getWeight(self, docId, term, tfidfcalc):
        '''
        this method returns weights for the feature vector
        '''
        if self.weightScheme == FeatureWeight.PRESENCE or tfidfcalc == None:
            return 1
        if self.weightScheme == FeatureWeight.TF:
            return tfidfcalc.get_tf(docId, term)
        if (self.weightScheme == FeatureWeight.TFIDF):
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
'''
if __name__ == '__main__':
    reviews = Review.readReviewsFromXML('../low-rating-reviews.xml')
    corpus = Corpus(reviews, nltk.WordNetLemmatizer(), POS_tagging = True)
    del reviews
    dictionary = Dictionary(corpus)
    generator = FeatureGenerator(corpus, dictionary, '../features-idf.txt', FeatureWeight.TFIDF, False)
    generator.generateFeatures()
'''
