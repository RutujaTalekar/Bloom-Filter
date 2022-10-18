# Bloom-Filter
Python implementation of bloom filter to analyze the false positive rates for different number of hash functions.

- Instruction to Run the code:  
  Clone the git repository
  Install the following dependency before running the program.
  1. $pip install mmh3
  2. $pip install bitarray
  3. $pip install matplotlib  

  Run the command $ python bf.py input.txt  

- Assumtions made.   
  The output graph uses following values to plot FP_Rate:   
  k (no. of hash functions) = 2,4,8,16  
  n (no. of words) =  100, 250, 500, 750, 1000, 2500, 5000, 7500, 10,000 and 25,000  
  You can initialize m (bloom filter size) in the input.txt file  
  Input.txt file contains the following:
  Line 1 : Bloom Filter Size  
  Line 2 : List of words for testing membership  

- Project Members  
  Rutuja Talekar, Nruthya Kadam, Swarali Gujarathi.
