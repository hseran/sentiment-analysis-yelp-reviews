import time
import lxml.html
from lxml import html
from lxml.html import parse
from Review import Review

#
#populates reviewer information
#
def populateReviewerInfo(reviewObj, element):

	#reviewer name

	tempList = element.cssselect('.externalReview .user-passport .user-passport-info .user-name a')
	name = ''
	if (len(tempList) > 0):
		name = html.tostring(tempList[0], method='text', encoding='unicode').strip()
	
	reviewObj.setReviewerName(name)

	#reviewer location

	tempList = element.cssselect('.externalReview .user-passport .reviewer_info')
	location = ''
	if (len(tempList) > 0):
		location = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewerLocation(location)
	
	#reviewer URL

	tempList = element.cssselect('.externalReview .user-passport .user-passport-info .user-name a')
	profileURL = ''
	if (len(tempList) > 0):
		profileURL = tempList[0].get('href')
	
	reviewObj.setReviewerProfileURL(profileURL)

	# reviewer's friends

	tempList = element.cssselect('.externalReview .reviewer-details .user-stats .friend-count')
	friendCount = ''
	if (len(tempList) > 0):
		friendCount = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewerFriends(friendCount)


    # number of reviews by user

	tempList = element.cssselect('.externalReview .reviewer-details .user-stats .review-count')
	reviews = ''
	if (len(tempList) > 0):
		reviews = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewsCount(friendCount)

    # review URL

	tempList = element.cssselect('.externalReview .externalReviewActions a.i-orange-link-common-wrap')
	reviewURL = ''
	if (len(tempList) > 0):
		reviewURL = "http://www.yelp.com" + tempList[0].get('href')

	reviewObj.setReviewURL(reviewURL)


#
#populates review specific information
#

def myparser(reviewObj, element):
	populateReviewerInfo(reviewObj, element);
	

    #date
	tempList = element.cssselect('.review-meta .date')
	date = ''
	if (len(tempList) > 0):
		date = html.tostring(tempList[0], method='text', encoding=unicode).strip()

	reviewObj.setReviewDate(date)

	
    #comment
	tempList = element.cssselect('.externalReview .review_comment')
	comment = ''
	if (len(tempList) > 0):
		tempElement = html.fragment_fromstring(html.tostring(tempList[0]).replace('<br>', ' ').replace('<br/>', ' ').replace('<BR>', ' ').replace('<BR/>', ' '))
		comment = html.tostring(tempElement, method='text', encoding=unicode).strip()
		
	reviewObj.setReviewText(comment)

	#rating
	tempList = element.cssselect('.externalReview .review-meta .rating meta')
	rating = ''
	if (len(tempList) > 0):
		rating = tempList[0].get('content')
    
	reviewObj.setReviewRating(rating)

#global variables
file_location = "../reviews.xml"
high_rating_location = "../high-rating-reviews.xml"
low_rating_location = "../low-rating-reviews.xml"
mid_rating_location = "../mid-rating-reviews.xml"

if __name__ == '__main__':
	hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
	
	#variable to loop through pages
	i=0
	#variable to assign doc id to reviews
	objCount = 1
	hCount = 0
	mCount = 0
	lCount = 0
	#we store our reviews temporarily in this before we write to file
	buffer = []
	hBuffer = []
	lBuffer = []
	mBuffer = []

	#crawl in a loop
	while(i<=1500):
		web_page= parse(hotel_url[0]+'?start='+str(i)).getroot()
		for review in web_page.cssselect('#bizReviews .externalReview'):
			obj = Review(objCount)
			myparser(obj, review)
			buffer.append(obj)
			if float(obj.review_rating) > 3:
				hBuffer.append(obj)
				hCount += 1
			elif float(obj.review_rating) < 3:
				lBuffer.append(obj)
				lCount += 1
			else:
				mBuffer.append(obj)
				mCount += 1
			objCount += 1
		i=i+40
		print objCount
		#if we crawl too fast, site comes up with captcha
		time.sleep(10)
	
	Review.serializeToXML(buffer, file_location)
	Review.serializeToXML(hBuffer, high_rating_location)
	Review.serializeToXML(lBuffer, low_rating_location)
	Review.serializeToXML(mBuffer, mid_rating_location)
	print "high: " + str(hCount) + " low: " + str(lCount) + " mid: " + str(mCount)

