from textblob import TextBlob
import pickle
import json
import sys
from sklearn.feature_extraction.text import CountVectorizer

def main():

	fileNameFile = sys.argv[1]
	value = int(sys.argv[2])
	#print(type(sys.argv[1:]))
	
	fileNames = []
	
	for line in open(fileNameFile):
		fileNames.append('data\\' + line.rstrip('\n'))
	print(fileNames)
	
	trainFiles(fileNames, value)

def trainFiles(fileNames, num):

	trainingData, titleVectorizer, tFlairVectorizer, flairsVectorizer, commentsVectorizer = getTrainingData(fileNames[:num])

	ID = ""
	
	for index in range(num):
		ID += fileNames[index][5:-3]
	
	for subIndex in range(len(trainingData)):
		for postIndex in range(0,len(trainingData[subIndex])):
			trainingData[subIndex][postIndex] = int(trainingData[subIndex][postIndex])
	writeTrainingData(trainingData, ID)
	writeVectorizerLibrary(titleVectorizer, tFlairVectorizer, flairsVectorizer, commentsVectorizer, ID)

def getTrainingData(fileNames):

	if (type(fileNames) is not list):
		print("Parameter for funciton getTrainingData() must be a list of filenames.")
		print("Now exiting...")
		sys.exit()

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
	disorgAllPosts = []
	for fileName in fileNames:
		try:
			disorgAllPosts.extend(getFileDictList(fileName))
		except:
			print("Error reading file. Name of file is: ")
			#print(file)
			sys.exit()
			
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
			if(post["TFLAIR"] == None):
				post["TFLAIR"] = "null"
			vectorizerFitDataTFlair.append(post["TFLAIR"])
			if(post["FLAIRS"] == []):
				post["FLAIRS"] = ["null"]
			vectorizerFitDataFlairs.extend(post["FLAIRS"])
			vectorizerFitDataComments.extend(post["COMMENTS"])
			
	titleVectorizer = CountVectorizer(stop_words = 'english')#, max_df=.8, min_df=.001)
	tFlairVectorizer = CountVectorizer(stop_words = 'english')
	flairsVectorizer = CountVectorizer(stop_words = 'english')
	commentsVectorizer = CountVectorizer(stop_words = 'english')#, max_df=.8, min_df=.001)
	
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
			data = titleVectorizer.transform(postTitle)
			denseData = data.toarray()
			#print(denseData)
			postData.extend(denseData[0])
			
			postTFlair = []
			postTFlair.append(post["TFLAIR"])
			data = tFlairVectorizer.transform(postTFlair)
			denseData = data.toarray()
			#print(denseData)
			postData.extend(denseData[0])
			
			postFlairsString = ""
			for flair in post["FLAIRS"]:
				postFlairsString += " " + flair
			postFlairs = []
			postFlairs.append(postFlairsString)
			data = flairsVectorizer.transform(postFlairs)
			denseData = data.toarray()
			#print(denseData)
			postData.extend(denseData[0])
			
			
			postCommentsString = ""
			for comment in post["COMMENTS"]:
				postCommentsString = postCommentsString + " " + comment
			postComments = []
			postComments.append(postCommentsString)
			data = commentsVectorizer.transform(postComments)
			denseData = data.toarray()
			#print(denseData)
			postData.extend(denseData[0])
			
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
	data = titleVectorizer.transform(postTitle)
	denseData = data.toarray()
	postData.extend(denseData[0])
	
	postTFlair = []
	postTFlair.append(post["TFLAIR"])
	data = tFlairVectorizer.transform(postTFlair)
	denseData = data.toarray()
	postData.extend(denseData[0])
	
	postFlairsString = ""
	for flair in post["FLAIRS"]:
		postFlairsString += " " + flair
	postFlairs = []
	postFlairs.append(postFlairsString)
	data = flairsVectorizer.transform(postFlairs)
	denseData = data.toarray()
	postData.extend(denseData[0])
	
	
	postCommentsString = ""
	for comment in post["COMMENTS"]:
		postCommentsString = postCommentsString + " " + comment
	postComments = []
	postComments.append(postCommentsString)
	data = commentsVectorizer.transform(postComments)
	denseData = data.toarray()
	postData.extend(denseData[0])
	
	postData.append(subRedditDict[post["SUBREDDIT"]])
	
	return postData
	
def writeTrainingData(trainingData, ID):

	outfileName = 'trainingData' + ID + '.jl'

	with open(outfileName, 'w') as outfile:
		for post in trainingData:
			json.dump(post, outfile)
			outfile.write('\n')
	
	return

def writeVectorizerLibrary(titleVectorizer, tFlairVectorizer, flairsVectorizer, commentsVectorizer, ID):

	outfileName = 'vectorizerLibraries' + ID + '.pkl'

	with open(outfileName, 'w') as outfile:
		pickle.dump(titleVectorizer, outfile)
		pickle.dump(tFlairVectorizer, outfile)
		pickle.dump(flairsVectorizer, outfile)
		pickle.dump(commentsVectorizer, outfile)
		

main()