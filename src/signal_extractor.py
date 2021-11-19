import os
import numpy as np
import newlinejson
from infodynamics import InfoDynamics, kld

def main():
    print("[INFO] reading model...")

    pX = np.loadtxt('dat/subject_pX.txt', delimiter=' ')
    t = list(range(pX.shape[0]))#TODO: update to timestamp
    
    print("[INFO] extracting signal...")
    idmdl = InfoDynamics(data = pX, time = t, window = 5)
    idmdl.novelty(meas = kld)
    idmdl.transience(meas = kld)
    idmdl.resonance(meas = kld)

    fname = 'mdl/subject_signal.json'
    if os.path.isfile(fname):
        pass
    else:
        os.mknod(fname)
    
    lignes = list()
    for i, date in enumerate(t):
        d = dict()
        d["date"] = date
        d["novelty"] = idmdl.nsignal[i] 
        d["transience"] = idmdl.tsignal[i]
        d["resonance"] = idmdl.rsignal[i]
        d["nsigma"] = idmdl.nsigma[i]
        d["tsigma"] = idmdl.tsigma[i]
        d["rsigma"] = idmdl.rsigma[i]
        lignes.append(d)
    
    with open(fname, "r+") as f:
        newlinejson.dump(lignes, f)

if __name__=='__main__':
    main()