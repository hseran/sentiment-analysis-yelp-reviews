
import lxml.html
from lxml import html
from lxml.html import parse

#
#class to represent review information
#
class Review:
	#reviewers name
	def setReviewerName(self, name):
		self.reviewer_name = name
	
	def getReviewerName(self):
		return self.reviewer_name

	#number of friends reviewer has
	def setReviewerFriends(self, number_of_friends):
		self.reviewer_friends = number_of_friends

	def getReviewerFriends(self):
		return self.reviewer_friends
		
	#number of reviews user as written
	def setReviewsCount(self, number_of_reviews):
		self.reviewer_review_count = number_of_reviews
	
	#URL to reviewer's profile
	def setReviewerProfileURL(self, profileURL):
		self.reviewer_profile_URL = profileURL

	#date on which review was written
	def setReviewDate(self, reviewDate):
		self.review_date = reviewDate
	
	#review text
	def setReviewText(self, text):
		self.review_text = text

	#reviewer Location
	def setReviewerLocation(self, location):
		self.reviewer_location = location

	def setReviewRating(self, value):
		self.review_rating = value

	def printReview(self):
		print self.reviewer_name
		print self.reviewer_profile_URL
		print self.review_rating
		print self.review_date
		print self.review_text
		
#
#populates reviewer information
#
def populateReviewerInfo(reviewObj, element):

	#reviewer name
	#for x in element.cssselect('.externalReview .user-passport .user-passport-info .user-name a'):
	#	print html.tostring(x, method='text', encoding='unicode').strip()

	tempList = element.cssselect('.externalReview .user-passport .user-passport-info .user-name a')
	name = ''
	if (len(tempList) > 0):
		name = html.tostring(tempList[0], method='text', encoding='unicode').strip()
	
	reviewObj.setReviewerName(name)

	#reviewer location
	#for x in element.cssselect('.externalReview .user-passport .reviewer_info'):
	#	print html.tostring(x, method='text', encoding='unicode').strip()

	tempList = element.cssselect('.externalReview .user-passport .reviewer_info')
	location = ''
	if (len(tempList) > 0):
		location = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewerLocation(location)
	
	#reviewer URL
	#for x in element.cssselect('.externalReview .user-passport .user-passport-info .user-name a'):
	#	print x.get('href')

	tempList = element.cssselect('.externalReview .user-passport .user-passport-info .user-name a')
	profileURL = ''
	if (len(tempList) > 0):
		profileURL = tempList[0].get('href')
	
	reviewObj.setReviewerProfileURL(profileURL)

	# reviewer's friends
	#for x in element.cssselect('.externalReview .reviewer-details .user-stats .friend-count'):
	#	print html.tostring(x, method='text', encoding='unicode').strip()

	tempList = element.cssselect('.externalReview .reviewer-details .user-stats .friend-count')
	friendCount = ''
	if (len(tempList) > 0):
		friendCount = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewerFriends(friendCount)


    # number of reviews by user
	#for x in element.cssselect('.externalReview .reviewer-details .user-stats .review-count'):
	#	print html.tostring(x, method='text', encoding='unicode').strip()	

	tempList = element.cssselect('.externalReview .reviewer-details .user-stats .review-count')
	reviews = ''
	if (len(tempList) > 0):
		reviews = html.tostring(tempList[0], method='text', encoding='unicode').strip()

	reviewObj.setReviewsCount(friendCount)

	# rating
	#for x in element.cssselect('.externalReview .review-meta .rating meta'):
	#	print x.get('content')


#
#populates review specific information
#

def myparser(reviewObj, element):
	populateReviewerInfo(reviewObj, element);
	
	# date 
	#for review_date in elements.cssselect ('.review-meta .date'):
	#	print html.tostring(review_date, method='text', encoding=unicode).strip()

    #date
	tempList = element.cssselect('.review-meta .date')
	date = ''
	if (len(tempList) > 0):
		date = html.tostring(tempList[0], method='text', encoding=unicode).strip()

	reviewObj.setReviewDate(date)

	#for x in elements.cssselect('.externalReview .review_comment'):
	#	print html.tostring(x, method='text',encoding=unicode)
	
    #comment
	tempList = element.cssselect('.externalReview .review_comment')
	comment = ''
	if (len(tempList) > 0):
		comment = html.tostring(tempList[0], method='text', encoding=unicode).strip()

	reviewObj.setReviewText(comment)

	#rating
	tempList = element.cssselect('.externalReview .review-meta .rating meta')
	rating = ''
	if (len(tempList) > 0):
		rating = tempList[0].get('content')
    
	reviewObj.setReviewRating(rating)



if __name__ == '__main__':
	hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
	#web_page= parse(hotel_url[0]).getroot()
	#for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
	#	myparser(all_reviews)
	i=0
	while(i<=1360):
		#print i
		web_page= parse(hotel_url[0]+'?start='+str(i)).getroot()
		for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
			obj = Review()
			myparser(obj, all_reviews)
			obj.printReview()
		i=i+40
