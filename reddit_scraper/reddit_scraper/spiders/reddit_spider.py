import scrapy
import re

#spider that crawls through reddit getting data on posts

class RedditSpider(scrapy.Spider) :
	#name of the spider
	name = "reddit"
	
	#number of pages to scrape 
	#set this to 2 for training dat (top all time), 1 for testing (top month)
	pages = 1

	#all the subreddits it will crawl through
	start_urls = [
		#TRAINING DATA (TOP OF ALL TIME)
		#"https://reddit.com/r/pcgaming/top/?sort=top&t=all",
		#"https://www.reddit.com/r/nottheonion/top/?sort=top&t=all",
		#"https://www.reddit.com/r/mildlyinteresting/top/?sort=top&t=all",
		#"https://www.reddit.com/r/overwatch/top/?sort=top&t=all",
		#"https://www.reddit.com/r/hearthstone/top/?sort=top&t=all",
		#"https://www.reddit.com/r/nintendoswitch/top/?sort=top&t=all",
		#"https://www.reddit.com/r/animalsbeingderps/top/?sort=top&t=all",
		#"https://www.reddit.com/r/crappydesign/top/?sort=top&t=all",
		#"https://www.reddit.com/r/cinemagraphs/top/?sort=top&t=all",
		#"https://www.reddit.com/r/writingprompts/top/?sort=top&t=all",
		#"https://www.reddit.com/r/explainlikeimfive/top/?sort=top&t=all",
		#"https://www.reddit.com/r/space/top/?sort=top&t=all",
		#"https://www.reddit.com/r/wholesomememes/top/?sort=top&t=all",
		#"https://www.reddit.com/r/nevertellmetheodds/top/?sort=top&t=all",
		#"https://www.reddit.com/r/floridaman/top/?sort=top&t=all",
		#"https://www.reddit.com/r/holdmybeer/top/?sort=top&t=all",
		#"https://www.reddit.com/r/evilbuildings/top/?sort=top&t=all",
		#"https://www.reddit.com/r/kenm/top/?sort=top&t=all",
		#"https://www.reddit.com/r/fitness/top/?sort=top&t=all",
		#"https://www.reddit.com/r/babyelephantgifs/top/?sort=top&t=all",
		#"https://www.reddit.com/r/dadjokes/top/?sort=top&t=all",
		#"https://www.reddit.com/r/maliciouscompliance/top/?sort=top&t=all",
		#"https://www.reddit.com/r/wheredidthesodago/top/?sort=top&t=all",
		#"https://www.reddit.com/r/thathappened/top/?sort=top&t=all",
		#"https://www.reddit.com/r/askreddit/top/?sort=top&t=all",
		#"https://www.reddit.com/r/aww/top/?sort=top&t=all",
		#"https://www.reddit.com/r/outoftheloop/top/?sort=top&t=all",
		#"https://www.reddit.com/r/talesfromretail/top/?sort=top&t=all",
		#"https://www.reddit.com/r/oldpeoplefacebook/top/?sort=top&t=all",
		#"https://www.reddit.com/r/whatcouldgowrong/top/?sort=top&t=all",

		#TESTING DATA (TOP OF THE MONTH)
		#"https://reddit.com/r/pcgaming/top/?sort=top&t=month",
		#"https://www.reddit.com/r/nottheonion/top/?sort=top&t=month",
		#"https://www.reddit.com/r/mildlyinteresting/top/?sort=top&t=month",
		#"https://www.reddit.com/r/overwatch/top/?sort=top&t=month",
		#"https://www.reddit.com/r/hearthstone/top/?sort=top&t=month",
		#"https://www.reddit.com/r/nintendoswitch/top/?sort=top&t=month",
		#"https://www.reddit.com/r/animalsbeingderps/top/?sort=top&t=month",
		#"https://www.reddit.com/r/crappydesign/top/?sort=top&t=month",
		#"https://www.reddit.com/r/cinemagraphs/top/?sort=top&t=month",
		#"https://www.reddit.com/r/writingprompts/top/?sort=top&t=month",
		#"https://www.reddit.com/r/explainlikeimfive/top/?sort=top&t=month",
		#"https://www.reddit.com/r/space/top/?sort=top&t=month",
		#"https://www.reddit.com/r/wholesomememes/top/?sort=top&t=month",
		#"https://www.reddit.com/r/nevertellmetheodds/top/?sort=top&t=month",
		#"https://www.reddit.com/r/floridaman/top/?sort=top&t=month",
		#"https://www.reddit.com/r/holdmybeer/top/?sort=top&t=month",
		#"https://www.reddit.com/r/evilbuildings/top/?sort=top&t=month",
		#"https://www.reddit.com/r/kenm/top/?sort=top&t=month",
		#"https://www.reddit.com/r/fitness/top/?sort=top&t=month",
		#"https://www.reddit.com/r/babyelephantgifs/top/?sort=top&t=month",
		#"https://www.reddit.com/r/dadjokes/top/?sort=top&t=month",
		#"https://www.reddit.com/r/maliciouscompliance/top/?sort=top&t=month",
		#"https://www.reddit.com/r/wheredidthesodago/top/?sort=top&t=month",
		#"https://www.reddit.com/r/thathappened/top/?sort=top&t=month",
		#"https://www.reddit.com/r/askreddit/top/?sort=top&t=month",
		#"https://www.reddit.com/r/aww/top/?sort=top&t=month",
		#"https://www.reddit.com/r/outoftheloop/top/?sort=top&t=month",
		#"https://www.reddit.com/r/talesfromretail/top/?sort=top&t=month",
		#"https://www.reddit.com/r/oldpeoplefacebook/top/?sort=top&t=month",
		"https://www.reddit.com/r/whatcouldgowrong/top/?sort=top&t=month",
	]
	


	#main parser. Handles the main pages. Loads links to posts.
	def parse(self, response) :
		#get all the links to the posts from the main page
		for post in response.css("div.content div.thing a.comments::attr(href)").extract() : 
			yield scrapy.Request(response.urljoin(post), callback=self.parse_post)
		#load next page
		next_page = response.css("div.nav-buttons span.next-button a::attr(href)").extract_first()
		#stop when page limit is reached
		if "count="+str(self.pages * 25) not in next_page :
			yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


	#parses individual posts
	def parse_post(self, response) :
		#all comments, and only child comments (used to find parents)
		everything = response.css("div.commentarea div.usertext-body p::text").extract()
		children = response.css("div.commentarea div.child div.usertext-body p::text").extract()
		#used to get total number of comments
		com_num = response.css("div.content div.thing a.comments::text").extract_first()
		#used to find post type (link or self)
		post_link = response.css("div.thing::attr(data-domain)").extract_first()
		subreddit = response.css("div.thing::attr(data-subreddit)").extract_first()
		#used to find the number of upvotes
		score = response.css("div.side span.number::text").extract_first()
		yield {
			'TITLE' : response.css("a.title::text").extract_first(),
			'SCORE' : int(''.join([x for x in score if x != ','])),
			'TFLAIR' : response.css("span.linkflairlabel::text").extract_first(),
			'TOTAL' : int(re.search(r'\d+', com_num).group()),
			'TYPE' : 1 if post_link	== "self." + subreddit else 0,
			'SUBREDDIT' : subreddit,
			'FLAIRS' : response.css("div.commentarea p.tagline span.flair::text").extract(),
			#only pulling the parent comments
			'COMMENTS' : [s for s in everything if s not in children]
		}
