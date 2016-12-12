import json
import unicodedata
import random
import math
import operator
import unittest

def def_dictionary(dic1, dic2):
    sno = 1
    business = open('C:\\sample_knn.json')
    for line in business:
        dic1[sno] =  json.loads(line).get('business_id')
        dic2[json.loads(line).get('business_id')] = sno
        sno = sno + 1

def loadDataset(split, trainingSet=[] , testSet=[]):
    dataset = []
    business = open('C:\\sample_knn.json')
    for line in business:
        id_ = json.loads(line).get('business_id')
        review_count = json.loads(line).get('review_count')
        stars = json.loads(line).get('stars')
        dataset.append([review_count, id_, stars])
	#dataset = list(business)
    for x in range(len(dataset)-1):

            if random.random() < split:
                trainingSet.append(dataset[x])
            else:
                testSet.append(dataset[x])

#==========================================================================

def euclideanDistance(instance1, instance2, length):
	distance = 0

	y0 = math.pow((instance2[2] - instance1[2]), 2)# (y2-y1)^2
	x0 = math.pow((instance2[0] - instance1[0]), 2)# (x2-x1)^2

	distance = y0 + x0

	return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance)-1
    for x in range(len(trainingSet)):
	    dist = euclideanDistance(testInstance, trainingSet[x], length)
	    distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
    	    neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

def getrmse(testSet, predictions):
	correct = 0
	for x in range(len(testSet)):
		if testSet[x][-1] == predictions[x]:
			correct += 1
	return (correct/float(len(testSet)))

def main():
        training_set = []
        test_set = []
        business_dictionary1 = {}#sno->business name
        business_dictionary2 = {}#business name->sno
        predictions = []

        loadDataset(0.99, training_set, test_set)
        def_dictionary(business_dictionary1,business_dictionary2)
        '''
        a = len(training_set)
        b = len(test_set)
        print a, b
        '''

        for i in range(len(training_set)):
            training_set[i][1] = business_dictionary2[training_set[i][1]]
        for i in range(len(test_set)):
            test_set[i][1] = business_dictionary2[test_set[i][1]]

        a = getNeighbors(training_set, test_set[0], 3)
       # print a

        b = getResponse(a)
       # print b

        k = 4
        for x in range(len(test_set)):
            neighbors = getNeighbors(training_set, test_set[x], k)
            #print neighbors
            result = getResponse(neighbors)
            predictions.append(result)
           # print('> predicted rating =' + repr(result)+ ' for business: ' + business_dictionary1[test_set[x][1]])

        print getrmse(test_set, predictions)

class MyTest(unittest.TestCase):
    def test_1(self):
        a=np.matrix('1 2 ; 3 4')
        b=np.matrix('4 5 ; 6 7')

        self.assertEqual(rmse(a,b), 3)

unittest.main()
main()
