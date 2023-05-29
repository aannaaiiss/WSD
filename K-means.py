import numpy as np
import torch
import pandas as pd
import random

class K_Means():
    ''' 
    classifieur K-means pour un mot particulier
    '''

    def __init__(self, examples):
        '''
        Instancie les différentes variables utiles pour l'algorithme du K-means

        examples : liste d'examples dont le mot à désambiguiser est le même pour 
                   chaque example
        example : couple d'un mot avec son contexte de fenêtre 4 (sous forme 
                  d'embedding) et du numéro de sens attendu du mot à désambiguiser 
                  (gold class sous forme d'integer)
                    si example = ([1.9, 2.3, 0.6], 1),
                    - le contexte avec le mot à désambiguiser et son lemme est 
                      l'embedding [1.9, 2.3, 0.6]
                    - le numéro de sens est 1
        '''

        # transforme l'ensemble des examples en une liste pour pouvoir garder le 
        # même indice pour chaque example par la suite
        self.examples = list(examples)
        # transforme les embeddings en tensors
        self.tensors_examples = [example[0] for example in self.examples]
        # détermine le nombre de sens possibles k (donc le nombre de clusters) 
        # à l'aide des données
        self.k = self.nb_senses()
        # initialisation de centroids : pour chaque sens, un example est pris au hasard
        self.tensors_centroids = [random.choice(example) 
                                  for example in self.examples_of_same_sense().values()]
        # initialisation de clusters : tous les examples sont associés au cluster 0
        self.clusters = np.zeros(len(examples))

    def nb_senses(self):
        '''
        Renvoie le nombre de sens existants dans un ensemble d'examples
        '''

        known_senses = []
        # pour chaque exemple
        for example in self.examples:
            # si le sens attendu (gold class) n'a pas encore été rencontré
            if example[1] not in known_senses:
                # l'ajoute à la liste des sens possibles
                known_senses.append(example[1])
        # renvoie le nombre de sens
        return len(known_senses)
    
    def examples_of_same_sense(self):
        '''
        Regroupe les contextes des examples dans un dictionnaire triés selon le 
        sens du mot à désambiguiser
        '''

        # clé : numéro du sens
        # valeur : liste de contextes avec ce sens en gold class
        sense2examples = {}
        # pour chaque example
        for example in self.examples:
            # si sa gold class n'a pas été déjà rencontrée
            if example[1] not in sense2examples:
                # ajoute une clé pour cette gold class
                sense2examples[example[1]] = []
            # ajoute le contexte au dictionnaire correspondant au sens utilisé
            sense2examples[example[1]].append(example[0])

        return sense2examples
    
    def learn_clusters(self):
        '''
        Algorithme de K-Means
        Retourne les coordonnées de chaque centroide ainsi que le cluster auquel 
        appartient chaque example
        '''

        # différence initialisée à Vrai
        diff = True
        
        # tant qu'il y a une différence entre l'ancienne liste et la nouvelle 
        # liste de centroides
        while diff:

            # CALCUL DES DISTANCES ENTRE CHAQUE EXAMPLE ET CHAQUE CENTROIDE

            # pour chaque couple (indice, coordonnées) dans les examples
            for i, tensor_example in enumerate(self.tensors_examples):
                # initialisation de la distance minimum à l'infini
                min_dist = float('inf')
                # pour chaque couple (indice, coordonnées) dans les centroides
                for j, tensor_centroid in enumerate(self.tensors_centroids):
                    # calcul de la distance entre cet example et ce centroide
                    d = 0
                    for k in range(len(tensor_example)):
                        d += (tensor_centroid[k].item() - tensor_example[k].item())**2
                    d = np.sqrt(d)
                    # si une distance plus faible est trouvée
                    if min_dist > d:
                        # la distance ainsi que le centroide sont stockés
                        min_dist = d
                        self.clusters[i] = j
            
            # CALCUL DES NOUVEAUX CENTROIDES

            # calcul des nouveaux centroides en utilisant le point au milieu de tous les
            # autres points du même cluster
            new_centroids = pd.DataFrame(self.tensors_examples).groupby(by = self.clusters).mean()
            # transforme ces nouveaux centroides en tensors
            tensors_new_centroids = []
            for i in range(len(new_centroids.index)):
                colums = []
                for j in range(len(new_centroids.columns)):
                    colums.append(int(new_centroids.iat[i,j]))
                tensors_new_centroids.append(torch.tensor(colums))

            # MISE A JOUR DES CENTROIDES

            count_diff = 0
            # pour chaque centroide
            for i in range(len(self.tensors_centroids)):
                # si l'ancien centroide et le nouveau ne sont pas les mêmes
                if not(torch.equal(self.tensors_centroids[i], tensors_new_centroids[i])):
                    count_diff += 1
                    # met à jour le centroide
                    self.tensors_centroids = tensors_new_centroids
            # s'il n'y a eu aucune différence entre les anciens et les nouveaux centroides, 
            # la boucle while se termine
            if count_diff == 0:
                diff = False
            
    


examples = {(torch.tensor([1,0,0]), 1), (torch.tensor([8,9,6]), 2), (torch.tensor([8,7,9]), 2), (torch.tensor([7,8,9]), 2), (torch.tensor([0,0,1]), 1)}
k_Means = K_Means(examples)
print(k_Means.k, k_Means.tensors_centroids, k_Means.clusters)
k_Means.learn_clusters()
print(k_Means.tensors_examples)
print(k_Means.k, k_Means.tensors_centroids, k_Means.clusters)

