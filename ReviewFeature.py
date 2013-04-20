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
            #increment document length
            self.docLength += len(text) 
            '''
            if POS tagging is enabled tag words in sentences using nltk.pos_tag()
            Remove all non-alphanumeric characters in the individual tokens in any case
            '''
            
            stopwords = []
            if self.removeStopWords:
                stopwords = nltk.corpus.stopwords.words('english')
            
            if self.POS_tagging:
                self.tokens.extend([re.sub(r'[^a-zA-Z0-9]','',
                                           (x if self.lemmatizer == None 
                                            else self.lemmatizer.lemmatize(x, self.get_wordnet_pos(y)))).lower() 
                                    + '/' + y for (x,y) in nltk.pos_tag(text) if x.lower() not in stopwords])
            else:
                self.tokens.extend([re.sub(r'[^a-zA-Z0-9]','',
                                           (w if self.lemmatizer == None else self.lemmatizer.lemmatize(w))).lower() 
                                    for w in text if w.lower() not in stopwords])
    '''
    convert upenn tree bank POS tags to wordnet POS tags 
    If we pass POS information as well to the lemmatizer, it will be more accurate
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
    pass lemmatizer that should be used for lemmatization 
    set POS_tagging to true if we want to tag tokens with POS tags
    '''
    def __init__(self, doc_id, review_text, review_polarity, rating, 
                 lemmatizer = None, POS_tagging = False, removeStopWords = False):
        '''
        Constructor
        '''
        self.doc_id = doc_id
        self.sentences = []
        self.tokens = []
        self.review_text = review_text
        self.rating = rating
        self.polarity = review_polarity if review_polarity and review_polarity.strip() != "" else "?"
        self.lemmatizer = lemmatizer
        self.POS_tagging = POS_tagging
        self.removeStopWords = removeStopWords
        self.docLength = 0
        self.processTokens()
    
    def getTokens(self):
        return self.tokens
    
    def getSentences(self):
        return self.sentences
    
    def getDocId(self):
        return self.doc_id
    
    def getPolarity(self):
        return self.polarity if self.polarity != None else '?'
    
    def getRating(self):
        return self.rating
    
    def getDocLength(self):
        return self.docLength