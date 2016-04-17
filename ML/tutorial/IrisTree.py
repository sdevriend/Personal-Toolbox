#!/usr/bin/python
import numpy
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot




iris = load_iris()
#print iris.data[0]
#for i in range(len(iris.target)):
#	print "Voorbeeld %d: label %s, features %s" % (i, iris.target[i], iris.data[i])

test_index = [0, 50, 100]

# training data
train_target = numpy.delete(iris.target, test_index)
train_data = numpy.delete(iris.data, test_index, axis=0)

# test dataset
test_target = iris.target[test_index]
test_data = iris.data[test_index]


clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)
print clf.predict(test_data)


dot_data = StringIO() 
tree.export_graphviz(clf, out_file=dot_data,
                     feature_names=iris.feature_names,
                     class_names=iris.target_names,
                     filled=True, rounded=True,
                     impurity=True,
                     leaves_parallel=True)
graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
graph.write_pdf("iris.pdf") 
