phrases = [["La rue , pourtant étroite , /aboutit sur la place Juan Carlos ."], ["Le projet n'a pas /abouti ."], ["Les marges ne sont pas /justifiées ."],
           ["Votre absence n'est pas /justifiée ."], ["Je suis /intervenue pour faire cesser la dispute ."], 
           ["Les professeurs sont /intervenus au sujet de la distanciation sociale ."], ["J'y suis /arrivée !"], ["Je suis /arrivée !"], 
           ["Les policiers ont /interpellé la jeune manifestante ."], ["Cette anomalie m' a /interpellé ."]]




def left_context(context): 
    left = {}
    index = 0
    for el in reversed(context): 
        index += 1
        left.update({f'previous_word_{index}': el})
    return left

def right_context(context): 
    right = {}
    for i in range(len(context)): 
        right.update({f'next_word_{i+1}': context[i]})
    return right

toy = []
for example in phrases:
    for sentence in example:
        sent = {}
        sentence = sentence.lower().split()
        instance = [word for word in sentence if word.startswith("/") ]
        index_instance = sentence.index(instance[0])
        sent.update({"instance": instance[0].strip("/")})
        sent.update(right_context(sentence[index_instance+1:]))
        sent.update(left_context(sentence[:index_instance]))
        toy.append(sent)
        
print(toy)



