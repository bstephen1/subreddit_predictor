from textblob import TextBlob
import json
import sys
from sklearn.feature_extraction.text import CountVectorizer



def getTrainingData(fileName):

	#Contains a dictionary of the subreddits and their corresponding list index
	subRedditDict = {}

	#allSubs is a list of lists of dictionaries
	#each list in allSubs corresponds to a subreddit
	#each element in the subreddit is a post
	#the post is a dictionary with the following values:
	#	TITLE, SCORE, TFLAIR, TOTAL, TYPE, SUBREDDIT, FLAIRS, COMMENTS
	allSubs = []
	#for i in range(1,len(sys.argv)):
	#	allSubs.append(getFileDictList(sys.argv[i]))
	
	#all of the posts in one list
	disorgAllPosts = getFileDictList(fileName)

	#fills allSubs with the subreddits and their posts
	currentIndex = 0
	for post in disorgAllPosts:
		if post["SUBREDDIT"] in subRedditDict:
			allSubs[subRedditDict[post["SUBREDDIT"]]].append(post)
		else:
			subRedditDict[post["SUBREDDIT"]] = currentIndex
			currentIndex += 1
			allSubs.append([])
			allSubs[subRedditDict[post["SUBREDDIT"]]].append(post)
	
	vectorizerFitDataTitle = []
	vectorizerFitDataTFlair = []
	vectorizerFitDataFlairs = []
	vectorizerFitDataComments = []
	
	for subReddit in allSubs:
		for post in subReddit:
			vectorizerFitDataTitle.append(post["TITLE"])
			vectorizerFitDataTFlair.append(post["TFLAIR"])
			vectorizerFitDataFlairs.extend(post["FLAIRS"])
			vectorizerFitDataComments.extend(post["COMMENTS"])
			
	titleVectorizer = CountVectorizer(stop_words='english')
	tFlairVectorizer = CountVectorizer(stop_words='english')
	flairsVectorizer = CountVectorizer(stop_words='english')
	commentsVectorizer = CountVectorizer(stop_words='english')
	
	titleVectorizer.fit(vectorizerFitDataTitle)
	tFlairVectorizer.fit(vectorizerFitDataTFlair)
	flairsVectorizer.fit(vectorizerFitDataFlairs)
	commentsVectorizer.fit(vectorizerFitDataComments)
	
	trainingData = []
	
	for subReddit in allSubs:
		for post in subReddit:
			postData = []
			
			postTitle = []
			postTitle.append(post["TITLE"])
			postData.extend(titleVectorizer.transform(postTitle))
			
			postTFlair = []
			postTFlair.append(post["TFLAIR"])
			postData.extend(tFlairVectorizer.transform(postTFlair))
			
			postFlairsString = ""
			for flair in post["FLAIRS"]:
				postFlairsString += " " + flair
			postFlairs = []
			postFlairs.append(postFlairsString)
			postData.extend(flairsVectorizer.transform(postFlairs))
			
			postCommentsString = ""
			for comment in post["COMMENTS"]:
				postCommentsString += " " + flair
			postComments = []
			postComments.append(postCommentsString)
			postData.extend(commentsVectorizer.transform(post["COMMENTS"]))
			
			postData.append(subRedditDict[post["SUBREDDIT"]])
			
			trainingData.append(postData)
			
			return trainingData, titleVectorizer, tFlairVectorizer, flairsVectorizer, commentsVectorizer




def getFileDictList(fileName):
	data = []
	with open(fileName) as f :
		#JSON line files have to be read line-by-line 
		for line in f :
			#appends each line to the end of @data
			data.append(json.loads(line))
	return data
	
def getPostParams(post, titleVectorizer, tFlairVectorizer, flairsVectorizer, commentsVectorizer):
	postData = []
	
	postTitle = []
	postTitle.append(post["TITLE"])
	postData.extend(titleVectorizer.transform(postTitle))
			
	postTFlair = []
	postTFlair.append(post["TFLAIR"])
	postData.extend(tFlairVectorizer.transform(postTFlair))
			
	postFlairsString = ""
	for flair in post["FLAIRS"]:
		postFlairsString += " " + flair
	postFlairs = []
	postFlairs.append(postFlairsString)
	postData.extend(flairsVectorizer.transform(postFlairs))
			
	postCommentsString = ""
	for comment in post["COMMENTS"]:
		postCommentsString += " " + flair
	postComments = []
	postComments.append(postCommentsString)
	postData.extend(commentsVectorizer.transform(post["COMMENTS"]))
			
	postData.append(subRedditDict[post["SUBREDDIT"]])
	
	return postData
	
print(getTrainingData(sys.argv[1])[0])