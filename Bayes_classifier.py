# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 20:35:40 2017

@author: Trung Duy
"""

import csv
import time
import random
import math
from collections import Counter 
import os
import struct
import numpy as np
import pandas as pd  
from numpy.linalg import pinv,slogdet,inv

#import itertools
#import matplotlib.pyplot as plt
#from sklearn.metrics import confusion_matrix
#import plotly.plotly as py
#import plotly.graph_objs as go
#from plotly.graph_objs import *
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#init_notebook_mode() 


def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if (vector[0] not in separated):
            separated[vector[0]] = []
        separated[vector[0]].append(vector)
    return separated
 
def summarize(dataset):
    summaries = [(np.mean(attribute), np.std(attribute,ddof= 1)) for attribute in zip(*dataset)]
    del summaries[0]
    return summaries
 
def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classValue, instances in separated.items():
        summaries[classValue] = summarize(instances)
    return summaries 

def getMean(summaries):
    Mean = {}
    for classValue in range(0,2):
        Mean[classValue] = [item[0] for item in summaries[classValue]] 
    return Mean


def getCovbyClass(separated,data_name = 'mnist'):
    cov_class = {}
    for classValue, instances in separated.items():
        mtrx = pd.DataFrame(separated.get(classValue)).as_matrix()
        cov_mtrx = np.cov(mtrx[:,1:].T)
        if data_name == 'mnist':
            np.fill_diagonal(cov_mtrx, cov_mtrx.diagonal(0) + 1e4) #use this for mnist dataset
        #np.fill_diagonal(cov_mtrx, cov_mtrx.diagonal(0))
        cov_class[classValue] = pinv(cov_mtrx)
    return cov_class

def getDetbyClass(cov_class):
    det ={}
    for classValue, instances in cov_class.items():
        (sign, logdet) = slogdet(cov_class[classValue])
        det[classValue] = logdet
    return det

def getprior(label):
    class_counts = Counter(label)
    class_priors = {}
    for classValue in class_counts:
        class_priors[classValue] = class_counts[classValue]/sum(class_counts.values())
    return class_priors

def Bayes_Classifier_fit(x,data_name = 'mnist'):
    print('===== START TRAINING =====')
    start = time.time()
    separated = separateByClass(x)
    summaries = summarizeByClass(x)
    prior = getprior(np.array(x[:,0]))
    Mean = getMean(summaries)
    cov_class = getCovbyClass(separated,data_name)
    logdet = getDetbyClass(cov_class)
    print('Training time: '+ str(time.time()-start) + 's')
    print('===== FINISH TRAINING =====')
    return summaries,cov_class,Mean,logdet, prior

    
#def calculateProbability(x, mean, stdev):
#    #if stdev < 1e-3:
#    #    if math.fabs(x-mean) < 1e-2:
#    #        return 1.0
#    #    else:
#    #        return 0
#    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
#    return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
# 
#def calculateClassProbabilities(summaries, inputVector):
#    probabilities = {}
#    for classValue, classSummaries in summaries.items():
#        probabilities[classValue] = 1
#        likelihood = []
#        for i in range(len(classSummaries)):
#            mean, stdev = classSummaries[i]
#            #if stdev !=0.0:
#            x = inputVector[i]
#            likelihood.append(calculateProbability(x, mean, stdev)*100)
#        probabilities[classValue] *= np.log(np.prod(likelihood))
#    return probabilities

def calculateClassProbabilities2(summaries, cov_class, Mean, logdet, prior, inputVector):
    probabilities = {}
    for classValue in range(0,2):
        err = np.array(inputVector-Mean[classValue])
        term1 = -0.5* np.dot(np.dot(err.T,cov_class[classValue]),err)
        term2 = (-0.5*logdet[classValue]) - (cov_class[classValue].shape[0]*0.5*np.log(2*math.pi))
        probabilities[classValue] = term1 + term2 + np.log(prior[classValue])
    return probabilities

def predict2(summaries, cov_class, Mean, logdet, prior, inputVector):
    probabilities = calculateClassProbabilities2(summaries, cov_class, Mean, logdet,prior, inputVector)
    return max(probabilities, key=probabilities.get)


#def predict(summaries, inputVector):
#    probabilities = calculateClassProbabilities(summaries, inputVector)
#    return max(probabilities, key=probabilities.get)
 
def getPredictions(summaries, cov_class, Mean, logdet, prior, testSet):
    predictions = []
    for i in range(len(testSet)):
        #result = predict(summaries, testSet[i])
        result = predict2(summaries, cov_class, Mean, logdet, prior,testSet[i])
        predictions.append(result)
        if i%1000 == 0:
            print('Done sample test: ',i)
    return predictions
 
def score(y_test, y_predict):
    return np.sum(y_predict == y_test)/float(len(y_test))*100.0


