from collections import Counter
transcount = Counter()
unigramcount = Counter()
emissioncount = Counter()
transprob = {}
emissionprob ={}
tags = []
mytags =[]

lines = [line.strip() for line in open('wsj00-18.tag')]
for l in lines:
    if '\t' in l:
        tags.append(l.split('\t')[1])
    else:
        tags.append(l)
    
lines1 = [line.strip() for line in open('wsj00-18.tag') if '\t' in line]
wordtags = [(l.split("\t")[0],l.split("\t")[1]) for l in lines1]

start =0;
for tag in tags:
    if start ==0:
        mytags.append('<s>')
        start = 1
    if tag == '':
        mytags.append('</s>')
        mytags.append('<s>')
    else:
         mytags.append(tag)
mytags = mytags[0:len(mytags) -1]

for i, j in zip(mytags, mytags[1:]):
    bigramtag = (i,j)
    transcount[bigramtag] +=1
    unigramcount[i]+=1
    
for tag in transcount:
    transprob[tag] = transcount[tag]/unigramcount[tag[1]]
    
for wordtag in wordtags:
    emissiontuple = (wordtag[0],wordtag[1])
    emissioncount[emissiontuple] +=1
    
for wordtag in emissioncount:
    emissionprob[wordtag] = emissioncount[wordtag]/unigramcount[wordtag[1]]
    
    
def viterbi(sentence, transprob, emissionprob):
    sentence.insert(len(sentence),"</s>")     
    sentence.insert(0,"<s>") 
    iterations = [] 
    trellis = {}
    POSList = []
    nodeprob ='nodeProbability'
    trellisstate ='trellisState'
    states = unigramcount.keys()
    
    for i in range(0,len(sentence)):
        iterations.insert(i,i)   
    for iterate in iterations:
        for state in states:
            trellis[(state,iterate)]={nodeprob:0,trellisstate:''}
    trellis[('<s>',0)][nodeprob] = 1
    for iterate, iterate_next, word in zip(iterations,iterations[1:],sentence[1:]):
        for curr_state in states:
            for next_state in states:
                old_prob = trellis[(next_state,iterate_next)][nodeprob]
                old_state = trellis[(next_state,iterate_next)][trellisstate]
                                                
                emission_prob = emissionprob.get((word,next_state),0)
                trans_prob = transprob.get((curr_state,next_state),0)
                
                if word == '</s>' and next_state == '</s>':
                    emission_prob = 1
				
                new_prob = trans_prob * emission_prob*  trellis[(curr_state,iterate)][nodeprob]
                new_state = curr_state
                if old_prob < new_prob:
                    trellis[(next_state, iterate_next)] = {nodeprob:new_prob, trellisstate:new_state}    
                else:
                    trellis[(next_state, iterate_next)] = {nodeprob:old_prob, trellisstate:old_state}  
    storedstate = '</s>'
    for iterate in list(reversed(iterations))[:(len(sentence) - 2)]:
        storedstate = trellis[(storedstate,iterate)].get(trellisstate)
        POSList.append(storedstate)
    return list(reversed(POSList))
  
print(viterbi(['This','is','a','sentence','.'], transprob, emissionprob))
print(viterbi(['This','might','produce','a','result','if','the','system','works','well','.'], transprob, emissionprob))
print(viterbi(['Can','a','can','can','a','can','?'], transprob, emissionprob))
print(viterbi(['Can','a','can','move','a','can','?'], transprob, emissionprob))
print(viterbi(['Can','you','walk','the','walk','and','talk','the','talk','?'], transprob, emissionprob))

            
            
            
        
        
    