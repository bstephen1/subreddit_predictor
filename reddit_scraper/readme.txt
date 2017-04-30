
Reddit spider is fully operational. The spider (reddit_spider.py) can crawl through n pages 
  from any number of subreddits.
Usage: scrapy crawl reddit 
Note: to edit which subreddits the spider crawls through, add them into the @urls field. To 
  edit how many pages it pulls, edit the @pages field (25 posts per page).
  
Format of output:
  TITLE : title of the post
  TOTAL COMMENTS : the total number of comments (int)
  POST TYPE : the domain the post links to. If it is "self.<SUBREDDIT>", it is a self post.
  SUBREDDIT : the subreddit the post belongs to (name of the subreddit, eg, "pcgaming")
  FLAIRS : a list containing all the user flairs from the post
  COMMENTS : a list containing all the top-level comments from the top 200 comments in the post
Each post is stored on a single line as a dictionary containing the above key : value pairs. 
