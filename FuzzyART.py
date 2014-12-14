import numpy as np
from sys import argv
import matplotlib.pyplot as plt
from random import shuffle

def scaledList(list):
    min = None
    max = None
    for i in range(len(list)):
        if min is None or min > list[i]:
            min = list[i]
        if max is None or max < list[i]:
            max = list[i]
    for i in range(len(list)):
        list[i] = (float)(list[i] - min)/(max - min)
    #print "min = " + str(min) + ", max = " + str(max)
    return list

def complementCodedConversion(list1, list2):
    list = []
    for i in range(len(list1)):
        complementVector = (list1[i], list2[i], 1-list1[i], 1-list2[i])
        list.append(complementVector)
    return list

def fuzzyAnd(tuple1, tuple2):
    ls = []
    for i in range(len(tuple1)):
        ls.append(min(tuple1[i], tuple2[i]))
    return ls


def printData(list):
    for i in range(len(list)):
        print list[i]


def myPlot(dataList, boxList):
    x = map(lambda item:item[0], dataList)
    y = map(lambda item:item[1], dataList)
    plt.scatter(x, y)
    for i in range(len(boxList)):
        (a,b,c,d) = boxList[i]
        plt.plot([a,c,c,a,a], [b, b, d, d, b])

    plt.show()

script, training_file, testing_file = argv
training = np.loadtxt(training_file)
testing = np.loadtxt(testing_file)

trainingData = complementCodedConversion(scaledList(training[:, 2].tolist()), scaledList(training[:, 3].tolist()))
testingData = complementCodedConversion(scaledList(testing[:, 2].tolist()), scaledList(testing[:, 3].tolist()))

#printData(trainingData)

#parameters setting
#learning rate
beta = 1
#vigilance
rho = 0.8
alpha = 0.000001
categoryList = []
#shuffle(trainingData)

while True:
    #shuffle(trainingData)
    len1 = len(categoryList)
    for i in range(len(trainingData)):
        tjList = []
        for j in range(len(categoryList)):
            tjList.append((j, sum(fuzzyAnd(trainingData[i], categoryList[j]))/(alpha+sum(categoryList[j]))))
        tjList = sorted(tjList, key=lambda item:item[1])
        noMatchFlag = True
        while len(tjList) != 0 :
            (index, value) = tjList.pop(0)
            if sum(fuzzyAnd(trainingData[i], categoryList[index]))/sum(trainingData[i]) >= rho :
                categoryList[index] = map(lambda x, y: x*beta + y*(1-beta),
                                          fuzzyAnd(trainingData[i], categoryList[index]), categoryList[index])
                noMatchFlag = False
                break
        if noMatchFlag:
            categoryList.append(trainingData[i])

    novellist = []
    for i in range(len(testingData)):
        tjList = []
        for j in range(len(categoryList)):
            tjList.append((j, sum(fuzzyAnd(testingData[i], categoryList[j]))/(alpha+sum(categoryList[j]))))
        tjList = sorted(tjList, key=lambda item:item[1])
        noMatchFlag = True
        while len(tjList) != 0 :
            (index, value) = tjList.pop(0)
            if sum(fuzzyAnd(testingData[i], categoryList[index]))/sum(testingData[i]) >= rho :
                noMatchFlag = False
                break
        if noMatchFlag:
            novellist.append(i)

    print "***************"
    printData(categoryList)
    print "***************"
    print "Novel list:"
    print novellist
    myPlot(trainingData, categoryList)
    #print "novelist: ", len(novellist)
    len2 = len(categoryList)
    if len2 == len1 :
        break

#print "number of centers: ", len2

