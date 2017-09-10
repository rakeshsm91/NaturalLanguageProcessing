# -*- coding: utf-8 -*-
#"""
#Created on Sun Nov 13 19:37:37 2016
#
#@author: rakes
#"""


import numpy as np
from sklearn.preprocessing import normalize
from collections import Counter
from sklearn.cluster import KMeans

#Read the lines from the file without considering blank lines
def readconll(file):
    lines = [line.strip() for line in open(file)]
    while lines[-1] == '':  # Remove trailing empty lines
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]  # Quick split corpus into sentences
    return [[y.split() for y in x] for x in s]
    

freqWordMap = Counter()
freqwordList =[]
leftVector = Counter()
rightVector = Counter()
rightVectorList =[]
leftVectorList = []
finalVectorList =[]
clusterafterkmeans = {}
words =[]
uniquewordList =[]
vectorList =[]

lines = readconll("wsj00-18.tag")  # read sentences from the wsj00-18.tag file

for sentences in lines:
    for word in sentences:
        words.append(word[0]) #read all the words and put it in a list
        
for word in words:
    freqWordMap[word.lower()] +=1
    
for word in sorted(freqWordMap,key=freqWordMap.get,reverse=True): #sort the list with descending frequent words 
    uniquewordList.append(word)

topfreqWordList = uniquewordList[:1000]  # Take the top 1000 most frequent words

for clustWord in topfreqWordList:      # Obtain the left vector and the right vector
    i=0
    for i in range(0,len(words)-1):
        if words[i] == clustWord:
            if i != 0:
                leftVector[(clustWord,words[i-1])] +=1  # Left vector containing the word left to the clusterword
            if i != len(words)-1:
                rightVector[(clustWord,words[i+1])] +=1  # right vector containing the word right to the clusterword
                
for clustWord in topfreqWordList:     # Obtain the final vector list for each top
    vectorList = []
    leftVectorList = []
    rightVectorList = []
    for word in uniquewordList:
        leftVectorList.append(leftVector.get((clustWord,word),0))   
        rightVectorList.append(rightVector.get((clustWord,word),0))
        
    vectorList = leftVectorList + rightVectorList
    finalVectorList.append(vectorList)

vec = np.array(finalVectorList) 
X = np.array(normalize(vec, axis=1, norm='l1'))  # Normalize the final vector list to 1
kmeans = KMeans(n_clusters=25, random_state=0).fit(X) # Applying Kmeans to the normalized vector


for word, cluster in zip(topfreqWordList,kmeans.labels_):  # Mapping the clusternumbers to its corresponding word
    clusterafterkmeans.setdefault(cluster,[]).append(word)

for i in clusterafterkmeans:        # display the cluster and the words
    print(i, clusterafterkmeans[i])