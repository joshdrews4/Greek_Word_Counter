# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 14:14:16 2018

@author: Joshua Drews

Date: 5/16/18

General Comments: This function counts the frequency of words appearing in any
Greek or English text. Note that this function does not aggregate based on declension or
conjugation, but instead only counts together words that are literally equal.
It is possible that this script also can process languages that are not English
or Greek, but that has not been tested. This code is an extension of 
WordCounter.py that was written for BIOINF 575.

Input: The text file desired to be counted, the lower bound of count of the
words to be displayed, the upper bound of count of words to be displayed (i.e.
only words with lower <= count <= upper will be displayed).

Input can take three forms:
    wordCounterGreek.py TEXT.txt lowerbound upperbound
    wordCounterGreek.py TEXT.txt lowerbound
        No upperbound
    wordCounterGreek.py TEXT.txt
        No upperbound or lower bound
    
Output: A list of words and their count in descending order.
    

"""

import sys
import string
import json


"""
General Comments: This funciton remove punctuation from each line in the file
and stips it of spaces.

Input: A line of text.

Output: The same line without punctuation and spaces.
"""
def process_line(line):
    punctuation = string.punctuation

    line = line.lower()
    for i in range(len(punctuation)):
        line = line.replace(punctuation[i], '') #Delete punctuation
    line = line.split()
    for j in range(len(line)):
        line[j]=line[j].strip() #Delete spaces
    return line

"""
General Comments: This function counts words in a line and adds them to the
existing word count dictionary.

Input: A list of words to be added to the dictionary, the dictionary.

Output: The updated dictionary.
"""
def accumulate_counts(wordList, wordCounts):
    for i in range(len(wordList)):
        if wordList[i] in wordCounts:
            wordCounts[wordList[i]]+=1 #Add to an existing entry in the dictionary
        else:
            wordCounts[wordList[i]]=1 #Create a new entry in the dictionary
    return wordCounts


"""
General Comments: This function sorts the word count dictionary in descending
order.

Input: The word count dictionary.

Output: The sorted word count dictionary.
"""
def sort_words(wordCounts):
    wordCounts = sorted(wordCounts.items()) #Sort alphabetically
    wordCounts.sort(key=lambda x: x[1], reverse = True) #Sort by total word count
    return wordCounts


"""
General Comments: The main script. First processes each line, then adds each
line to the word count dictionary, then filters out the words that do not fit
within the upper and lower count bounds, then sorts the word count dictionary.
"""
def main():
    fileName = sys.argv[1] #The file name that will be processed
    
    if len(sys.argv) == 4:
        lower = sys.argv[2] #The lower bound of count for the words to be displayed
        upper = sys.argv[3] #The upper bound of count for the words to be displayed
        
    if len(sys.argv) == 3:
        lower = sys.argv[2] #The lower bound of count for the words to be displayed
        upper = 1000000 #The upper bound of count for the words to be displayed
        
    if len(sys.argv) == 2:
        lower = 0 #The lower bound of count for the words to be displayed
        upper = 1000000 #The upper bound of count for the words to be displayed
    
    wordCounts={} #Define the empty word count dictionary
            
    with open(fileName, 'r', encoding = "utf8") as inFile:
        lines = inFile.readlines()
        for i in range(len(lines)):
            wordList = process_line(lines[i]) #Process each line for punctuation
            accumulate_counts(wordList, wordCounts) #Add to existing word count dictionary
        inFile.close()
            
    for k in list(wordCounts):
        if wordCounts[k] < int(lower) or wordCounts[k] > int(upper):
            del wordCounts[k] #Delete the words that do not have a count between upper and lower
    
    wordCounts = sort_words(wordCounts) #Sort the dictionary by word count and alphabet
    
    print(json.dumps(wordCounts, ensure_ascii=False)) #Print output

if __name__ == '__main__':
    main()
