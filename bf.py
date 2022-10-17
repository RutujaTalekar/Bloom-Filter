# -*- coding: utf-8 -*-
"""
Created on Sun Oct  9 20:21:27 2022

@author: ritu1
"""

from cProfile import label
import math
import mmh3
from bitarray import bitarray
import sys
import matplotlib.pyplot as plt

#from random import shuffle

class BloomFilter(object):
    def __init__(self, items_count, hash_count, bf_size):
        self.items_count= items_count
        # number of hash functions to use
        self.total_hashs = hash_count
         # Size of bit array to use
        self.size = bf_size
        # False possible probability in decimal
        self.fp_prob = self.getFpProb()
		# Bit array of given size
        self.bit_array = bitarray(self.size)
		# initialize all bits as 0
        self.bit_array.setall(0)
        
    def reset(self):
        del self.bit_array[:]
        print("Bit array has been reset", self.bit_array)
        return True
    
    def add(self, item):
        digests = []
        for i in range(self.total_hashs):
			# i work as seed to mmh3.hash() function
            digest = mmh3.hash(item, i) % self.size
            digests.append(digest)
			# set the bit True in bit_array
            self.bit_array[digest] = True
    
    def membershipCheck(self, item):
        for i in range(self.total_hashs):
            digest = mmh3.hash(item, i) % self.size
            if self.bit_array[digest] == False:
                return False
        return True
    
    def getFpProb(self):
        #P(false positives ) = is given with a formula (1-e^(-kn/m))^k
        kn = self.total_hashs * self.items_count
        val = -kn/self.size
        P = (1-math.exp(val))**self.total_hashs
        return P

def readDataSet():
    #fin = open("wlist_match1.txt")
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
    
    # plt.plot(num_of_words,fp_rate)
    # plt.xlabel('Number of words')
    # plt.ylabel('False positive rate')
    
    fig,ax = plt.subplots()
    # for k,v in dict.items():
    #     ax.plot(num_of_words, v, label= k)
    
    ax.plot(num_of_words, dict[2], color = 'green', label="H2")
    ax.plot(num_of_words, dict[4], color = 'red', label="H4")
    ax.plot(num_of_words, dict[8], color = 'blue', label="H8")
    ax.plot(num_of_words, dict[16], color = 'purple', label="H16")
    
    plt.show()
    return True


dataset = readDataSet()
#m = bloom size, k = number of hash functions used, n = total number of words
m,test_data = readCommands(sys.argv[1])
n = [100, 250, 500, 750, 1000, 2500, 5000, 7500, 10000, 25000]
k = [2,4,8,16]
dict = {2:[],4:[], 8:[], 16:[]}
#Storing values for graph
fp_rates = []


#1 k=2, m=16 n= 100,...........
# for i in range(len(k)):
#     for j in range(len(n)):
#         bf = BloomFilter(n[j], k[i], m)
#         fp_rates[j]= bf.getFpProb()

for i in range(len(n)):
    for key,value in dict.items():
        bf= BloomFilter(n[i], key, m)
        dict[key].append(bf.getFpProb())  

print(dict)

'''
print("Total number of elements added in bloom filter:{}".format(n))
print("Size of bit array:{}".format(bloomf.size))
print("Number of hash functions:{}".format(bloomf.total_hashs))
print("False positive Probability:{}".format(bloomf.fp_prob))
#print("Test the following words:", test_data)
#print("Bloom filter before adding words........")
#print(bloomf.bit_array)
'''

'''
#Using the best fp rate configurations for membership check
bfTest = BloomFilter(n[-1], k[-1], m)
for item in dataset:
	bfTest.add(item)
'''
#Membership test

# for item in test_data:
#     if bfTest.membershipCheck(item):
#         print("Item probably exists in bloom filter")
#     else:
#         print("Item definitely doesnt exists in bloom filter")



#Plot graph
plotGraph(n, dict)


#Test rest function
#print(bfTest.reset())



        