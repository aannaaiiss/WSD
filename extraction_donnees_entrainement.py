import re
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np

#paths à définir
data_path = "../donnees/FSE-1.1-191210/FSE-1.1.data.xml"
gold_path = "../donnees/FSE-1.1-191210/FSE-1.1.gold.key.txt"

#récupération des données XML
tree = ET.parse(data_path)
data_file = tree.getroot()[0]

#récupération des données .txt
gold_file = open(gold_path, "r",encoding="utf-8")

context_size = 4

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

def get_data_sets(instance2examples):
    
    """Builds the dictionary to get the sets from the instance.

    Args:
        instance (string)
        instance2examples (dictionary): associates the list of context vectors corresponding to the instance

    Returns:
        list of dictionary, list of ints: list of context vectors, list of gold 
    """
    instance2sets ={}
    for instance, examples in instance2examples.items():
        instance2sets[instance] = ([],[])
        for context, gold in examples :
            instance2sets[instance][0].append(context)
            instance2sets[instance][1].append(gold)
         
    return instance2sets

instances = list(instance2examples.keys())
print("nombre d'instances et instances présentes dans le corpus, ",len(instances),instances,"\n")

instance = instances[0]
examples = instance2examples[instance]
instance2sets = get_data_sets(instance2examples)
print(instance, ": nombre d'examples ", len(examples))

'''
#PROBLEME : Comment splitter en 80%, 10%, 10% des données quand il y a moins de 10 examples ?
#cross validation ?
def train_test_dev_split(X,y,train_size=0.8):
    """Inspired by the sklearn method train_test_split(). Returns the same lists but with the development ones added.
    

    Args:
        X (list): list of context vectors for one instance
        y (list): list of gold class for one instance. Indexes corresponds to the X's.
        train_size (float, optional): training set size. Defaults to 0.8.

    Returns:
        lists: sets to build the model
    """
    
    X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=train_size)
    
    #une fois les premiers sets obtenus, on split X_test et y_test en deux pour obtenir les sets de développement
    
    X_dev = X_test[:len(X_test)//2]
    X_test = X_test[len(X_test)//2:]
    y_dev = y_test[:len(X_test)//2]
    y_test = y_test[len(X_test)//2:]
    
    return X_train, X_test, X_dev, y_train, y_test, y_dev

X_train, X_test, X_dev, y_train, y_test, y_dev = train_test_dev_split(X,y)
'''

i2w = set()
for context,gold in examples :
    i2w.update(context)
i2w = list(i2w)
print("vocabulaire  des données d'entraînement du mot "+ instance,i2w,"\n")

file_embeddings = "embeddings.txt" #à définir

'''
#Code pour créer le fichier d'embeddings

fasstex_path = "../fasstex" #à définir
f = open(fasstex_path, "r", encoding="UTF-8")
word2vec = {}

f.readline() #permet de ne pas prendre en compte la première ligne du fichier qui résumé ce que contient le fichier
lines = f.readlines()


#On crée un fichier dans lequel on copie seulement les embeddings correspondantes aux mots du vocabulaire
with open(file_embeddings,"w",encoding="UTF-8") as f : 
        f.writelines([line for line in lines if line.split(" ")[0] in i2w])
'''
#Construction du dictionnaire qui va permettre de faire le lookup

path = "./"+file_embeddings #à définir

f = open(path, "r", encoding="UTF-8")

#On récupère dans le fichier crée les embeddings pour crée un dictionnaire
w2emb = {}
for line in f.readlines():
    splitted_line = line.split(" ")
    word = splitted_line[0]
    embedding = list(map(float,splitted_line[1:]))
    w2emb[word] = embedding

#look up

#A partir du dictionnaire, on crée un nouveau set d'examples
examples_embeddings = []

for context,gold in examples:
    
    emb_size = len(list(w2emb.values())[0]) #300
    context_emb = np.zeros(emb_size)
    #Le nouveau vecteur est similaire à l'ancien mais on a remplacé dans celui-ci chaque mot par son embedding correspondant
    #vector_embeddings = { word_ind : word2vec[vector[word_ind]] for word_ind in vector if word_ind in word2vec}
    for word in context :
        if word in w2emb :
            context_emb = np.add(context_emb, np.array(w2emb[word]))
            
    examples_embeddings.append((context_emb,gold))

#print("example n°1 with embeddings : ",examples_embeddings[0])

X,y = zip(*examples_embeddings)
X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.8)

clf = MLPClassifier(random_state=1,hidden_layer_sizes=(100,))
print('MLP')

clf.fit(X_train, y_train)
print(f'AND : {clf.predict(X_test) == y_test}')
