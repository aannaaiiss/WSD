import re
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split

#paths à définir
data_path = "donnees/FSE-1.1-191210/wiktionary-190418.data.xml"
gold_path = "donnees/FSE-1.1-191210/wiktionary-190418.gold.key.txt"

#récupération des données XML
tree = ET.parse(data_path)
data_file = tree.getroot()[0]

#récupération des données .txt
gold_file = open(gold_path, "r",encoding="utf-8")

instance2examples = {} 
context_size = 10

def extract_examples(data_file, gold_file):
    """Extract the data from the files.

    Args:
        data_file (Element): Sentences
        gold_file (TextIOWrapper): Golds keys

    Returns:
        dictionary: associates the list of context vectors corresponding to the instance
    """
    
    for (sentence,gold_line) in zip(data_file,gold_file.readlines()) :
        
        #pour chaque phrase, on initialise deux listes qui permettront de respecter les tailles des contextes (+10,-10)
        context_before = []
        context_after = []
        context_vector = {}
        
        #on boucle sur les mots de la phrase pour construire les listes
        #on cherche l'instance et on repart en arrière pour constuire le contexte avant
        i_instance = 0
        while sentence[i_instance].tag != "instance" : 
            i_instance+=1
        
        instance = sentence[i_instance].attrib['lemma'].lower()
        context_vector["instance"] = instance
        
        if instance not in instance2examples : 
            instance2examples[instance] = []
        
        #on vérifie la longueur des phrases pour ne pas soulever d'erreur
        
        #context_before 
        
        #si le contexte avant l'instance est supérieur ou égale à la taille du contexte choisie
        #on ajoute à la liste chaque mot aux index from i-instance-1 to i_instance-11
        if (len(sentence[:i_instance])>=context_size) :
                for i in range(1,context_size+1) :
                    context_before.append(sentence[i_instance-i].attrib['lemma'].lower())
        
        #sinon, on ajoute à la liste tous les mots et on ajoutera des balises pour compléter
        else :
            for i in range(1,len(sentence[:i_instance])+1) :
                context_before.append(sentence[i_instance-i].attrib['lemma'].lower())

        #context_after
        
        #si le contexte après l'instance est supérieur ou égale à la taille du contexte choisie
        #on ajoute à la liste chaque mot aux index from i-instance+1 to i_instance+11
        if(len(sentence[i_instance+1:])>= context_size) :
            for i in range(i_instance+1,i_instance+(context_size+1)):
                context_after.append(sentence[i].attrib['lemma'].lower())
        
        #sinon, on ajoute à la liste tous les mots et on ajoutera des balises pour compléter
        else :
            for i in range(i_instance+1,len(sentence)):
                context_after.append(sentence[i].attrib['lemma'].lower())
        
        #une fois les listes constituées, on ajoute les balises de début et de fin de phrase si nécessaire
        for i in range(context_size-len(context_before)) :
            context_before.append("<d>")
            
        for i in range(context_size-len(context_after)) :
            context_after.append("<f>")
            
        #on construit le vecteur de contexte à partir des listes finalisées
        for i in range(context_size):
            context_vector["next_word_"+str(i+1)] = context_after[i]
            
        for i in range(context_size):
            context_vector["previous_word_"+str(i+1)] = context_before[i]
            
        #on récupère ensuite le nombre associé au sens pour constuire l'exemple
        gold = int((re.findall("ws_[0-9]",gold_line)[0]).replace("ws_",""))
        
        instance2examples[instance].append((context_vector,gold))
        
    return instance2examples

instance2examples = extract_examples(data_file,gold_file)

def get_data_sets(instance,instance2examples):
    
    """Returns the sets corresponding to the instance.

    Args:
        instance (string)
        instance2examples (dictionary): associates the list of context vectors corresponding to the instance

    Returns:
        list of dictionary, list of ints: list of context vectors, list of gold 
    """
    X=[]
    y=[]
    for (context_vector, gold) in instance2examples[instance]:
        X.append(context_vector)
        y.append(gold)

    return X,y

X, y = get_data_sets("2.0", instance2examples)

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

print(len(X_train), len(X_test), len(X_dev))


      
    