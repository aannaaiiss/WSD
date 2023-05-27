import numpy as np


def make_batches(examples, batch_size, shuffle_data=True):
    """ input examples : python list of (x,y) pairs,
                    with
                    - the x vector : a sparse vector encoded according to the following bolean components: 
                        - instance (the instance word)
                        - next_word_1, next_word_2, ..., next_word_context_size (for the context words after the instance)
                        - previous_word_1, previous_word_2, ..., previous_word_context_size (for the context words before the instance)) 
                    - y = the gold definition id for the instance
    """
    if shuffle_data:
        np.random.shuffle(examples)
        
    nb_examples = len(examples)
    
    i = 0
    while i < nb_examples:
        # we take batch_size examples
        batch = examples[i:i+batch_size]
        i += batch_size
        
        # separating input sentences and gold labels
        (batchX, batchY) = list(zip(*examples))

        yield(batchX, batchY)

