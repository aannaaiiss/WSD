phrases = [(["La rue , pourtant étroite , /aboutit sur la place Juan Carlos ."], 1), (["Le projet n'a pas /abouti ."], 2), 
            (["La marge n'est pas /justifiée ."],1), (["Votre absence n'est pas /justifiée ."], 2),
            (["Je suis /intervenue pour faire cesser le dispute ."], 1), (["Le professeur est /intervenu au sujet de la distanciation social ."], 2),
            (["J'y suis /arrivé !"], 1), (["Je suis /arrivé !"], 2),
            (["Le policier a /interpelé le jeune manifestant ."], 1), (["Cette anomalie m'a /interpelée ."], 2)]

context_size = 10

def left_context(context): 
    '''
    context: list of words
    returns: dictionary of previous words
    '''
    left = {}
    context.reverse()
    for i in range(0,context_size,1):
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
    for i in range(context_size): 
        if i < len(context):
             right.update({f'next_word_{i+1}': context[i]})
        else: 
            right.update({f'next_word_{i+1}': '<f>'})
    return right

toy = []
for example in phrases:
        sentence, gold = example[0], example[1]
    
        # dictionary to store the instance and its context
        print(sentence)
        sent = {}
        sentence = sentence[0].lower().split()
        print(sentence)
        instance = [word for word in sentence if word.startswith("/") ]
        index_instance = sentence.index(instance[0])
        sent.update({"instance": instance[0].strip("/")})
        sent.update(right_context(sentence[index_instance+1:]))
        sent.update(left_context(sentence[:index_instance]))
        toy.append((sent,gold))
        
print(toy)



