import os
import argparse
import json
import numpy as np
import scipy as sp
import scipy.stats as stats
import saffine.detrending_method as dm
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({"text.usetex": False,
                    "font.family": "serif",
                    "mathtext.fontset": "cm",
                    "axes.unicode_minus": False
                    })

def normalize(x, lower=-1, upper=1):
    """ transform x to x_ab in range [a, b]
    """
    x_norm = (upper - lower)*((x - np.min(x)) / (np.max(x) - np.min(x))) + lower
    return x_norm


def adaptive_filter(y, span=56):
    #if len(y) % 2:
    #   y=y[:-1]

    w = int(4 * np.floor(len(y)/span) + 1)
    y_dt = np.mat([float(j) for j in y])
    _, y_smooth = dm.detrending_method(y_dt, w, 1)
    
    return y_smooth.T

def plot_ci_manual(t, s_err, n, x, x2, y2, ax=None):
    """Return an axes of confidence bands using a simple approach.

    """
    if ax is None:
        ax = plt.gca()

    ci = t * s_err * np.sqrt(1/n + (x2 - np.mean(x))**2 / np.sum((x - np.mean(x))**2))
    ax.fill_between(x2, y2 + ci, y2 - ci, color="#b9cfe7", edgecolor="")

    return ax


def plot_ci_bootstrap(xs, ys, resid, nboot=500, ax=None):
    """Return an axes of confidence bands using a bootstrap approach.
    Returns
    -------
    ax : axes
        - Cluster of lines
        - Upper and Lower bounds (high and low) (optional)  Note: sensitive to outliers
    """ 
    if ax is None:
        ax = plt.gca()

    bootindex = sp.random.randint

    for _ in range(nboot):
        resamp_resid = resid[bootindex(0, len(resid) - 1, len(resid))]
        # Make coeffs of for polys
        pc = np.polyfit(xs, ys + resamp_resid, 1)                   
        # Plot bootstrap cluster
        ax.plot(xs, np.polyval(pc, xs), "r-", linewidth=2, alpha=3.0 / float(nboot))

    return ax

def adaptiveline(x1, x2, fname="adaptline.png"):
    _, ax = plt.subplots(2,1,figsize=(14,6),dpi=300)
    c = ["g", "r", "b"]
    ax[0].plot(normalize(x1, lower=0),c="gray")
    for i, span in enumerate([128]):
        #n_smooth = normalize(adaptive_filter(x1, span=span), lower=0)
        n_smooth = adaptive_filter(normalize(x1, lower=0), span=span)
        ax[0].plot(n_smooth,c=c[i])
    ax[0].set_ylabel("$\\mathcal{N}ovelty$", fontsize=14)
    
    ax[1].plot(normalize(x2, lower=-1),c="gray")
    for i, span in enumerate([128]):
        #r_smooth = normalize(adaptive_filter(x2, span=span), lower=-1)
        r_smooth = adaptive_filter(normalize(x2, lower=-1), span=span)
        ax[1].plot(r_smooth,c=c[i])
    ax[1].set_ylabel("$\\mathcal{R}esonance$", fontsize=14)
    plt.tight_layout()
    plt.savefig(fname)
    plt.close()


def regline(x, y, bootstap=True, fname="regline.png"):
    p, _ = np.polyfit(x, y, 1, cov=True)
    y_model = np.polyval(p, x)
    # statistics
    n = y.size
    m = p.size
    dof = n - m
    t = stats.t.ppf(0.975, n - m)
    # estimates of error
    resid = y - y_model                           
    chi2 = np.sum((resid / y_model)**2) 
    chi2_red = chi2 / dof
    s_err = np.sqrt(np.sum(resid**2) / dof)    
    # plot
    fig, ax = plt.subplots(figsize=(8, 7.5),dpi=300)
    ax.plot(x, y, ".", color="#b9cfe7", markersize=8,markeredgewidth=1, markeredgecolor="r", markerfacecolor="None")
    ax.plot(x, y_model, "-", color="0.1", linewidth=1.5, alpha=0.5, label="$\\beta_1 = {}$".format(round(p[0], 2)))
    x2 = np.linspace(np.min(x), np.max(x), 100)
    y2 = np.polyval(p, x2)
    # confidence interval option
    if bootstap:
        plot_ci_bootstrap(x, y, resid, ax=ax)
    else:
        plot_ci_manual(t, s_err, n, x, x2, y2, ax=ax)
    # prediction interval
    pi = t * s_err * np.sqrt(1 + 1/n + (x2 - np.mean(x))**2 / np.sum((x - np.mean(x))**2))   
    ax.fill_between(x2, y2 + pi, y2 - pi, color="None", linestyle="--")
    ax.plot(x2, y2 - pi, "--", color="0.5", label="95% Prediction Limits")
    ax.plot(x2, y2 + pi, "--", color="0.5")
    # borders
    ax.spines["top"].set_color("0.5")
    ax.spines["bottom"].set_color("0.5")
    ax.spines["left"].set_color("0.5")
    ax.spines["right"].set_color("0.5")
    ax.get_xaxis().set_tick_params(direction="out")
    ax.get_yaxis().set_tick_params(direction="out")
    ax.xaxis.tick_bottom()
    ax.yaxis.tick_left()
    # labels
    plt.title("Classification of Uncertainty State", fontsize="14", fontweight="bold")
    plt.xlabel("$\\mathcal{N}ovelty_z$", fontsize="14", fontweight="bold")
    plt.ylabel("$\\mathcal{R}esonance_z$", fontsize="14", fontweight="bold")
    plt.xlim(np.min(x) - .25, np.max(x) + .25)
    # custom legend
    handles, labels = ax.get_legend_handles_labels()
    display = (0, 1)
    anyArtist = plt.Line2D((0, 1), (0, 0), color="#ea5752")
    legend = plt.legend(
        [handle for i, handle in enumerate(handles) if i in display] + [anyArtist],
        [label for i, label in enumerate(labels) if i in display] + ["95% Confidence Limits"],
        loc=9, bbox_to_anchor=(0, -0.21, 1., 0.102), ncol=3, mode="expand"
    )  
    frame = legend.get_frame().set_edgecolor("0.5")
    mpl.rcParams['axes.linewidth'] = 1
    # save figure
    plt.tight_layout()
    plt.savefig(fname, bbox_extra_artists=(legend,), bbox_inches="tight")

def main():
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
    
    # trend detection
    figname0 = 'fig/subject_adaptline.png'
    adaptiveline(novelty, resonance, fname=figname0)

    # remove window start-end
    w = 5
    time = time[w:-w]
    novelty = novelty[w:-w]
    resonance = resonance[w:-w]
    # classification based on z-scores
    xz = stats.zscore(novelty)
    yz = stats.zscore(resonance)
    figname1 = 'fig/subject_regline.png'
    regline(xz, yz, fname=figname1)
    

if __name__=='__main__':
    main()