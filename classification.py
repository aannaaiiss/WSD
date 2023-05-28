import re
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.metrics import accuracy_score
import random

creer_fichier_embeddings = False

#1) Extraction des données d'entraînement

#Eléments à définir
data_path = "../donnees/FSE-1.1-191210/FSE-1.1.data.xml"
gold_path = "../donnees/FSE-1.1-191210/FSE-1.1.gold.key.txt"
context_size = 4
embeddings_path = "embeddings.txt" #Saisir le path du fichier existant ou le nom de celui qui sera crée dans le cas échéant

#récupération des données XML
tree = ET.parse(data_path)
data_file = tree.getroot()[0]

#récupération des données .txt
gold_file = open(gold_path, "r",encoding="utf-8")

def extract_examples(data_file, gold_file):
    """Extract the data from the files.

    Args:
        data_file (Element): Sentences
        gold_file (TextIOWrapper): Golds keys

    Returns:
        dictionary: associates the list of context vectors corresponding to the instance
    """
    
    instance2examples={}
    
    for (sentence,gold_line) in zip(data_file,gold_file.readlines()) :
        
        #pour chaque phrase, on initialise deux listes qui permettront de respecter les tailles des contextes (+10,-10)
        context_before = []
        context_after = []
        context = []
        
        #on boucle sur les mots de la phrase pour construire les listes
        #on cherche l'instance et on repart en arrière pour constuire le contexte avant
        i_instance = 0
        while sentence[i_instance].tag != "instance" : 
            i_instance+=1
        
        instance = sentence[i_instance].attrib["lemma"].lower()
        
        if instance not in instance2examples : 
            instance2examples[instance] = []
        
        #on vérifie la longueur des phrases pour ne pas soulever d'erreur
        
        #context_before 
        
        #si le contexte avant l'instance est supérieur ou égale à la taille du contexte choisie
        #on ajoute à la liste chaque mot aux index from i-instance-1 to i_instance-5
        if (len(sentence[:i_instance])>=context_size) :
                for i in range(1,context_size+1) :
                    context_before.append(sentence[i_instance-i].text.lower())
        
        #sinon, on ajoute à la liste tous les mots et on ajoutera des balises pour compléter
        else :
            for i in range(1,len(sentence[:i_instance])+1) :
                context_before.append(sentence[i_instance-i].text.lower())

        #context_after
        
        #si le contexte après l'instance est supérieur ou égale à la taille du contexte choisie
        #on ajoute à la liste chaque mot aux index from i-instance+1 to i_instance+11
        if(len(sentence[i_instance+1:])>= context_size) :
            for i in range(i_instance+1,i_instance+(context_size+1)):
                context_after.append(sentence[i].text.lower())
        
        #sinon, on ajoute à la liste tous les mots et on ajoutera des balises pour compléter
        else :
            for i in range(i_instance+1,len(sentence)):
                context_after.append(sentence[i].text.lower())
        
        #une fois les listes constituées, on ajoute les balises de début et de fin de phrase si nécessaire
        for i in range(context_size-len(context_before)) :
            context_before.append("<d>")
            
        for i in range(context_size-len(context_after)) :
            context_after.append("<f>")
            
        #le vecteur sera une concaténation des contextes d'avant et d'après
        context = context_before
        context.append(instance)
        context.extend(context_after)
            
        #on récupère ensuite le nombre associé au sens pour constuire l'exemple
        gold = int((re.findall("ws_[0-9]",gold_line)[0]).replace("ws_",""))
        
        instance2examples[instance].append((context,gold))
        
    return instance2examples

instance2examples = extract_examples(data_file,gold_file)

instances = list(instance2examples.keys())
print("nombre d'instances présentes dans le corpus: ",len(instances),"\n")
print("instance et taille des données d'entraînement",[(instance,len(instance2examples[instance])) for instance in instance2examples],"\n")

#2) Facultatif : script pour créer le fichier texte ne comportant que les embeddings qui nous intéressent - plus rapide

if creer_fichier_embeddings :
    #Element à définir
    fasstex_path = "../fasstex" 

    #création du vocabulaire du corpus entier
    i2w = set()
    for instance,examples in instance2examples.items():
        for context,gold in examples :
            i2w.update(context)
    i2w = list(i2w)

    f = open(fasstex_path, "r", encoding="UTF-8")
    f.readline() #permet de ne pas prendre en compte la première ligne du fichier qui résumé ce que contient le fichier
    lines = f.readlines()

    with open(embeddings_path,"w",encoding="UTF-8") as f : 
            f.writelines([line for line in lines if line.split(" ")[0] in i2w])

#3) Construction du dictionnaire qui va nous permettre de faire le look up (matrice d'embeddings)

def extract_embeddings(path_embeddings) :
    f = open(path_embeddings , "r", encoding="UTF-8")

    #On récupère dans le fichier crée les embeddings pour créer un dictionnaire
    w2emb = {}
    for line in f.readlines():
        splitted_line = line.split(" ")
        word = splitted_line[0]
        embedding = list(map(float,splitted_line[1:]))
        w2emb[word] = embedding
    return w2emb

w2emb = extract_embeddings(embeddings_path)
#4) Sélection des instances pour la classification et opération de look up pour chacune d'elle

#Elément à définir
instances_to_test = instances[:3]

def look_up(context, w2emb) :
    emb_size = len(list(w2emb.values())[0]) #on récupère la taille d'un embedding : 300
    context_emb = np.zeros(emb_size)
    for word in context :
        if word in w2emb :
            context_emb = np.add(context_emb, np.array(w2emb[word]))             
    return context_emb

#5) Classification tests

size_data = [1,0.8,0.6,0.4,0.2]
clf = MLPClassifier(random_state=1,hidden_layer_sizes=(1000,)) 

for size in size_data :
    
    print(f'{size*100}% données annotées considérées')
    
    for instance in instances_to_test :
            
        print("instance :",instance)
            
        examples = instance2examples[instance]
        selected_examples = random.choices(examples,k=round(size*len(examples)))
        X = [look_up(context,w2emb)for context,gold in selected_examples]
        y = [gold for context,gold in selected_examples]
            
        X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.8)
            
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        print("nombre de données annotées : ", len(X))
        print("prédiction :", y_pred)
        print("gold :",y_test)
        print("accuracy score : ", accuracy_score(y_pred,y_test),"\n")




    


