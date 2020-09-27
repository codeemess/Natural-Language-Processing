#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 20:06:13 2020

@author: pratt
"""

class Bigram:
    __zeroOccurenceProbGoodTuring = 0
    __model = {}
    
    def __readAndFormatFile(self):
        f = open('./POS-Tagged-Corpus.txt', 'r')
        Lines = f.readlines() 
          
        count = 0
        
        content = []
        for line in Lines: 
            count +=1
            content.append(line)
            
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
        return split_content
    
    def __unigramCounts(self,split_content):
        count_dictionary = {}
        
        for line in split_content:
            for word in line:
                if word in count_dictionary.keys():
                    count_dictionary[word] += 1 
                else:
                    count_dictionary[word] = 1
        return count_dictionary
    
    
    def __bigramCounts(self,split_content):    
        bigrams = {}
        for i in range(len(split_content)):
            for x in range(len(split_content[i])-1):
                temp = (split_content[i][x], split_content[i][x+1]) 
                if not temp in bigrams:
                    bigrams[temp] = 1
                else:
                    bigrams[temp] += 1
        return bigrams
    
    #print(bigrams)
     
    def __getTotalWords(self,count_dictionary):           
        total_words = 0
        for key in count_dictionary.keys():
            total_words += count_dictionary[key]
        
    #print(total_words)
        
    def __computeBigrams(self,bigrams,count_dictionary):
        with open("bigrams.txt", 'w') as out:
            out.write('Bigram' + '\t' + 'Bigram Count' + '\t' + 'Uni Count' + '\t' + 'Bigram Prob' + '\t' + 'Add One Probability' + '\t' + 'Add One C-star')
            out.write('\n')
            out.close()
            
        goodTuring = self.__goodTuringSmoothing(bigrams,count_dictionary)
        
        for bigram,bigram_count in bigrams.items():
            
            first_word = bigram[0]
            first_word_count = count_dictionary[first_word] 
            bigram_probability = self.__unsmoothedBigram(bigram, bigram_count, first_word_count,len(count_dictionary))
            add_one_probability, cStar_addOne = self.__laplaceBigram(bigram, bigram_count, first_word_count,len(count_dictionary))
            self.__model[bigram]={}
            self.__model[bigram]["count"] = bigram_count
            self.__model[bigram]["prob"] = bigram_probability
            self.__model[bigram]["cstar-addOne"] = cStar_addOne
            self.__model[bigram]["prob-addOne"] = add_one_probability
            for x in goodTuring:
                if bigram_count == x[0]:
                    self.__model[bigram]['cStar-gt'] = x[1]['cStar']
                    self.__model[bigram]['prob-gt'] = x[1]['prob']
            with open("bigrams.txt", 'a') as out:
                out.write(bigram[0] + ' ' + bigram[1] + '\t' + str(bigram_count) + '\t' + str(first_word_count) + '\t' + str(bigram_probability) + '\t' + str(add_one_probability) + '\t' + str(cStar_addOne)) 
                out.write('\n')
                out.close()
    
    def __unsmoothedBigram(self,bigram,bigram_count,first_word_count,vocab_count):
        return (bigram_count/first_word_count)
    
    def __laplaceBigram(self,bigram,bigram_count,first_word_count,vocab_count):
        prob = (bigram_count + 1)/(first_word_count + vocab_count)
        cStar = ((bigram_count + 1) * first_word_count) / (first_word_count + vocab_count)
        return prob, cStar
    
    def __goodTuringSmoothing(self,bigrams,count_dictionary):
        freqOfFreq = {}
        for bigram, count in bigrams.items():
            if count in freqOfFreq.keys():
                freqOfFreq[count]["value"] +=1
            else:
                freqOfFreq[count] = {}
                freqOfFreq[count]["value"] = 1
                freqOfFreq[count]["prob"] = None
        freqOfFreqSorted = sorted(freqOfFreq.items() , key=lambda t : t[0])
 
        for x in range(len(freqOfFreqSorted)-1):
           
            if ((freqOfFreqSorted[x+1][0] - freqOfFreqSorted[x][0]) == 1):
                freqOfFreqSorted[x][1]["cStar"] = (x+1)*(freqOfFreqSorted[x+1][1]['value'])/freqOfFreqSorted[x][1]['value']
                freqOfFreqSorted[x][1]["prob"] = freqOfFreqSorted[x][1]["cStar"]/len(bigrams)
            else:
                freqOfFreqSorted[x][1]["cStar"] = 0
                freqOfFreqSorted[x][1]["prob"] = 0
        #last bucket will never have a bucket ahead
        freqOfFreqSorted[-1][1]['cStar'] = 0
        freqOfFreqSorted[-1][1]['prob'] = 0
        #for Nc=0
        freqOfFreqSorted.append((0, {'prob':freqOfFreqSorted[0][1]['value'] / len(bigrams)}))
        return freqOfFreqSorted
                
    def train(self):
        split_content = self.__readAndFormatFile()
        unigramC = self.__unigramCounts(split_content)
        bigramC = self.__bigramCounts(split_content)    
        self.__computeBigrams(bigramC,unigramC)
        print(self.__model[('the','soaring')])

bg = Bigram()
bg.train()