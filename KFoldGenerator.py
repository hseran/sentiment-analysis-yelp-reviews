'''
Created on Apr 6, 2013

@author: naresh
'''

from Review import Review
from Dictionary import Dictionary
from Corpus import Corpus
from FeatureGenerator import *

class KFoldGenerator(object):
    '''
    classdocs
    '''

    def __init__(self, reviews, k):
        self.reviews = reviews
        self.k = k
            
    ## {{{ http://code.activestate.com/recipes/521906/ (r3)
    def k_fold_cross_validation(self, randomise = False):
        """
        Generates K (training, validation) pairs from the items in X.
    
        Each pair is a partition of X, where validation is an iterable
        of length len(X)/K. So each training iterable is of length (K-1)*len(X)/K.
    
        If randomise is true, a copy of X is shuffled before partitioning,
        otherwise its order is preserved in training and validation.
        """
        X = self.reviews
        K = self.k
        
        if randomise: from random import shuffle; X=list(X); shuffle(X)
        for k in xrange(K):
            training = [x for i, x in enumerate(X) if i % K != k]
            validation = [x for i, x in enumerate(X) if i % K == k]
            yield training, validation

    #X = [i for i in xrange(97)]
    #for training, validation in k_fold_cross_validation(X, K=7):
    #    for x in X: assert (x in training) ^ (x in validation), x
    ## end of http://code.activestate.com/recipes/521906/ }}}
    
    def generateKFolds(self, location = "./", trainingData = {}, validationData = {}):
        if self.reviews == None or len(self.reviews) == 0:
            print 'No data to work on'
            return
        i = 0;
        
        import os
        if not os.path.isdir(location):
            location = "./"
        
        for training, validation in self.k_fold_cross_validation():
            i = i + 1
            Review.serializeToXML(training, location + "/train" + str(i) + ".xml")
            Review.serializeToXML(validation, location + "/valid" + str(i) + ".xml")
            trainingData[str(i)] = training
            validationData[str(i)] = validation


    def generateFeatures(self, outdir, lemmatizer = None, POS_tagging = False):
        if self.reviews == None or len(self.reviews) == 0:
            print 'No data to work on'
            return
        
        trainingData = {}
        validationData = {}
        self.generateKFolds(outdir, trainingData, validationData)        
        
        for i in range(1,self.k+1):
            print "generating features for fold " + str(i)          
            
            trainCorpus = Corpus(trainingData[str(i)], lemmatizer, POS_tagging)
            '''this dictionary will be used for both training and validation data'''
            dictionary = Dictionary(trainCorpus)
            generator = FeatureGenerator(trainCorpus, dictionary, Feature.TFIDF, outdir + '/train' + str(i) + '.csv')
            generator.generateFeatures()
            
            validCorpus = Corpus(trainingData[str(i)], lemmatizer, POS_tagging);
            generator = FeatureGenerator(validCorpus, dictionary, Feature.TFIDF, outdir + '/valid' + str(i) + '.csv')
            generator.generateFeatures()
            
if __name__ == '__main__':
    reviews = Review.readReviewsFromXML("../test.xml")
    lemmatizer = nltk.WordNetLemmatizer()
    print 'reviews: ' + str(len(reviews))
    kfg = KFoldGenerator(reviews, 10)
    kfg.generateFeatures("../kfolds", lemmatizer, True)    