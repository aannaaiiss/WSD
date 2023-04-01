import re
import xml.etree.ElementTree as ET

data_path = "donnees/FSE-1.1-191210/wiktionary-190418.data.xml"
gold_path = "donnees/FSE-1.1-191210/wiktionary-190418.gold.key.txt"

tree = ET.parse(data_path)
data = tree.getroot()[0]

gold_file = open(gold_path, "r",encoding="utf-8")

X = []

for (sentence,gold_line) in zip(data,gold_file.readlines()) :
    
    #pour chaque phrase, on initialise deux listes qui permettront de respecter les tailles des contextes (+10,-10)
    context_before = []
    context_after = []
    context_vector = {}
    
    #on boucle sur les mots de la phrase pour construire les listes
    i_instance = 0
    while sentence[i_instance].tag != "instance" : 
        context_before.append(sentence[i_instance].text.lower())
        i_instance+=1
        
    context_vector["instance"] = sentence[i_instance].text.lower()

    for i in range(i_instance+1,len(sentence)):
        context_after.append(sentence[i].text.lower())
        
    #une fois les listes constituées, on ajoute les balises de début et de fin de phras    
    for i in range(10-len(context_before)) :
        context_before.insert(0,"<d>")
        
    for i in range(10-len(context_after)) :
        context_after.append("<f>")
        
    #on construit le vecteur de contexte à partir des listes finalisées
    for i in range(10):
        context_vector["next_word_"+str(i+1)] = context_after[i]
        
    for i in range(10):
        context_vector["previous_word_"+str(i+1)] = context_before[9-i]
        
    #on récupère ensuite le nombre associé au sens pour constuire l'exemple
    gold = int((re.findall("ws_[0-9]",gold_line)[0]).replace("ws_",""))
    
    X.append((context_vector,gold))
    
print(len(X))  
print(X[0])