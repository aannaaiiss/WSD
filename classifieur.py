from collections import defaultdict
import re
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import numpy as np
from sklearn.metrics import accuracy_score
import random

#A définir
data_path = "../donnees/FSE-1.1-191210/FSE-1.1.data.xml"
gold_path = "../donnees/FSE-1.1-191210/FSE-1.1.gold.key.txt"
context_size = 4
embeddings_path = "embeddings.txt" #Saisir le path du fichier existant ou le nom de celui qui sera crée dans le cas échéant
#_________________________________________________________________________________________________________________
class Classifieur :
    
    def __init__(self,data_path,gold_path,embeddings_path):
        
        #récupération des données XML
        tree = ET.parse(data_path)
        data_file = tree.getroot()[0]

        #récupération des données .txt
        gold_file = open(gold_path, "r",encoding="utf-8")
        
        self.w2examples, self.w2senses = self.extract_examples_and_senses(data_file,gold_file)
        self.w2emb = self.extract_embeddings(embeddings_path)
    
    def extract_examples_and_senses(data_file, gold_file):
        """Extract the data from the files.

        Args:
            data_file (Element): Sentences
            gold_file (TextIOWrapper): Golds keys

        Returns:
            dictionary: associates the list of context vectors corresponding to the instance
            dictionary : associates to the word each senses
        """
    
        w2examples={}
        w2senses = defaultdict(set)
        
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
            
            if instance not in w2examples : 
                w2examples[instance] = []
            
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
                
            #on récupère ensuite le nombre associé au sens pour constuire l'exemple + ajouter au dictionnaire w2sense
            gold = int((re.findall("ws_[0-9]",gold_line)[0]).replace("ws_",""))
            
            w2senses[instance].add(gold)
            w2examples[instance].append((context,gold))
            
            return w2examples,w2senses
    
    def extract_embeddings(path_embeddings) :
        """Récupère les embeddings dans le fichier générée.

        Args:
            path_embeddings (string)

        Returns:
            dictionnary: Associe à chaque mot son embedding
        """
        f = open(path_embeddings , "r", encoding="UTF-8")

        #On récupère dans le fichier crée les embeddings pour créer un dictionnaire
        w2emb = {}
        for line in f.readlines():
            splitted_line = line.split(" ")
            word = splitted_line[0]
            embedding = list(map(float,splitted_line[1:]))
            w2emb[word] = embedding
        return w2emb

    def look_up(context, w2emb) :
        """Remplace dans le vecteur de contexte les mots par leur embedding.

        Args:
            context (list): liste de taille (size_window*2)+1
            w2emb (dictionnary): Associe à chaque mot son embedding

        Returns:
            list : liste de taille size_embedding : BOW
        """
        emb_size = len(list(w2emb.values())[0]) #on récupère la taille d'un embedding : 300
        context_emb = np.zeros(emb_size)
        for word in context :
            if word in w2emb :
                context_emb = np.add(context_emb, np.array(w2emb[word]))             
        return context_emb
    
    def select_examples(examples,senses,size):
        """Choisit des examples d'entraînement représentatifs du corpus.

        Args:
            examples (list)
            n_senses (int): nombre de senses associés à l'instance
            size (float): quantité des données d'entraînement considérés

        Returns:
            list: examples qui contiennent au moins un example de chaque sense
        """
        selected_examples = []
        
        #Pour chaque sens, on ajoute un example associé à ce sens ,au hasard
        for sense in senses :
            selected_examples.append(random.choice(list(filter((lambda example:example[1]==sense),examples))))
        
        #On calcule ensuite le nombre d'examples qu'il reste à ajouter pour atteindre la quantité de données souhaitée
        size_to_add = round(size*(len(examples)))-len(selected_examples)
        
        #On ajoute ce nombre de données (non-présentes déjà dans la liste) selectionnées au hasard
        selected_examples.extend(random.choices(list(filter((lambda example : example not in selected_examples),examples)),k=size_to_add))
        
        return selected_examples

    def classify(self,instance,data_size) :
        
        print("instance :",instance)
        print(f'{data_size*100}% des données annotées considérées')
        
        clf = MLPClassifier(random_state=1,hidden_layer_sizes=(1000,)) 
        
        selected_examples = self.select_examples(self.w2examples[instance],self.w2senses[instance],data_size)
        X = [self.look_up(context,self.w2emb)for context,gold in selected_examples]
        y = [gold for context,gold in selected_examples]
            
        X_train, X_test, y_train, y_test = train_test_split(X,y,train_size=0.8)
            
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        print("nombre de données annotées : ", len(X))
        print("prédiction :", y_pred)
        print("gold :",y_test)
        print("accuracy score : ", accuracy_score(y_pred,y_test),"\n")
        
        return y_pred
    
#_____________________________________________________________________________________________________________

myClassif = Classifieur(data_path,gold_path,embeddings_path)
myClassif.classify("aboutir",0.8)