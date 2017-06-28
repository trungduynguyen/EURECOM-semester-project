# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 10:19:13 2017

@author: Trung Duy
"""

import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC



data_df = []
for i in range(0,11):
    temp = pd.DataFrame.from_csv('data/data'+str(i)+'.csv')
    data_df.append(temp)
    
recipe_df = pd.concat(data_df)  
label = [ 1 if x>= np.mean(recipe_df['rate']) else 0 for x in recipe_df['rate']]
recipe_df['label'] = label
         
         
shuffle_df = shuffle(recipe_df)


recipe_features = np.delete(shuffle_df.as_matrix(),[3926,3927],1)
recipe_labels = shuffle_df.as_matrix()[:,-1]


multiNB = gaussNB = svm = []

for i in range(0,20):
    X_train, X_test, y_train, y_test = train_test_split(recipe_features, recipe_labels, test_size=0.3, random_state=42)
    ###################################################################
    clf = MultinomialNB()
    clf.fit(X_train, y_train)
    MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    multiNB.append(clf.score(X_test,y_test))
    #print('MultinomialNB Accuracy: ' , clf.score(X_test,y_test))
    ###################################################################
    clf = GaussianNB()
    clf.fit(X_train, y_train)
    GaussianNB(priors=None)
    gaussNB.append(clf.score(X_test,y_test))
    #print('GaussianlNB Accuracy: ' , clf.score(X_test,y_test))
    ###################################################################
    clf = SVC()
    clf.fit(X_train, y_train) 
    SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
        decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
        max_iter=-1, probability=False, random_state=None, shrinking=True,
        tol=0.001, verbose=False)
    svm.append(clf.score(X_test,y_test))
    #print('Support Vector Machine Accuracy: ' , clf.score(X_test,y_test))

