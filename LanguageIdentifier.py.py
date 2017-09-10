import codecs
import math   
import collections     

classes = ['de','en','nl','sv']

texts = {}
alphabet = set()
wl ={}
prob = {}
probs ={}
unigram ={}
unigamCount = {}
bigram ={}
bigramCount ={}
sentenceBigram ={}
smoothfactor = 0.5

def classify(probs, classes, mysentence):
    totalprobabilty ={}
    for lang in classes:
                sentenceBigram[lang] = ["".join(seq) for seq in zip(list(mysentence), list(mysentence)[1:])]                
                for i in sentenceBigram[lang]:
                    totalprobabilty[lang] = totalprobabilty.get(lang,0) + math.log((probs.get(lang).get(i, 0) + smoothfactor )/(probs.get(lang).get(i[0],0)+1))
                    
                print(lang,totalprobabilty.get(lang), end =" ")
    print("\n")

for lang in classes:
    texts[lang] = [line.strip() for line in codecs.open(lang,'r',encoding='utf-8')][0]
    alphabet |= {unigram for unigram in texts[lang]} 
    
 
for lang in classes:
    unigram[lang] = list(texts.get(lang))
    unigamCount[lang] = collections.Counter(unigram[lang])
    bigram[lang] = ["".join(seq) for seq in zip(unigram[lang], unigram[lang][1:])]
    bigramCount[lang] = collections.Counter(bigram[lang])
    probs[lang] = unigamCount[lang].copy()
    probs[lang].update(bigramCount[lang])
    

classify(probs, classes, u'this is a very short text')
classify(probs, classes, u'dies ist ein sehr kurzer text')
classify(probs, classes, u'dit is een zeer korte tekst')
classify(probs, classes, u'detta är en mycket kort text')


    

    
    
    