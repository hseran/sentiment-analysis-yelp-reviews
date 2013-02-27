
import lxml.html
from lxml import html
from lxml.html import parse

def myparser(elements):
	# date 
	for review_date in elements.cssselect ('.review-meta .date'):
		print html.tostring(review_date, method='text', encoding=unicode).strip()
	for x in elements.cssselect('.externalReview .review_comment'):
		print html.tostring(x, method='text',encoding=unicode)

if __name__ == '__main__':
	hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
	i=0
	while(i<=1360):
		print i
		web_page= parse(hotel_url[0]+'?start='+str(i)).getroot()
		for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
			myparser(all_reviews)
		i=i+40
