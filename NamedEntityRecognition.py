from collections import Counter
featureMap = Counter()
sentences =[]

def readconll(file):
    lines = [line.strip() for line in open(file)]
    while lines[-1] == '':  # Remove trailing empty lines
        lines.pop()
    s = [x.split('_') for x in '_'.join(lines).split('__')]  # Quick split corpus into sentences
    return [[y.split() for y in x] for x in s]


##Training Begins####  
sentences = readconll('eng.train')
finalfeaturelist =[]   
classlist = []  
index =0
for sentence in sentences:
    index =0
    for word in sentence: 
        featureMap[("word="+word[0])] +=2   # Token as a feature
        featureMap[("POS="+word[1])] +=2    # POS as a feature
        featureMap[("hyphen="+str('-' in word[0]))] +=2 # Check for Hyphen as a feature
        if index > 0:
            featureMap[("IniCaps="+str(word[0][0].isupper()))] +=2 # Starting Character  as a feature
        if index == 0:
            featureMap[("FirstWordIniCaps="+str(word[0][0].isupper()))] +=2
        featureMap[("HasDigit="+str(any(char.isdigit() for char in word[0])))] +=1
        featureMap[("AlphaNum="+str(word[0].isalnum()))] +=2  
        featureMap[("BracketsQuotes="+str("\'" or ("[" and "]") or ("(" and ")") in word[0]))] +=2   
        featureMap[("WordPosition="+str(index))] +=1    # Word Position as a feature
        featureMap[("WordLength="+str(len(word[0])))] +=1   # Word length as a feature
        if index >=2:
            entity = sentence[index-1][3]
            if 'I-' in entity:
                entity = sentence[index-2][3]
            featureMap[("PrevEntity="+sentence[index-1][3])] +=2    # Previous Entity as a feature
            featureMap[("PrevToken="+sentence[index-1][0])] +=2     # Previous Word as a feature      
            featureMap[("PrevPOS="+sentence[index-1][1])] +=2       # Previous Part of Speech as a feature  
        if index < len(sentence)-1:
            featureMap[("NextPOS="+sentence[index+1][1])] +=2
            featureMap[("NextToken="+sentence[index+1][0])] +=2
        if index < len(sentence)-2:
            featureMap[("NextNextPOS="+sentence[index+1][1] + "||" + sentence[index+2][1])] +=2  
            featureMap[("NextNextToken="+sentence[index+1][0] + "||" + sentence[index+2][0])] +=2  

        if index > 1:
            featureMap[("PrePrePOS="+sentence[index-1][1] + "||" + sentence[index-2][1])] +=2       # Conacaenation of previous and its previous words
            featureMap[("PrePreToken="+sentence[index-1][0] + "||" + sentence[index-2][0])] +=2
            featureMap[("PrePreEntity="+sentence[index-1][3] + "||" + sentence[index-2][3])] +=2 
        
        if len(word[0]) > 1:
            for i in range(int(len(word[0])/2)-1, len(word[0])-1):
                featureMap[("suff=" +word[0][(i):(len(word[0]))])] +=1
            for i in range(0,int(len(word[0])/20)-1):
                featureMap[("pref=" +word[0][(i):(int(len(word[0])/2))])] +=1
        index= index+1
           
        finalfeaturelist.append(dict(featureMap))  # Add the featurevector for each word to a list
        classlist.append(word[3])                   # Add the class for the corresponding feature to a list
        featureMap.clear()
    
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm 
vectorizer = DictVectorizer(sparse = True)
X = vectorizer.fit_transform(finalfeaturelist)
clf = svm.LinearSVC()                             # use Linear SVM
clf.fit(X, classlist)                             # Modelling

##Training Ends####


### Testing Begins###
testsentences = readconll('eng.testa')
featureMap.clear()
for sentence in testsentences:
    index =0
    for word in sentence: 
        featureMap[("word="+word[0])] +=2 # Using the same featurees as that has been extracted in Training
        featureMap[("POS="+word[1])] +=2
        featureMap[("hyphen="+str('-' in word[0]))] +=2
        if index > 0:
            featureMap[("IniCaps="+str(word[0][0].isupper()))] +=2
        if index == 0:
            featureMap[("FirstWordIniCaps="+str(word[0][0].isupper()))] +=2
        featureMap[("HasDigit="+str(any(char.isdigit() for char in word[0])))] +=1
        featureMap[("AlphaNum="+str(word[0].isalnum()))] +=2    
        featureMap[("BracketsQuotes="+str("\'" or ("[" and "]") or ("(" and ")") in word[0]))] +=2   
        featureMap[("WordPosition="+str(index))] +=1 
        featureMap[("WordLength="+str(len(word[0])))] +=1          
        if index >=1:
            featureMap[("PrevEntity="+sentence[index-1][4])] +=2  # Using the predicted class and not the golden attribute for feature  
            featureMap[("PrevToken="+sentence[index-1][0])] +=2
            featureMap[("PrevPOS="+sentence[index-1][1])] +=2
        if index < len(sentence)-1:
            featureMap[("NextPOS="+sentence[index+1][1])] +=2
            featureMap[("NextToken="+sentence[index+1][0])] +=2
        
        if index < len(sentence)-2:
            featureMap[("NextNextPOS="+sentence[index+1][1] + "||" + sentence[index+2][1])] +=2        
            featureMap[("NextNextToken="+sentence[index+1][0] + "||" + sentence[index+2][0])] +=2 
    
        if index > 1:
            featureMap[("PrePrePOS="+sentence[index-1][1] + "||" + sentence[index-2][1])] +=2
            featureMap[("PrePreToken="+sentence[index-1][0] + "||" + sentence[index-2][0])] +=2
            featureMap[("PrePreEntity="+sentence[index-1][4] + "||" + sentence[index-2][4])] +=2    # Using the predicted class and not the golden attribute for feature        
        index= index+1
        if len(word[0]) > 1:
            for i in range(int(len(word[0])/2)-1, len(word[0])-1):
                featureMap[("suff=" +word[0][(i):(len(word[0]))])] +=1
            for i in range(0,int(len(word[0])/2)-1):
                featureMap[("pref=" +word[0][(i):(int(len(word[0])/2))])] +=1
        
        guessEntity = str(clf.predict(vectorizer.transform(dict(featureMap)))[0])   # prediction of class
        if guessEntity == "":
            guessEntity = 'O'
        word.append(guessEntity)    # Appending the predicted class to the testsenetences 
        featureMap.clear()
        
# Writing the sentences with the guessed Entity into a file
file_name = "eng.guessa"  
file = open(file_name, 'w+').close()
file = open(file_name, 'w+')
for testSentence in testsentences:
    for testword in testSentence:
        file.write(' '.join(testword) + '\n')
    file.write('\n')
file.close


