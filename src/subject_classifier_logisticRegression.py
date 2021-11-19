import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import html
import eli5
from eli5.lime import TextExplainer
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn import metrics


def main():
    filepath = '../dat/whole_set.csv'
    df = pd.read_csv(filepath)
    ## filter foreman
    #print(df.columns)

    content = df['Text'].values

    # TODO: pruning and stopwords on the input 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(content)
    
    y = df['Subject 1'].values
    target_names = df['Subject 1'].drop_duplicates()
    #print("target name: ", target_names)

    subject_counts = df['Subject 1'].value_counts()
    #print(subject_counts)
    
    # split in train and validation set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3) # 70% training and 30% test

    ### For Logistic Regression
    '''
    # create model 
    clf = LogisticRegression(solver='lbfgs', max_iter=100)
    # train model
    clf.fit(X_train, y_train)
    # predict
    pred = clf.predict(X_test)

    #  metric report
    metricRepport = metrics.classification_report(y_test, pred)
    
    # eli5 explanations
    explanation = eli5.show_weights(clf, vec = vectorizer, top=20)
    save_HTMLfigure(explanation)
    '''
    ### For MultinomialNB ###
    mncl = MultinomialNB()
    mncl.fit(X_train, y_train)

    # predict 
    y_pred = mncl.predict(X_test)

    # compute accuracy
    accuracy = mncl.score(X_test, y_test)
    print("Test accuracy", accuracy)

    # Metric classification report
    class_report = classification_report(y_test, y_pred, target_names=target_names)
    print(class_report)

def save_HTMLfigure(display_figure):
    with open('../fig/eli5.htm','wb') as f:   # Use some reasonable temp name
        f.write(display_figure.data.encode("UTF-8"))


if __name__=='__main__':
    main()