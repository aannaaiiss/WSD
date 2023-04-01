'''
from bs4 import BeautifulSoup

with open("donnees/FSE-1.1-191210/wiktionary-190418.data.xml", "r",encoding="utf8") as file :
    data = file.read()

bs_data = BeautifulSoup(data, "xml")
    
X_train = []
    
print(bs_data.find("sentence"))
#for sentence in bs_data.find_all("sentence") :
#     print(sentence)
'''
path = "donnees/FSE-1.1-191210/wiktionary-190418.data.xml"
import xml.etree.ElementTree as ET
tree = ET.parse(path)
root = tree.getroot()  
print(root.tag)

corpus = root
text = root[0]

sentence1 = text[0]

'''
context_before = []
context_after = []
instance_id = 0

for i in range(len(sentence1)) :
    if sentence1[i].tag != "instance" : 
        context_before.append(sentence1[i].text.lower())
    else :
        instance_id = i
        instance = sentence1[i].text.lower()
        break

for i in range(len(sentence1)-(instance_id+1)):
    context_after.append(sentence1[i+instance_id+1].text.lower())

for i in range(10-len(context_before)) :
    context_before.insert(0,"<d>")
    
for i in range(10-len(context_after)) :
    context_after.append("<f>")
    
context_before.append(instance)
context_before.extend(context_after) 
print(context_before)
'''
'''
context_vector = {"previous_cont" : [], "next_cont" : []}
instance_id = 0

for i in range(len(sentence1)) :
    if sentence1[i].tag != "instance" : 
        context_vector["previous_cont"].append(sentence1[i].text.lower())
    else :
        instance_id = i
        context_vector["instance"] = sentence1[i].text.lower()
        break

for i in range(len(sentence1)-(instance_id+1)):
    context_vector["next_cont"].append(sentence1[i+instance_id+1].text.lower())

for i in range(10-len(context_vector["previous_cont"])) :
    context_vector["previous_cont"].insert(0,"<d>")
    
for i in range(10-len(context_vector["next_cont"])) :
    context_vector["next_cont"].append("<f>")
    
print(context_vector)
'''

X = []

for sentence in text :
    
    #pour chaque phrase, on initialise deux listes qui permettront de respecter les tailles des contextes (+10,-10)
    context_before = []
    context_after = []
    instance_id = 0

    #on boucle sur les mots de la phrase et on break lorsqu'on arrive à l'instance
    for i in range(len(sentence)) :
        if sentence1[i].tag != "instance" : 
            context_before.append(sentence1[i].text.lower())
        else :
            instance_id = i
            instance = sentence1[i].text.lower()
            break

    for i in range(len(sentence1)-(instance_id+1)):
        context_after.append(sentence1[i+instance_id+1].text.lower())

    for i in range(10-len(context_before)) :
        context_before.insert(0,"<d>")
        
    for i in range(10-len(context_after)) :
        context_after.append("<f>")
        
    context_vector = {}
    context_vector["instance"] = instance

    for i in range(10):
        context_vector["next_word_"+str(i+1)] = context_after[i]
        
    for i in range(10):
        context_vector["previous_word_"+str(i+1)] = context_before[9-i]
        
    print(context_vector)