#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 20:06:13 2020

@author: konoha
"""
#import pandas as pd

f = open('./POS-Tagged-Corpus.txt', 'r')
Lines = f.readlines() 
  
count = 0

content = []
for line in Lines: 
    count +=1
    content.append(line)
    #print("Line{}: {}".format(count, line.strip()))
#print(count)
    
refined_content = []
for line in content:
    X = []
    X = line.split()
    refined_content.append(X)

split_content = []
for x in refined_content:
    z = []
    z.append("<s>")
    for word in x:
        word = word.split('_')[0]
        word = word.lower()
        z.append(word)
    z.append("</s>")
    split_content.append(z)
    
#print(split_content)

count_dictionary = {}

for line in split_content:
    for word in line:
        if word in count_dictionary.keys():
            count_dictionary[word] += 1 
        else:
            count_dictionary[word] = 1

#print(count_dictionary)
bigrams = {}
for i in range(len(split_content)):
    for x in range(len(split_content[i])-1):
        temp = (split_content[i][x], split_content[i][x+1]) # Tuples are easier to reuse than nested lists
        if not temp in bigrams:
            bigrams[temp] = 1
        else:
            bigrams[temp] += 1

#print(bigrams)
            
total_words = 0
for key in count_dictionary.keys():
    total_words += count_dictionary[key]
    
#print(total_words)

with open("bigrams.txt", 'a') as out:
    out.write('Bigram' + '\t' + 'Bigram Count' + '\t' + 'Uni Count' + '\t' + 'Bigram Prob' + '\t' + 'Add One Probability' + '\t' + 'Add One C-star')
    out.write('\n')
    out.close()

for bigram,bigram_count in bigrams.items():
    first_word = bigram[0]
    first_word_count = count_dictionary[first_word] 
    bigram_probability = bigrams[bigram]/first_word_count
    add_one_probability = (bigram_count + 1)/(first_word_count + len(count_dictionary))
    cStar_addOne = ((bigram_count + 1) * first_word_count) / (first_word_count + len(count_dictionary))
    with open("bigrams.txt", 'a') as out:
        out.write(bigram[0] + ' ' + bigram[1] + '\t' + str(bigram_count) + '\t' + str(first_word_count) + '\t' + str(bigram_probability) + '\t' + str(add_one_probability) + '\t' + str(cStar_addOne)) 
        out.write('\n')
        out.close()





