#!/usr/bin/python

from sklearn import tree
# This is for comparing apples with oranges.
# the first column describes the weigth of the fruits
# the second describes the surface, 1 = smooth, 0 = bumpy
features = [[140, 1], [130, 1], [150, 0], [170, 0]]
labels = [0, 0, 1, 1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)

print clf.predict([[160, 0], [150, 1]])
# This predicts two organges.
