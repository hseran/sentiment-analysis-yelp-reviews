from Review import Review

if __name__ == '__main__':
	Review.serializeToXML(Review.readReviewsFromXML('../low-rating-reviews.xml'), '../test.xml')
