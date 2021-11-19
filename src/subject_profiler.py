import operator
import re
import pandas as pd
import numpy as np
import copy

def word_count(tokens, sort = False):
    """ count words
    """
    counter = {}
    for word in tokens:
        counter.setdefault(word, 0)
        counter[word] = counter[word] + 1
    
    if sort:
        counter = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))

    return counter

def normalizer(ls):
    ls = [re.sub(' +', '-', elem.lower()) for elem in ls]
    
    return ls

def subject_counter(tokens, types, sort = True):
    #counter = zip(types, [0 for val in types]])
    
    counter = dict()
    for t in types: counter[t] = 0
    for t in tokens: counter[t] += 1
    
    return counter

def main():
    print('[INFO] reading data...')
    data = pd.read_csv('dat/subject_time.csv')
    timeset = sorted(list(set(data['time'].values)))    
    inventory = normalizer(sorted(list(set(data['subject'].values))))

    print('[INFO] extracting subject arrays...')
    (m, n) = len(timeset), len(inventory)
    X = np.zeros((m, n))
    pX = copy.deepcopy(X)
    add_noise = True
    verbose = 100
    for (i, time) in enumerate(timeset):
        if i % verbose == 0:
            print(f'[INFO] file {i} of {m}')
        idxs = data['time'] == time
        subjects = normalizer(data['subject'].loc[idxs].values)
        xarr = subject_counter(subjects, inventory)
        xarr = np.array(list(xarr.values()))
        if add_noise:
            wnoise = np.random.normal(0, .01, xarr.shape)
            xarr = np.abs(xarr + wnoise)
        X[i,:] = xarr
        pX[i,:] = np.divide(xarr, np.ones_like(xarr)*sum(idxs))

    np.savetxt('dat/subject_X.txt', X, fmt='%.18e', delimiter=' ')
    np.savetxt('dat/subject_pX.txt', pX, fmt='%.18e', delimiter=' ')

if __name__=='__main__':
    main()