# Team Slytherin :snake: does DataTinget #

## Introduction ##

[DataTinget](https://datasprint2021.kb.dk/en/) is a hackathon on democracy and political negotiations in the Danish Parliament, _Folketinget_, participants are compete on modeling Folketingets proceedings from 1953 to 2021. 

Inspirational speaker [Niels Wium Olesen](https://pure.au.dk/portal/da/persons/niels-wium-olesen(91fd39f8-08b8-4b45-bfd8-3576c2e0c22e).html) prompted us to a) develop a technique to detect significant societal events as reflected in parliamentary data; and b) train a noise-tolerant model that can label large unstructured data (e.g., _data-set 1_). 

Team Syltherin identifies _two_ related issues that utilize (ground truth) labels for subjects, `subject 1`, in _data-set 2_:

* Model Validation: Validation of current information dynamics models on ground truth subject labels
* Subject Classification: Classification of subject for unlabelled data (ex. _data-set 1_) 

## Model Validation ##

Recently there has been a surge in information theoretic models that use unstructured data to detect and characterize change as a function of events in stream of cultural data (e.g., news, social media). The models however have only been validated indirectly through their capacity to predict pre-defined events. In this paper, we validate the signals used to detect events in full text data by comparing them to signals based on ground truth annotations of subjects in parliamentary data.

### Methods ###

#### Data and Normalization ####

From _data-set 2_ 

#### Novelty and Resonance ####

$\mathcal{N}$: novelty as article $s^{(j)}$'s reliable difference from past articles $s^{(j-1)}, s^{(j-2)} , \dots ,s^{(j-w)}$ in window $w$:

$$\mathcal{N}_w (j) = \frac{1}{w} \sum_{d=1}^{w}  JSD (s^{(j)} \mid s^{(j - d)})$$

$\mathcal{R}$: resonance as the degree to which future articles $s^{(j+1)}, s^{(j+2)}, \dots , s^{(j+w)}$ conforms to article $s^{(j)}$'s novelty:

$$\mathcal{R}_w (j) = \mathcal{N}_w (j) - \mathcal{T}_w (j)$$

where $\mathcal{T}$ is the transience of $s^{(j)}$:

$$\mathcal{T}_w (j) = \frac{1}{w} \sum_{d=1}^{w}  JSD (s^{(j)} \mid s^{(j + d)})$$

we propose a symmetrized and smooth version by using the Jensen–Shannon divergence ($JSD$):


$$JSD (s^{(j)} \mid s^{(k)}) =  \frac{1}{2} D (s^{(j)} \mid M) + \frac{1}{2} D (s^{(k)} \mid M)$$

with $M = \frac{1}{2} (s^{(j)} + s^{(k)})$ and $D$ is the Kullback-Leibler divergence:

$$D (s^{(j)} \mid s^{(k)}) = \sum_{i = 1}^{K} s_i^{(j)} \times \log_2 \frac{s_i^{(j)}}{s_i^{(k)}}$$

In order to compare information states between model and ground truth, we fit resonance on novelty to estimate the $\mathcal{N}\times\mathcal{R}$ slope $\beta_1$:

$$\mathcal{R}_i = \beta_0 + \beta_1 \mathcal{N}_i + \epsilon_i, ~~ i = 1, \dots, n.$$

### Results ###

<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/subject_adaptline.png" alt="Trulli" style="width:100%">
<figcaption align = "center"><b>Fig.1 Novelty and Resonance for GT Subjects</b></figcaption>
</figure>

<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/subject_regline.png" alt="Trulli" style="width:50%">
<figcaption align = "center"><b>Fig.2 Resonance on Novelty for GT Subjects</b></figcaption>
</figure>

<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/subject_states.png" alt="Trulli" style="width:100%">
<figcaption align = "center"><b>Fig.3 Novelty singal from subjects and subject states on time (index day), for GT Subjects</b></figcaption>
</figure>




<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/dtw_speech_vs_subject.png" alt="Trulli" style="width:100%">
<figcaption align = "center"><b>Fig.4 subject x model</b></figcaption>
</figure>


<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/dtw_speech_vs_random.png" alt="Trulli" style="width:100%">
<figcaption align = "center"><b>Fig.5 random x model </b></figcaption>
</figure>




## Subject Classification ##

### Methods ###



#### Data and Normalization ####

From _data-set 2_ 


#### Naive Bayes Classifier ####

The probability of a document $d$ being in class $c$, $P(c \mid d)$ is computed as:

$$P(c \mid d) \propto P(c) \prod_{i = 1}^{m}P(t_i \mid c) $$

and the class of a document $d$ is then computed as:

$$c_{MAP} = arg~max_{c \in \{c_1, c_2 \}} P(c \mid d)$$


### Results ###


#### Further Classification Comparison ####

<figure>
<img src="https://raw.githubusercontent.com/centre-for-humanities-computing/slytherin-parl/main/fig/FINAL_comparison.png" alt="Trulli" style="width:100%">
<figcaption align = "center"><b>Fig.5 random x model </b></figcaption>
</figure>



## Discussion ##

## Acknowledgements ##

UCloud, KB, Aarhus University