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
from sklearn.decomposition import PCA

def load_data():

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
    
    return recipe_features,recipe_labels

def run_models(recipe_features,recipe_labels):

    multiNB = []
    gaussNB = []
    svm = []
    
    for i in range(0,10):
        #X_train, X_test, y_train, y_test = train_test_split(recipe_features, recipe_labels, test_size=0.2, random_state = 42)
        
        recipe_df = pd.DataFrame(np.c_[recipe_labels,recipe_features])
        
        train_proportion = np.random.rand(len(recipe_df)) < 0.8
        train = recipe_df[train_proportion]
        test = recipe_df[~train_proportion]
        
        X_train = train.as_matrix()[:,1:]
        y_train = train.as_matrix()[:,0]
        
        X_test = test.as_matrix()[:,1:]
        y_test = test.as_matrix()[:,0]
        
        
        print('Iter: '+str(i))
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
    return  gaussNB,multiNB,svm

def run_models_pca(recipe_features,recipe_labels,num_component):

    multiNB = []
    gaussNB = []
    svm = []
    
    for i in range(0,10):
        #X_train, X_test, y_train, y_test = train_test_split(recipe_features, recipe_labels, test_size=0.2, random_state = 42)
        
        recipe_df = pd.DataFrame(np.c_[recipe_labels,recipe_features])
        
        train_proportion = np.random.rand(len(recipe_df)) < 0.8
        train = recipe_df[train_proportion]
        test = recipe_df[~train_proportion]
        
#        X_train = train.as_matrix()[:,1:]
        y_train = train.as_matrix()[:,0]
#        
#        X_test = test.as_matrix()[:,1:]
        y_test = test.as_matrix()[:,0]
        
        pca = PCA(n_components=num_component)
        
        X_train_pca = pca.fit_transform(train.as_matrix()[:,1:])
        X_test_pca = pca.transform(test.as_matrix()[:,1:])
        
        
        print('Iter: '+str(i))
        ###################################################################
#        clf = MultinomialNB()
#        clf.fit(X_train_pca, y_train)
#        MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
#        multiNB.append(clf.score(X_test_pca,y_test))
#        #print('MultinomialNB Accuracy: ' , clf.score(X_test,y_test))
        ###################################################################
        clf = GaussianNB()
        clf.fit(X_train_pca, y_train)
        GaussianNB(priors=None)
        gaussNB.append(clf.score(X_test_pca,y_test))
        #print('GaussianlNB Accuracy: ' , clf.score(X_test,y_test))
        ###################################################################
        clf = SVC()
        clf.fit(X_train_pca, y_train) 
        SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
            decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
            max_iter=-1, probability=False, random_state=None, shrinking=True,
            tol=0.001, verbose=False)
        svm.append(clf.score(X_test_pca,y_test))
        
        #print('Support Vector Machine Accuracy: ' , clf.score(X_test,y_test))
    return  gaussNB,svm

