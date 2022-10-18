# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 20:21:27 2022

@author: ritu1
"""

from cProfile import label
import math
from turtle import color
import mmh3
from bitarray import bitarray
import sys
import matplotlib.pyplot as plt

#from random import shuffle

class BloomFilter(object):
    def __init__(self, total_words, hash_count, bf_size):
        self.total_words= total_words
        # number of hash functions to use
        self.total_hashs = hash_count
         # Size of bit array to use
        self.bf_size = bf_size
        # False possible probability in decimal
        self.fp_rate = self.getFpRate()
		# Bit array of given size
        self.bit_array = bitarray(self.bf_size)
		# initialize all bits as 0
        self.bit_array.setall(0)
        
    def reset(self):
        del self.bit_array[:]
        print("The bloom filter bit array has been reset", self.bit_array)
        return True
    
    def insert(self, item):
        digests = []
        for i in range(self.total_hashs):
            digest = mmh3.hash(item, i) % self.bf_size  
            digests.append(digest)
            self.bit_array[digest] = True
    
    def testmembership(self, item):
        for i in range(self.total_hashs):
            digest = mmh3.hash(item, i) % self.bf_size
            if self.bit_array[digest] == False:
                return False
        return True
    
    def getFpRate(self):
        #P(false positives ) = is given with a formula (1-e^(-kn/m))^k
        kn = self.total_hashs * self.total_words
        val = -kn/self.bf_size
        P = (1-math.exp(val))**self.total_hashs
        return P
    
    
def getOptimalHashFns(bf_size,total_words):
        # Optimal k = (m/n) * lg(2)
        return int((bf_size/total_words) * math.log(2))       

def readDataSet():
    with open("wlist_match12.txt") as file_in:
        lines = []
        for line in file_in:
            lines.append(line.strip('\n'))
    return lines

def readCommands(filename):
    fin = open(filename, "r")
    bfSize = int(fin.readline())
    #numHashes = int(fin.readline())
    wordList = fin.readline()
    testData = wordList.split(",")
    fin.close()
    return bfSize,testData
    
def plotGraph(num_of_words, dict):
    fig,ax = plt.subplots()
    # for k,v in dict.items():
    #     ax.plot(num_of_words, v, label= k)
    plt.title("Bloom Filter Performance Analysis", weight="bold", color="blue")
    ax.plot(num_of_words, dict[2], color = 'green', label="H2")
    ax.plot(num_of_words, dict[4], color = 'red', label="H4")
    ax.plot(num_of_words, dict[8], color = 'blue', label="H8")
    ax.plot(num_of_words, dict[16], color = 'purple', label="H16")
    ax.set_xlabel("Number of words", weight = "bold")
    ax.set_ylabel("False positive rate", weight = "bold")
    plt.legend()
    plt.show()
    return True

'''
def plotGraphOptimalK(num_of_words, fp_rate):
    plt.plot(num_of_words, fp_rate)
    plt.title("Bloom Filter Performance Analysis", weight="bold", color="blue")
    plt.xlabel("Number of words", weight = "bold")
    plt.ylabel("False positive rate", weight = "bold")
    plt.legend()
    plt.show()
    return True
'''

dataset = readDataSet()
#m = bloom size, k = number of hash functions used, n = total number of words
m,test_data = readCommands(sys.argv[1])
n = [100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000, 25000]
k = [2,4,8,16]
#dict will store number of hash functions used : respective FP rate
dict = {2:[],4:[], 8:[], 16:[]}


for i in range(len(n)):
    for key,value in dict.items():
        bf= BloomFilter(n[i], key, m)
        dict[key].append(bf.getFpRate())  

#print(dict)
#Plot graph
print()
print("The graph shows FP rates against the number of words for different count of hash functions for the bloom filter")
plotGraph(n, dict)
print()
'''
fp_rates = []
#Plot optimal K graph
for i in range(len(n)):
    kOptimal = getOptimalHashFns(m,n[i])
    bfOptimalK = BloomFilter(n[i],kOptimal, m)
    fp_rates.append(bfOptimalK.getFpRate())
plotGraphOptimalK(n, fp_rates)
'''






#Using the best fp rate configurations for membership check
bfTest = BloomFilter(n[-2], k[-2], m)      #Taking m = 10000 since it is giving balanced results
for item in dataset:
	bfTest.insert(item)

print("Total number of words - ",bfTest.total_words)
print("Total number of hash functions used -",bfTest.total_hashs)
print("Size of bit array | bloom filter - ",bfTest.bf_size)
print("Projected false positive rate - ",bfTest.getFpRate())
print()

#Membership test
for item in test_data:
    if bfTest.testmembership(item):
        print("The following item could be a member - " + item)
    else:
        print("The following item is not a member - "+ item)

#Reset function
print()
bfTest.reset()




        