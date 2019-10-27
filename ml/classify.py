#!/bin/python

import numpy as np

def train_classifier(X, y, *args, **kargs):
	"""Train a classifier using the given training data.

	Uses gridsearch to find the best hyper-parameter values.
	"""
	rtn_scores = False
	if 'rtn_cv_results' in kargs and kargs['rtn_cv_results'] == True:
		rtn_scores = True

	from sklearn.linear_model import LogisticRegression
	from sklearn.model_selection import GridSearchCV
	parameters = {
		'penalty': ['l2'], 
		#'C': [1e-3, 1e-2, 1e-1, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 1, 1.5, 1e1, 1e2, 1e3]
		'C': [1e-3, 1e-2, 1e-1, 0.5, 1, 1.5, 1e1, 5e1, 1e2, 5e2, 1e3, 1e4, 1e5, 1e6]
		#'C': [10.0]
	}

	#cls = LogisticRegression(random_state=0, solver='lbfgs', max_iter=10000)
	cls = LogisticRegression(random_state=0, max_iter=30000)
	#cls.fit(X,y) # Uncommnet these two for original train classifier
	#return cls

	clf = GridSearchCV(cls, parameters, cv=5, n_jobs=-1, return_train_score=rtn_scores)
	clf.fit(X, y)
	print("Best params:", clf.best_params_)
	if rtn_scores:
		return clf, clf.cv_results_, parameters['C']
	return clf


def evaluate(X, yt, cls, name='data'):
	"""Evaluated a classifier on the given labeled data using accuracy."""
	from sklearn import metrics
	yp = cls.predict(X)
	acc = metrics.accuracy_score(yt, yp)
	print("  Accuracy on %s  is: %s" % (name, acc))
