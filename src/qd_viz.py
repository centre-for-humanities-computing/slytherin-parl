import os
import argparse
import json
import numpy as np
import scipy as sp
import scipy.stats as stats
import saffine.detrending_method as dm
from signal_viz import normalize, adaptive_filter
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({"text.usetex": False,
                    "font.family": "serif",
                    "mathtext.fontset": "cm",
                    "axes.unicode_minus": False
                    })

def main():
    # state detector
    X = np.round(np.loadtxt('dat/subject_pX.txt', delimiter=' '))

    fig, ax = plt.subplots(figsize=(14, 6),dpi=300)
    for i in range(X.shape[1]):
        bool_idxs = X.T[i,:]
        x = np.zeros(bool_idxs.shape)
        y = x.copy()
        for (ii, val) in enumerate(bool_idxs):
            if val == 1.:
                x[ii] = ii
                y[ii] = i + 1 
        ax.scatter(x, y, color='k', marker='.')
    
    ax.set_yticks(range(0, X.shape[1]+2))
    #ax.set_yticklabels()
    
    plt.savefig('fig/subject_states.png')
        
    
    
    with open('mdl/subject_signal.json', "r") as fobj:
        lignes = fobj.readlines()
    
    time = list()
    novelty = list()
    resonance = list()
    for (i, ligne) in enumerate(lignes):
        dobj = json.loads(ligne)
        time.append(dobj["date"])
        novelty.append(dobj["novelty"])
        resonance.append(dobj["resonance"])
    
    
    # remove window start-end
    w = 5
    time = time[w:-w]
    novelty = novelty[w:-w]
    resonance = resonance[w:-w]
    
    ax.plot(time, normalize(novelty, lower=1, upper=20), color='r', alpha=.5)

    plt.savefig('fig/subject_states.png')
    

if __name__=='__main__':
    main()
