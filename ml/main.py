#!/bin/python

'''
Train a vanilla logistic regression.
'''
import classify
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import sentiment as sent

USE_BOG = True

if __name__ == "__main__":
    print("Reading data")
    datafile = "data/bayzick_clean.csv"
    sentiment = sent.read_files(datafile, use_bow=USE_BOG)

    print("\nTraining supervised classifier")
    cls, cv_results, c_list = classify.train_classifier(sentiment.trainX, sentiment.trainy, rtn_cv_results=True)

    import pickle
    pickle.dump(cls, open("lin_reg_unsup.pkl", "wb"))
    pickle.dump(sentiment, open("sen.pkl", "wb"))

    print("\nEvaluating Supervised")
    classify.evaluate(sentiment.trainX, sentiment.trainy, cls, 'train')
    classify.evaluate(sentiment.devX, sentiment.devy, cls, 'dev')