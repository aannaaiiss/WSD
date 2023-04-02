import spacy
nlp = spacy.load('fr_core_news_md')

context_before = []
context_after = []

sentence = ["mon","nom","est","Anaïs","oui","je", "crois", "que", "c'est", "une", "mauvaise", "idée", ",", "pas", "toi", "?","parce","que","cest","chaud","quand","même"]
i_instance = 15
print(sentence[i_instance])
print(sentence[:i_instance])
print(sentence[i_instance+1:])

if (len(sentence[:i_instance])>=10) :
        for i in range(1,11) :
            context_before.append(sentence[i_instance-i].lower())
else :
    for i in range(1,len(sentence[:i_instance])+1) :
       context_before.append(sentence[i_instance-i].lower())

if(len(sentence[i_instance+1:])>= 10) :
    for i in range(i_instance+1,i_instance+11):
        context_after.append(sentence[i].lower())
else :
    for i in range(i_instance+1,len(sentence)):
        print(sentence[i])
        context_after.append(sentence[i].lower())
        
for i in range(10-len(context_before)) :
    context_before.append("<d>")
        
for i in range(10-len(context_after)) :
    context_after.append("<f>")
        
print(context_before)
print(context_after)

for word in context_before :
    print(nlp(word))
    print(nlp(word)[0].lemma_)
