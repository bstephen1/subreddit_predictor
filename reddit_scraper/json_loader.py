import json

#sample code showing how to read the JSON line data files

#array to store each line
data = []
with open("gamingoniondata.jl") as f :
	#JSON line files have to be read line-by-line 
	for line in f :
		#appends each line to the end of @data
		data.append(json.loads(line))

#each element in @data is a post, represented as a dict
print(data[0]["TITLE"])
