
import random
X_train = X_train

def predict_on_batch(batch_size):
    for i in range(0, len(X_train), batch_size):
        if(i+batch_size > len(X_train)):
            batch_X_train = X_train[i:]
        else:
            batch_X_train = X_train[i:i+batch_size]
        predict(batch_X_train)


    

