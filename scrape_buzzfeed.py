import requests
import Queue
import time

src = "lukelewis/gifs-that-scream-friday-afternoon"

def diff(a, b):
	b = set(b)
	return [aa for aa in a if aa not in b]

def find_other_gif_articles(gif_article):
	gif_articles = []
	
	source = requests.get("http://www.buzzfeed.com/"+gif_article)
	
	related_strings = source.content.split('rel:gt_act="related-link/name"')

	for mess in related_strings[1:]:
		href_idx = mess.find('href="')
		if href_idx > 0:
			href_mess = mess[href_idx+7:]
			href = href_mess[0:href_mess.find('"')]
			if href.find('gif') > 0:
				gif_articles.append(href)
				
	return gif_articles
	

def crawl_for_gif_pages(source, limit=1000, delay=0.5):

	found = []

	sources = []
	sources.append(source)

	while (len(found)<limit and len(sources)>0):
		source = sources.pop()
		print "Searching from ", source
		print str(len(found))+"found so far"
		
		
		new_article_candidates = find_other_gif_articles(source)
		new_articles = diff(new_article_candidates, found)
		
		found.extend(new_articles)
		sources.extend(new_articles)
		
		time.sleep(delay)
		
	return found

print crawl_for_gif_pages(src)
		
		
		
