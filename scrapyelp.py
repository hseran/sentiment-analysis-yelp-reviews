
import lxml.html
from lxml import html
from lxml.html import parse

def myparser(elements):
    for x in elements.cssselect('.externalReview .review_comment'):
      print html.tostring(x, method='text',encoding=unicode)

if __name__ == '__main__':
   hotel_url= ['http://www.yelp.com/biz/morimoto-new-york']   
   web_page= parse(hotel_url[0]).getroot()
   for all_reviews in web_page.cssselect('#bizReviews .externalReview'):
	  myparser(all_reviews)
