'''
Created on Apr 5, 2013

@author: naresh
'''
from ReviewFeature import ReviewFeature

class Corpus(object):
    '''
    classdocs
    '''
    def __init__(self, reviewList, lemmatizer = None, POS_tagging = False):
        self.lemmatizer = lemmatizer
        #self.grams = grams
        self.POS_tagging = POS_tagging
        self.reviews = reviewList
        self.process()

    def processReview(self, review):
        review_text = review.getReviewText()
        review_polarity = review.getReviewPolarity()
        doc_id = review.getReviewId()
        processed_review = ReviewFeature(doc_id, review_text, review_polarity, self.lemmatizer, self.POS_tagging)
        return processed_review    
    
    def process(self):
        self.corpus = []
        for review in self.reviews:
            review_feature = self.processReview(review)      
            if review_feature:
                self.corpus.append(review_feature)
    
    def getCorpus(self):
        return self.corpus
    
    def __str__(self):
        str_list = []
        for clause in self.corpus:
            str_list.append(str(clause))
        return '\n'.join(str_list)           