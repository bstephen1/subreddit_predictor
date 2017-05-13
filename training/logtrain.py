from sklearn import linear_model
from sklearn.model_selection import cross_val_score
import json

#this file reads in formatted feature vectors from "training.jl" 
#and trains it using logistic regression

#NOTE: this file is completely untested

#set up the model
log = linear_model.LogisticRegression()

#get the data
#raw format has class label as last element
posts = []
with open("training.jl") as f :
	for line in f :
		posts.append(json.loads(line))

#convert raw format to X and Y vectors
X_train = []
Y_train = []
for post in posts :
	X_train.append(post[:-1])
	Y_train.append(post[-1])

#train
model = log.fit(X_train, Y_train)

#train with cross validation
cvscores = cross_val_score(log, X_train, Y_train, cv=5)
print(cvscores)
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))




