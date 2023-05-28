import numpy as np
import torch
import pandas as pd

class K_Means():
    # classifieur K-means pour un lemme particulier

    def __init__(self, examples):
        # examples est un ensemble d'examples pour un meme lemme

        import random

        examples = list(examples)
        self.tensors_examples = [example[0] for example in examples]
        self.k = self.nb_senses(examples)
        # initialisation de centroids : pour chaque sens, un example est pris au hasard
        self.tensors_centroids = [random.choice(example) for example in self.examples_of_same_sense(examples).values()]
        # initialisation de clusters : tous les examples sont associés au cluster 0
        self.clusters = np.zeros(len(examples))

    def nb_senses(self, examples):
        known_senses = []
        for example in examples:
            if example[1] not in known_senses:
                known_senses.append(example[1])
        return len(known_senses)
    
    def examples_of_same_sense(self, examples):

        sense2examples = {}
        for example in examples:
            if example[1] not in sense2examples:
                sense2examples[example[1]] = []
            sense2examples[example[1]].append(example[0])

        return sense2examples
    
    def vecteur_example(self, example):

        vecteur = np.zeros(300)

        for word in example[0].values():
            vecteur += self.look_up_operation(word)
        
        return vecteur
    
    def learn_clusters(self):

        # différence initialisée à Vrai
        diff = True
        
        # tant qu'il y a une différence entre l'ancienne liste et la nouvelle liste de centroides
        while diff:
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
            
            # calcul des nouveaux centroides en utilisant le point au milieu de tous les
            # autres points du même cluster
            new_centroids = pd.DataFrame(self.tensors_examples).groupby(by = self.clusters).mean()
            
            tensors_new_centroids = []
            for i in range(len(new_centroids.index)):
                colums = []
                for j in range(len(new_centroids.columns)):
                    colums.append(int(new_centroids.iat[i,j]))
                tensors_new_centroids.append(torch.tensor(colums))

            for i in range(len(self.tensors_centroids)):
                if torch.equal(self.tensors_centroids[i], tensors_new_centroids[i]):
                    diff = False
                    break
            else:
                self.tensors_centroids = tensors_new_centroids
            
    


examples = {(torch.tensor([1,0,0]), 1), (torch.tensor([8,9,6]), 2), (torch.tensor([8,7,9]), 2), (torch.tensor([7,8,9]), 2), (torch.tensor([0,0,1]), 1)}
k_Means = K_Means(examples)
print(k_Means.k, k_Means.tensors_centroids, k_Means.clusters)
k_Means.learn_clusters()
print(k_Means.tensors_examples)
print(k_Means.k, k_Means.tensors_centroids, k_Means.clusters)

