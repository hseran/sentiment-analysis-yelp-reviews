'''
Created on Apr 5, 2013

@author: naresh
'''
import nltk
from nltk.corpus import wordnet
import re

class ReviewFeature(object):
    '''
    This class tokenizes the review text based on the parameters passed to the constructor
    '''

    def processTokens(self):
        for sentence in nltk.sent_tokenize(self.review_text):
            self.sentences.append(sentence)
            text = nltk.word_tokenize(sentence)
            if (self.POS_tagging):
                self.tokens.extend([re.sub(r'[^a-zA-Z0-9]','',(x.lower() if self.lemmatizer == None else self.lemmatizer.lemmatize(x, self.get_wordnet_pos(y)))) 
                                    + '/' + y for (x,y) in nltk.pos_tag(text)])
            else:
                self.tokens.extend([re.sub(r'[^a-zA-Z0-9]','',w.lower() if self.lemmatizer == None else self.lemmatizer.lemmatize(x)) for w in text])
    
    '''
    convert upenn tree bank POS tags to wordnet POS tags 
    '''
    @staticmethod
    def get_wordnet_pos(upenn_tag):
        if upenn_tag.startswith('J'):
            return wordnet.ADJ
        elif upenn_tag.startswith('V'):
            return wordnet.VERB
        elif upenn_tag.startswith('N'):
            return wordnet.NOUN
        elif upenn_tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN                
    
    '''
    pass wordnet lemmatizer to lemmatize 
    set POS_tagging to true if we want to tag tokens with POS tags
    '''
    def __init__(self, doc_id, review_text, review_polarity, lemmatizer = None, POS_tagging = False):
        '''
        Constructor
        '''
        self.doc_id = doc_id
        self.sentences = []
        self.tokens = []
        self.review_text = review_text
        self.polarity = review_polarity if review_polarity and review_polarity.strip() != "" else "?"
        self.lemmatizer = lemmatizer
        self.POS_tagging = POS_tagging
        self.processTokens()
    
    def getTokens(self):
        return self.tokens
    
    def getSentences(self):
        return self.sentences
    
    def getDocId(self):
        return self.doc_id
    
    def getPolarity(self):
        return self.polarity if self.polarity != None else '?'