'''
Created on Mar 28, 2013
@author: naresh
'''

import nltk
from Corpus import Corpus
from Dictionary import Dictionary
from Review import Review

class FeatureGenerator(object):
    '''
    This class generates features for reviews
    '''
    def __init__(self, reviewsList, corpus, dictionary, featureVectorFile):
        self.review = reviewsList
        self.corpus = corpus
        self.output = featureVectorFile
        self.dictionary = dictionary
        
    '''
    invoke this method to generate feature vector
    '''
    def generateFeatures(self):
        if (not self.output) or self.output.strip() == "":
            self.output = "output.txt"
        
        dimensions = self.dictionary.getTerms()
        writer = open(self.output, "w")
        writer.write("doc_id," + ",".join(dimensions) + ",polarity\n")
        for rev_feat in self.corpus.getCorpus():
            arr = []
            for term in dimensions:
                present = 0
                if term in rev_feat.getTokens():
                    present = 1
                arr.append(present)
            writer.write(rev_feat.getDocId()+"," + ",".join(str(x) for x in arr) + "," + rev_feat.getPolarity()+"\n")
        writer.close()
        
if __name__ == '__main__':

    reviews = Review.readReviewsFromXML('../low-rating-reviews.xml')
    corpus = Corpus(reviews, nltk.WordNetLemmatizer(), POS_tagging = True)
    dictionary = Dictionary(corpus)
    generator = FeatureGenerator(reviews, corpus, dictionary, '../features.txt')
    generator.generateFeatures()
    
    '''sum = 0
    uniq = set()
    for review_feat in corpus.getCorpus():
        sum += len(review_feat.getTokens())
        for token in review_feat.getTokens():
            if token not in uniq:
                uniq.add(token)
    
    print 'total tokens: ' + str(sum) + ' uniq: ' + str(len(uniq))
    for token in uniq:
            print token'''
    