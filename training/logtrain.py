from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import json
import sys

#this file reads in formatted feature vectors from "training.jl" 
#and trains it using logistic regression

#usage: logtrain.py [trainingfile.jl] [testingfile.jl]
#first parameter is required. second is optional 
argc = len(sys.argv)
argv = sys.argv
if argc > 3 or argc < 2 :
	print("Usage: logtrain.py [trainingfile.jl] [testingfile.jl]")
	sys.exit()

#set up the model
log = linear_model.LogisticRegression()

#get the data
#raw format has class label as last element
def getData(f) :
	posts = []
	with open(argv[1]) as f :
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
if argc == 2 :
	X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=.1, random_state=1)

else :
	test = getData(argv[2])
	X_train = X_data
	Y_train = Y_data
	X_test = test[0]
	Y_test = test[1]
	

#train
model = log.fit(X_train, Y_train)

#record results to file 
f = open("results.txt", "a")
extra = argv[2] if argc == 3 else "None"
f.write("Train: %s :: Test: %s :: Acc: %f\n" % (argv[1], extra, log.score(X_test,Y_test)))

#prints actual class label vs prediction
for x in range(len(Y_test)) :
	print("Actual: %f :: Predicted: %f :: x: %d" % (Y_test[x], model.predict([X_test[x]]), x))
print("Accuracy over test data: %f" % log.score(X_test,Y_test))


#cross validation seemed to decrease accuracy 
"""
#train with cross validation
cvscores = cross_val_score(log, X_train, Y_train, cv=5)
print(cvscores)
print("Accuracy: %0.2f (+/- %0.2f)" % (cvscores.mean(), cvscores.std() * 2))
"""


