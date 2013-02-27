
import lxml.html
from lxml import html
from lxml.html import parse

#
#class to represent review information
#
class Review:
	
	def __init__(self, docid):
		self.reviewId = docid
	
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

	def setReviewURL(self, value):
		self.reviewURL = value;

	def printReview(self):
		print self.reviewer_name
		print self.reviewer_profile_URL
		print self.review_rating
		print self.review_date
		print self.review_text

	def serializeToXML(self):
		temp = []
		temp.append('<doc id=' + str(self.reviewId) + '>')
		temp.append('<stars>' + str(self.review_rating) + '</stars>')
		temp.append('<url>' + self.reviewURL + '</url>')
		temp.append('<date>' + self.review_date + '</date>')
		temp.append('<user>' + self.reviewer_profile_URL + '</user>')
		#temp.append('<title/>')
		temp.append('<review>' + self.review_text + '</review>')
		temp.append('<polarity>NULL</polarity>')
		temp.append('<confidence></confidence>')
		temp.append('</doc>')
		return '\n'.join(temp)


#
#
# CRAWLER CODE BELOW THIS
#


		
		
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

    # review URL
    #for x in element.cssselect('.externalReview .reviewer-details .user-stats .review-count'):
    #   print html.tostring(x, method='text', encoding='unicode').strip()   

	tempList = element.cssselect('.externalReview .externalReviewActions a.i-orange-link-common-wrap')
	reviewURL = ''
	if (len(tempList) > 0):
		reviewURL = "http://www.yelp.com" + tempList[0].get('href')

	reviewObj.setReviewURL(reviewURL)

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

file_location = "../reviews.xml"

if __name__ == '__main__':
	hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
	#web_page= parse(hotel_url[0]).getroot()
	#for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
	#	myparser(all_reviews)
	
	#variable to loop through pages
	i=0
	#variable to assign doc id to reviews
	objCount = 1;
	#we store our reviews temporarily in this before we write to file
	buffer = []
	#add <xml> to the buffer for the first time
	buffer.append('<xml>')

	while(i<=1360):
		web_page= parse(hotel_url[0]+'?start='+str(i)).getroot()
		for review in web_page.cssselect('#bizReviews .externalReview'):
			obj = Review(objCount)
			myparser(obj, review)
			buffer.append(obj.serializeToXML())
			objCount += 1
		i=i+40
	buffer.append('</xml>')

	print len(buffer)

	#write reviews to xml file
	f = open(file_location, 'w')
	f.write('\n'.join(buffer).encode('utf-8').strip())
