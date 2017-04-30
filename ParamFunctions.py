from textblob import TextBlob


#Input:
#	an list of strings to find avg sentiment of
#Return:
#	a tuple of the average sentiment formatted as (polarity, subjectivity)
def getAvgSentiment(testList):
	
	avgSentiment = (0,0)
	
	for testStr in testList:
		testSentiment = getSentiment(testStr)
		avgSentiment[0] += testSentiment[0]
		avgSentiment[1] += testSentiment[1]
	
	avgSentiment = avgSentiment/len(testList)
	return avgSentiment

#Input:
#	a string to find the avg sentiment of
#Return:
#	a tuple of the sentiment formatted as (polarity, subjectivity)
def getSentiment(testStr):
	return TextBlob(testStr).sentiment

#Input:
#	an int n that denotes the value for n-grams
#	an list of strings to find the average RougeN of
#	a list of the different summary string lists
#Return:
#	a list containing the average RougeNs of the different summary string lists
def getAllAvgRougeN(n, testList, summaryList):
	allAvgRougeN = []
	for summary in summaryList:
		allAvgRougeN.append(getAvgRougeN(n, testList, summary))
	return allAvgRougeN

#Input:
#	an int n that denotes the value for n-grams
#	a string to find the RougeN of
#	the list of strings used for the summary for comparison	against the test string
#Return:
#	the average RougeN of the list of strings
def getAvgRougeN(n, testList, summary):
	nGramSummary = []
	for item in summary:
		nGramSummary.extend(TextBlob(item).grams(n))
	avgRougeN = 0
	for testStr in testList:
		avgRougeN += getRougeN(n, testStr, nGramSummary)
	avgRougeN = avgRougeN/len(testList)
	return avgRougeN

#Input:
#	an int n that denotes the value for n-grams
#	a string to find the RougeN of
#	a list of all the n-grams in the summary
#Return:
#	the RougeN of the input string
def getRougeN(n, testStr, nGramSummary):
	rougeN = 0
	testNGrams = TextBlob(testStr).ngrams(n)
	for nGram in testNGrams:
		rougeN += nGramSummary.count(nGram)
	rougeN = rougeN/len(nGramSummary)
	return rougeN

#Input:
#	an int n that deenotes the shortest allowed substring
#	a list of strings to find the average common substring count of
#	a list of the different summary string lists
#Return:
#	a list of the average common substring counts for the list of test strings for each summary string list
def getAllAvgComSubstrCount(n, testList, summaryList):
	allAvgComSubstrCount = []
	for summary in summaryList:
		allAvgComSubstrCount.append(n, getAvgRougeN(testList, summary))
	return allAvgComSubstrCount

#Input:
#	an int n that deenotes the shortest allowed substring
#	a list of strings to find the average common substring count of
#	a summary string list used for comparison against the test string
#Return:
#	the average common substring count for given summary string list and test strings
def getAvgComSubstrCount(n, testList, summary):
	substrSummary = []
	for item in summary:
		substrSummary.extend(getAllSubstr(n, item))
	avgComSubstrCount = 0
	for testStr in testList:
		avgComSubstrCount += getComSubstrCount(testStr, substrSummary)
	avgComSubstrCount = avgComSubstrCount/len(testList)
	return avgComSubstrCount

#Input:
#	an int n that deenotes the shortest allowed substring
#	a test string to find the common substring count of when compared to the substring summary
#	the list of all of the substrings for the summary
#Return:
#	the common substring count for the given substring summary and test string
def getComSubstrCount(n, testStr, substrSummary):
	comSubstrCount = 0
	testSubstr = getAllSubstr(n, testStr)
	for substr in testSubstr:
		comSubstrCount += substrSummary.count(substr)
	#comSubstrCount = comSubstrCount/(substrSummary)
	return comSubstrCount

#Input:
#	an int n that denotes the shortest allowed substring
#	a string to find all the substrings of
#Return:
#	a list of all the substrings of at least length n in the input string
def getAllSubstr(n, inputStr):
	length = len(inputStr)
	return [inputStr[i:j + 1] for i in xrange(length) for j in xrange(i + (n-1),length)]


