'''
Created on Apr 8, 2013

@author: vinoth
'''

from Review import Review
import operator

if __name__ == '__main__':
	
	#input files
	review_files = ["../high-rating-reviews.xml", "../low-rating-reviews.xml","../mid-rating-reviews.xml"]
	
	#output files
	unlabeled_file='../unlabeled-reviews.xml'
	labeled_file='../labeled-reviews.xml'
	
	#lists for labeled and unlabeled reviews
	unlabeled=[]
	labeled=[]

	for each_file in review_files:	
		
		#call the readReviewsFromXML
		reviews = Review.readReviewsFromXML(each_file)

		for each_review in reviews:

			#convert reviewId into int, which help in sorting before saving in disk. 

			each_review.reviewId=int(each_review.getReviewId())

			#check and append if polarity is empty
		
			if (each_review.getReviewPolarity() == ""):
				unlabeled.append(each_review)
			else:
				labeled.append(each_review)

	#reviews from 3 files are appended to lists, but they are unsorted. Hence sorting them here.

	unlabeled.sort(key = operator.attrgetter('reviewId'))
	labeled.sort(key = operator.attrgetter('reviewId'))
	
	#Saving to disk
	
	Review.serializeToXML(unlabeled,unlabeled_file)
	Review.serializeToXML(labeled,labeled_file)

	#Comment if not required.
	print "Labeled :"+str(len(labeled))
	print "Unlabeled :"+str(len(unlabeled))

