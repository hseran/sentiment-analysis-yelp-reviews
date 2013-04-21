'''
Created on Apr 15, 2013

This is where we invoke modules to generate features for training and test data

@author: naresh
'''
from Review import Review
import nltk
from Corpus import Corpus
from Dictionary import Dictionary
from FeatureGenerator import FeatureGenerator
from FeatureWeight import FeatureWeight

if __name__ == '__main__':
    trainingreviews = Review.readReviewsFromXML("../old-training-shuffled.xml")
    lemmatizer = nltk.WordNetLemmatizer()
    testReviews = Review.readReviewsFromXML("../old-test-data.xml")
    
    trainCorpus = Corpus(trainingreviews, lemmatizer, POS_tagging = True)
    '''this dictionary will be used for both training and validation data'''
    dictionary = Dictionary(trainCorpus)
    generator = FeatureGenerator(trainCorpus, dictionary, '../train.csv', weightScheme= FeatureWeight.TFIDF)
    generator.generateFeatures()
    
    testCorpus = Corpus(testReviews, lemmatizer, POS_tagging = True);
    generator = FeatureGenerator(testCorpus, dictionary, '../test.csv',weightScheme= FeatureWeight.TFIDF)
    generator.generateFeatures()
