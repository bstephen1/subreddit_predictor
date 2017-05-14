#
#this file runs logtrain.py using the training and testing data files
#

trn="trainingData"
tst="testingData"
ext=".jl"

for i in {2..30}
do
	training="$trn$i$ext"
	testing="$tst$i$ext"
	python logtrain.py $training
	python logtrain.py $training $testing
		
done

