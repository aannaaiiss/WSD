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



