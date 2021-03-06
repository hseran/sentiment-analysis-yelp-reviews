'''
Created on Apr 8, 2013

@author: vinoth
'''

from Review import Review
import operator

if __name__ == '__main__':
	
	#input files
	review_files = ["../labeled-reviews.xml", "../unlabeled-reviews.xml"]
	
	#output files
	unlabeled_file='../test-data.xml'
	labeled_file='../traning-data.xml'
	
	#lists for labeled and unlabeled reviews
	unlabeled=[]
	labeled=[]
	labeled_high=[]
	labeled_low=[]
	labeled_mid=[]

	for each_file in review_files:	
		
		#call the readReviewsFromXML
		reviews = Review.readReviewsFromXML(each_file)

		for each_review in reviews:

			#convert reviewId into int, which help in sorting before saving in disk. 

			each_review.reviewId=int(each_review.getReviewId())

			#check and append if polarity is empty
		
			if (each_review.getReviewPolarity() == ""):
				unlabeled.append(each_review)
			elif (each_review.getReviewPolarity() == "-1"):
				labeled_low.append(each_review)
			elif(each_review.getReviewPolarity() == "0"):
				labeled_mid.append(each_review)
			elif(each_review.getReviewPolarity() == "1"):
				labeled_high.append(each_review)

	#reviews from 3 files are appended to lists, but they are unsorted. Hence sorting them here.
		
	unlabeled.sort(key = operator.attrgetter('reviewId'))
	labeled_low.sort(key = operator.attrgetter('reviewId'))
	labeled_mid.sort(key = operator.attrgetter('reviewId'))
	labeled_high.sort(key = operator.attrgetter('reviewId'))

	labeled.extend(labeled_low)
	labeled.extend(labeled_mid)
	labeled.extend(labeled_high)
	
	#Saving to disk
	
	Review.serializeToXML(unlabeled,unlabeled_file)
	Review.serializeToXML(labeled,labeled_file)

	#Comment if not required.
	print "Labeled-low: " +str(len(labeled_low))
	print "Labeled-mid: " +str(len(labeled_mid))
	print "Labeled-high: " +str(len(labeled_high))
	print "Total Labeled :"+str(len(labeled))
	print "Unlabeled :"+str(len(unlabeled))

