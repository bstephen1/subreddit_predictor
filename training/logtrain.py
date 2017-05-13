from sklearn import linear_model
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import json

#this file reads in formatted feature vectors from "training.jl" 
#and trains it using logistic regression

#NOTE: this file is completely untested

#set up the model
log = linear_model.LogisticRegression()

#get the data
#raw format has class label as last element
posts = []
with open("askderp.jl") as f :
	for line in f :
		posts.append(json.loads(line))

#convert raw format to X and Y vectors
X_data = []
Y_data = []
for post in posts :
	X_data.append(post[:-1])
	Y_data.append(post[-1])

#set a portion of the training data as testing samples
X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=.1, random_state=1)

#train
model = log.fit(X_train, Y_train)

#print stats
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


