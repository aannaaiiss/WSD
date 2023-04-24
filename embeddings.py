# %%
#copie du code du toy - le code prend un peu moins de 5min
phrases = [(["Le rue , pourtant étroit , /aboutir sur le place Juan Carlos ."], 1), (["Le projet ne avoir pas /aboutir ."], 2), 
            (["Le marge ne être pas /justifier ."],1), (["Votre absence ne être pas /justifier ."], 2),
            (["Je être /intervenir pour faire cesser le dispute ."], 1), (["Le professeur être /intervenir au sujet de le distanciation social ."], 2),
            (["Je y être /arriver !"], 1), (["Je être /arriver !"], 2),
            (["Le policier avoir /interpeler le jeune manifestant ."], 1), (["Ce anomalie me avoir /interpeler ."], 2)]

window_size = 10

def left_context(context): 
    '''
    context: list of words
    returns: dictionary of previous words
    '''
    left = {}
    context.reverse()
    for i in range(0,window_size,1):
        if i < len(context):
            left.update({f'previous_word_{i+1}': context[i]})
        else: 
            left.update({f'previous_word_{i+1}': '<d>'})

    return left

def right_context(context): 
    '''
    context: list of words
    returns: dictionary of following words
    '''
    right = {}
    for i in range(window_size): 
        if i < len(context):
             right.update({f'next_word_{i+1}': context[i]})
        else: 
            right.update({f'next_word_{i+1}': '<f>'})
    return right

toy = []
for example in phrases:
        sentence, gold = example[0], example[1]
    
        # dictionary to store the instance and its context
        sent = {}
        sentence = sentence[0].lower().split()
        instance = [word for word in sentence if word.startswith("/") ]
        index_instance = sentence.index(instance[0])
        sent.update({"instance": instance[0].strip("/")})
        sent.update(right_context(sentence[index_instance+1:]))
        sent.update(left_context(sentence[:index_instance]))
        toy.append((sent,gold))
        
print("examples : ",toy,"\n")

# %%
#Code pour créer le i2w d'une liste d'examples

examples = toy #à définir

#on crée un vocabulaire qui nous permettra de récupérer les lignes qui nous intéressent dans le fichier d'embeddings
i2w=[]

for (vector,gold) in examples :
    for word in vector.values() :
        if word not in i2w:
            i2w.append(word)

print("vocabulaire : ",i2w,"\n")

# %%
#Code pour créer le fichier d'embeddings

fasstex_path = "../fasstex" #à définir
f = open(fasstex_path, "r", encoding="UTF-8")
word2vec = {}

f.readline() #permet de ne pas prendre en compte la première ligne du fichier qui résumé ce que contient le fichier
lines = f.readlines()

#On crée un fichier dans lequel on copie seulement les embeddings correspondantes aux mots du vocabulaire
file_embeddings = "toy_embeddings.txt" #à définir
with open(file_embeddings,"w",encoding="UTF-8") as toy_embeddings_file : 
        toy_embeddings_file.writelines([line for line in lines if line.split(" ")[0] in i2w])

# %%
#Construction du dictionnaire qui va permettre de faire le lookup

path = "./"+file_embeddings #à définir

f = open(path, "r", encoding="UTF-8")

#On récupère dans le fichier crée les embeddings pour crée un dictionnaire
word2vec = {}
for line in f.readlines():
    splitted_line = line.split(" ")
    word = splitted_line[0]
    vector = list(map(float,splitted_line[1:]))
    word2vec[word] = vector

print("lemme(s) pour lesquels il n'existe pas d'embedding : ",([word for word in i2w if word not in word2vec],"\n"))

# %%
#look up

#A partir du dictionnaire, on crée un nouveau set d'examples
examples_embeddings = []

for example in toy:
    
    vector_embeddings = {}
    vector = example[0]
    gold = example[1]
    
    #Le nouveau vecteur est similaire à l'ancien mais on a remplacé dans celui-ci chaque mot par son embedding correspondant
    #vector_embeddings = { word_ind : word2vec[vector[word_ind]] for word_ind in vector if word_ind in word2vec}
    for word_ind in vector :

        if vector[word_ind] in word2vec :
            vector_embeddings[word_ind] = word2vec[vector[word_ind]]
        
        #solution pour qu'il n'y ait pas d'erreur si certains lemmes n'ont pas d'embeddings
        #mais biaise les calculs
        else :
            vector_embeddings[word_ind] = [0.0 for i in range(300)]
            
    examples_embeddings.append((vector_embeddings,gold))

print("example n°1 with embeddings : ",examples_embeddings[0])


