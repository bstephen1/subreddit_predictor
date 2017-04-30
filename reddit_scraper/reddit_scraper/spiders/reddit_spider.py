import scrapy

#spider that crawls through reddit getting data on posts

class RedditSpider(scrapy.Spider) :
	#name of the spider
	name = "reddit"
	
	#number of posts to scrape (MUST be a multiple of 25 -- only does
	#whole pages)
	#also this has to be a STRING
	posts = "50"

	#current page
	page = 0

	#all the subreddits it will crawl through
	start_urls = [
		"http://reddit.com/r/pcgaming/top/?sort=top&t=all",
		"https://www.reddit.com/r/nottheonion/top/?sort=top&t=all",
	]
	


	#main parser. Handles the main pages. Loads links to posts.
	def parse(self, response) :
		#get all the links to the posts from the main page
		for post in response.css("div.content div.thing a.comments::attr(href)").extract() : 
			yield scrapy.Request(response.urljoin(post), callback=self.parse_post)
		#load next page
		next_page = response.css("div.nav-buttons span.next-button a::attr(href)").extract_first()
		#stop when post limit is reached
		if "count="+self.posts not in next_page :
			yield scrapy.Request(response.urljoin(next_page), callback=self.parse)


	#parses individual posts
	def parse_post(self, response) :
		#all posts, and only children posts
		everything = response.css("div.commentarea div.usertext-body p::text").extract()
		children = response.css("div.commentarea div.child div.usertext-body p::text").extract()
		yield {
			'TITLE' : response.css("a.title::text").extract_first(),
			'COMMENT NUMBER' : response.css("div.content div.thing a.comments::text").extract_first(),
			'POST TYPE' : response.css("div.thing::attr(data-domain)").extract_first(),
			'SUBREDDIT' : response.css("div.thing::attr(data-subreddit)").extract_first(),
			'FLAIRS' : response.css("div.commentarea p.tagline span.flair::text").extract(),
			#only pulling the parent comments
			'COMMENTS' : [s for s in everything if s not in children]
		}
