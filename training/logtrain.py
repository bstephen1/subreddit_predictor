from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import json
import sys
import time

#this file reads in formatted feature vectors from "training.jl" 
#and trains it using logistic regression

#usage: logtrain.py [trainingfile.jl] [testingfile.jl]
#first parameter is required. second is optional 
start = time.time()
argc = len(sys.argv)
argv = sys.argv
if argc > 3 or argc < 2 :
	print("Usage: logtrain.py [trainingfile.jl] [testingfile.jl]")
	sys.exit()

#set up the model
log = linear_model.LogisticRegression()

#get the data
#raw format has class label as last element
def getData(arg) :
	posts = []
	with open(arg) as f :
		for line in f :
			posts.append(json.loads(line))
	#convert raw format to X and Y vectors
	X_data = []
	Y_data = []
	for post in posts :
		X_data.append(post[:-1])
		Y_data.append(post[-1])
	return [X_data, Y_data]

#get the training data
train = getData(argv[1])
X_data = train[0]
Y_data = train[1]	

#set a portion of the training data as testing samples
#only if no separate test file is given
#DEPRECATED -- not needed when doing CV
"""
if argc == 2 :
	X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0)
"""
X_train = X_data
Y_train = Y_data

#else :
if argc == 3 :
	test = getData(argv[2])
	#X_train = X_data
	#Y_train = Y_data
	X_test = test[0]
	Y_test = test[1]
	

#train
model = log.fit(X_train, Y_train)

#record results to file 
f = open("results.txt", "a")
extra = argv[2] if argc == 3 else "None"
f.write("Train: %s :: Test: %s :: " % (argv[1], extra))
print("Train: %s :: Test: %s" % (argv[1], extra))


#prints actual class label vs prediction
#used when there is a separate file for test data
if argc == 3 : 
	mis = 0
	for x in range(len(Y_test)) :
		act = Y_test[x]
		pred = model.predict([X_test[x]])
		if act != pred :
			#clogs up the console too much
			#print("Actual: %f :: Predicted: %f" % (act, pred))
			mis += 1
	score = log.score(X_test,Y_test)
	print("Test instances: %d :: Misclassified: %d" % (len(Y_test), mis))
	print("Accuracy over test data: %f" % score)
	f.write("Mis: %d :: All: %d :: Acc: %0.2f\n" % (mis, len(Y_test), score))

#estimate accuracy with cross validation
#used when there is no test data
if argc == 2 :
	folds = 10
	cvscores = cross_val_score(log, X_train, Y_train, cv=folds)
	print(cvscores)
	print("Accuracy: %0.2f (+/- %0.2f)" % (cvscores.mean(), cvscores.std() * 2))
	f.write("CV %d-fold acc: %0.2f (+/- %0.2f)\n" % (folds, cvscores.mean(), cvscores.std() * 2))


#timing for program execution
end = time.time() - start
print("Time: %f seconds\n" % end)


