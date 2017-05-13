from textblob import TextBlob
import ParamFunctions.py
import json
import sys

TITLE_ROUGEN_N = 2
TITLE_FLAIR_N = 2
COMMENT_FLAIR_N = 2
COMMENT_ROUGEN_N = 2


def main():

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
	disorgAllPosts = getFileDictList(sys.argv[i])

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
	
	
	#refSummaryFlair is a list of lists of strings
	#each list in refSummaryFlair corresponds to a subreddit
	#each element in the subreddit's list is a flair used for reference
	#This is used as the "summary" parameter when counting the number of common substrings in the flairs
	refSummaryFlair = []
	for subIndex in range(len(allSubs)):
		refSummaryFlair.append([])
		for dict in allSubs(subIndex):
			refSummaryFlair[subIndex].extend(dict["FLAIRS"])
	
	#refSummaryTitle is a list of lists of strings
	#each list in refSummaryTitle corresponds to a subreddit
	#each element in the subreddit's list is a title used for reference
	#This is used as the "summary" parameter when doing RougeN on the post titles
	refSummaryTitle = []
	for subIndex in range(len(allSubs)):
		refSummaryTitle.append([])
		for dict in allSubs(subIndex):
			refSummaryTitle[subIndex].extend(dict["TITLE"])
	
	#refSummaryComments is a list of lists of strings
	#each list in refSummaryComments corresponds to a subreddit
	#each element in the subreddit's list is a comment used for reference
	#This is used as the "summary" parameter when doing RougeN on the comments
	refSummaryComments = []
	for subIndex in range(len(allSubs)):
		refSummaryComments.append([])
		for dict in allSubs(subIndex):
			refSummaryComments[subIndex].extend(dict["COMMENTS"])
			
	#refSummaryTFlair is a list of lists of strings
	#each list in refSummaryTFlair corresponds to a subreddit
	#each element in the subreddit's list is a title flair used for reference
	#This is used as the "summary" parameter when counting the number of common substrings in the title flairs
	refSummaryTFlair = []
	for subIndex in range(len(allSubs)):
		refSummaryTFlair.append([])
		for dict in allSubs(subIndex):
			refSummaryTFlair[subIndex].extend(dict["TFLAIR"])
			
	featureListX = []
	featureListY = []
	for sub in allSubs:
		for postIndex in range(0,len(sub))
			featureListX.append([])
			featureListY.append(sub[postIndex]["SUBREDDIT"])
			#First feature: Self Post (1) or Link Post (0)
			featureListX[postIndex].append(float(sub[postIndex]["TYPE"]))
			#Second feature: Post score (Number of Upvotes - Number of Downvotes)
			featureListX[postIndex].append(float(sub[postIndex]["SCORE"]))
			#Third feature: Rouge-N values (for each possible label) of the post's title
			featureListX[postIndex].extend(getAllAvgRougeN(TITLE_ROUGEN_N,sub[postIndex]["TITLE"],refSummaryTitle))
			#Fourth feature: Sentiment (polarity and subjectivity) of the post's title
			featureList[postIndex].extend(getSentiment(sub[postIndex]["TITLE"]))
			#Fifth feature: Number of Common Substrings (of length greater than some given number)
			#				between the title flair and it's reference
			featureList[postIndex].extend(getAllAvgComSubstrCount(TITLE_FLAIR_N,sub[postIndex]["TFLAIR"],refSummaryTFlair))
			#Sixth feature: Average Sentiment (average polarity and average subjectivity) of the post's comments
			featureList[postIndex].extend(getAvgSentiment(sub[postIndex]["COMMENTS"]))
			#Seventh feature: Average Rouge-N values (for each possible label) of the post's comments
			featureListX[postIndex].extend(getAllAvgRougeN(COMMENT_ROUGEN_N,sub[postIndex]["COMMENTS"],refSummaryComments))
			#Eighth feature: Average Number of Common Substrings (of length greater than some given number)
			#				 between the comments' flair and their reference
			featureListX[postIndex].extebd(getAllAvgComSubstrCount(COMMENT_FLAIR_N,sub[postIndex["FLAIRS"],refSummaryFlair))
			
	
	
	
	
		
	
	

def getFileDictList(fileName):
	data = []
	with open(fileName) as f :
		#JSON line files have to be read line-by-line 
		for line in f :
			#appends each line to the end of @data
			data.append(json.loads(line))
	return data
	
main()