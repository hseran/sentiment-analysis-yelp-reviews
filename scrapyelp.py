
import lxml.html
from lxml import html
from lxml.html import parse

def getReviewerInfo(element):

	#reviewer name
	for x in element.cssselect('.externalReview .offscreen span'):
		print html.tostring(x, method='text', encoding='unicode').strip()

	#reviewer location
	for x in element.cssselect('.externalReview .user-passport .reviewer_info'):
		print html.tostring(x, method='text', encoding='unicode').strip()
	
	#reviewer URL
	for x in element.cssselect('.externalReview .user-passport .user-passport-info .username a'):
		print html.tostring(x, method='text', encoding='unicode').strip()

	# reviewer's friends
	for x in element.cssselect('.externalReview .reviewer-details .user-stats .friend-count'):
		print html.tostring(x, method='text', encoding='unicode').strip()

    # number of reviews by user
	for x in element.cssselect('.externalReview .reviewer-details .user-stats .review-count'):
		print html.tostring(x, method='text', encoding='unicode').strip()	

	# rating
	for x in element.cssselect('.externalReview .review-meta .rating meta'):
		print x.get('content')
	
	# number of reviews by user
	for x in element.cssselect('.externalReview .reviewer-details .user-stats .review-count'):
		print html.tostring(x, method='text', encoding='unicode').strip()

	#print "users" . no_of_users	
	#for x in element.cssselect('.externalReview .review_comment'):
		#print html.tostring(x, method='text',encoding=unicode)

def myparser(elements):
	# date 
	for review_date in elements.cssselect ('.review-meta .date'):
		print html.tostring(review_date, method='text', encoding=unicode).strip()
	for x in elements.cssselect('.externalReview .review_comment'):
		print html.tostring(x, method='text',encoding=unicode)

if __name__ == '__main__':
	hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
	web_page= parse(hotel_url[0]).getroot()
	for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
		myparser(all_reviews)
