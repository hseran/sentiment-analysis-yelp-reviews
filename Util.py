'''
Created on Apr 10, 2013

@author: naresh
'''
import random
from Review import Review

class Util(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def shuffleReviews(input_file, output_file):
        reviewList = Review.readReviewsFromXML(input_file)
        if reviewList == None or len(reviewList) == 0:
            print "No reviews in input file"
        
        random.shuffle(reviewList)
        Review.serializeToXML(reviewList, output_file)

    @staticmethod
    def siftReviewsByPolarity(input_file, output_file, polarity):
        '''
        out_file will contain all reviews from input_file 
        other than the ones labeled as polarity 
        '''
        reviewList = Review.readReviewsFromXML(input_file)
        if reviewList == None or len(reviewList) == 0:
            print "No reviews in input file"
        
        outList = []
        for review in reviewList:
            if str(review.getReviewPolarity()) == str(polarity):
                continue
            outList.append(review)
        Review.serializeToXML(outList, output_file)
    
    @staticmethod
    def seperateByRating(input_file, output_dir):
        reviewList = Review.readReviewsFromXML(input_file)
        high5 = []
        low1 = []
        medium = []
        low2 = []
        for review in reviewList:
            if str(review.getReviewRating()) == '5.0':
                review.setPolarity('1')
                review.setConfidence('1')
                high5.append(review)
            elif str(review.getReviewRating()) == '1.0':
                review.setPolarity('-1')
                review.setConfidence('1')
                low1.append(review)
            elif str(review.getReviewRating()) == '2.0':
                review.setPolarity('-1')
                review.setConfidence('1')
                low2.append(review)
            else:
                medium.append(review)
        
        Review.serializeToXML(high5, output_dir + "/high.xml")
        Review.serializeToXML(low1, output_dir + "/low1.xml")
        Review.serializeToXML(low2, output_dir + "/low2.xml")
        Review.serializeToXML(medium, output_dir + "/medium.xml")
        print "5: " + str(len(high5))
        print "1: " + str(len(low1))
        print "2: " + str(len(low2))       
         
    @staticmethod
    def printCount(file):
        reviewList = Review.readReviewsFromXML(file)
        print str(len(reviewList))
    
    @staticmethod
    def countLabeledReviews(file):
        reviewList = Review.readReviewsFromXML(file)
        count = 0
        for review in reviewList:
            if review.getReviewPolarity().strip() != '':
                count += 1
        print count
    
    @staticmethod
    def separateLabeledAndUnlabeled(file, output_dir):
        reviewList = Review.readReviewsFromXML(file)
        labeled = []
        unlabeled = []
        
        for review in reviewList:
            if review.getReviewPolarity().strip() != '':
                labeled.append(review)
            else:
                unlabeled.append(review)
        Review.serializeToXML(labeled, output_dir + "/labeled-neu.xml")
        Review.serializeToXML(unlabeled, output_dir + "/unlabeled-neu.xml")
        
        
    @staticmethod
    def labelTestFile(xml_test_file, weka_csv_results_file, output_file):
        '''
        this method takes the reviews xml file, weka results in CSV format
        applies polarity and confidence to reviews and write the resultant xml to output_file
        '''
        reviewList = Review.readReviewsFromXML(xml_test_file)
        
        results_file = open(weka_csv_results_file, "r")
        
        resultsList = results_file.readlines()
        
        if len(reviewList) != len(resultsList):
            print 'Different number of reviews and results'
            return
        
        counter = 0
        for review in reviewList:
            result = resultsList[counter].strip().split(',')
            counter += 1
            review.setPolarity( Util.getNumericLabel(result[2].split(':')[1]))
            review.setConfidence('0.9' if result[4] == '1' else result[4])
        
        print 'writing labelled test data to ' + output_file    
        Review.serializeToXML(reviewList, output_file)
        
            
    @staticmethod
    def getNumericLabel(polarity):
        if polarity == 'positive':
            return '1'
        elif polarity == 'negative':
            return '-1'
        return 0
    
if __name__ == '__main__':
    #Util.shuffleReviews("../new-training.xml", "../new-training.xml")
    #Util.siftReviewsByPolarity("../training-shuffled.xml", "../training-2-class.xml", 0)
    #Util.seperateByRating("../old-data/reviews.xml", "../")
    #Util.printCount('../high_.xml')
    #Util.countLabeledReviews('../high_.xml')
    #Util.separateLabeledAndUnlabeled("../medium.xml", "../")
    #Util.printCount('../low1.xml')
    #Util.printCount('../high.xml')
    Util.labelTestFile('../old-test-data.xml', '../weka-results.csv', '../labeled-test-data.xml')
    