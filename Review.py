from lxml import etree
#
#class to represent review information
#
class Review(object):
	
	def __init__(self, docid):
		self.reviewId = docid
		self.polarity = None
		self.confidence = None
		self.reviewer_name = None
		self.reviewer_friends = 0
		self.reviewer_review_count = 0
		self.reviewer_profile_URL = None
		self.review_date = None
		self.review_text = None
		self.reviewer_location = None
		self.review_rating = 0
		self.reviewURL = None

	def getReviewId(self):
		return self.reviewId

	def getReviewText(self):
		return self.review_text
	
	def getReviewPolarity(self):
		return self.polarity
	
	def getReviewConfidence(self):
		return self.confidence
	
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
	
	def setPolarity(self, value):
		self.polarity = value

	def setConfidence(self, value):
		self.confidence = value

	def printReview(self):
		print self.reviewer_name
		print self.reviewer_profile_URL
		print self.review_rating
		print self.review_date
		print self.review_text

	@staticmethod
	def serializeToXML(listofreviews, outputfile):
		page = etree.Element("reviewDocs");
		xml = etree.ElementTree(page)
		for review in listofreviews:
			doc = etree.SubElement(page, 'doc', id = str(review.reviewId))
			stars = etree.SubElement(doc, 'stars')
			stars.text = str(review.review_rating)
			url = etree.SubElement(doc, 'url')
			url.text = review.reviewURL
			date = etree.SubElement(doc, 'date')
			date.text = review.review_date
			user = etree.SubElement(doc, 'user')
			user.text = review.reviewer_profile_URL
			rev = etree.SubElement(doc, 'review')
			rev.text = review.review_text
			polarity = etree.SubElement(doc, 'polarity')
			polarity.text = review.polarity if review.polarity != None else ""
			confidence = etree.SubElement(doc, 'confidence')
			confidence.text = review.confidence if review.confidence != None else ""

		out = open(outputfile, 'w')
		xml.write(out, xml_declaration=True, encoding='utf-16', pretty_print=True)

	@staticmethod
	def readReviewsFromXML(xmlfile):
		try:
			root = etree.parse(xmlfile)
		except IOError as e:
			print "I/O error({0}): {1}".format(e.errno, e.strerror)
			return
		#list to store all reviews
		reviews = []
		
		#iterate over all doc elements and extract review data
		for element in root.getiterator('doc'):
			review = Review(element.get('id'))
			review.setReviewDate(element.findtext('date'))
			review.setReviewText(element.findtext('review'))
			review.setReviewRating(element.findtext('stars'))
			review.setReviewerProfileURL(element.findtext('user'))
			review.setReviewURL(element.findtext('url'))
			review.setPolarity(element.findtext('polarity'))
			review.setConfidence(element.findtext('confidence'))
			reviews.append(review)
		return reviews

if __name__ == '__main__':
	reviews = []
	review = Review(1)
	review.setReviewDate('today')
	review.setReviewText('this hotel is great')
	review.setReviewRating('4')
	review.setReviewerName('naresh')
	review.setReviewerProfileURL('http://www.google.com')
	review.setReviewURL('http://ntu.edu.sg')
	reviews.append(review)
	review = Review(2)
	review.setReviewDate('tomorrow')
	review.setReviewText('this hotel is bad')
	review.setReviewRating('2')
	review.setReviewerName('suresh')
	review.setReviewerProfileURL('http://www2.google.com')
	review.setReviewURL('http://ntu2.edu.sg')
	reviews.append(review)
	Review.serializeToXML(reviews, 'test.xml')
