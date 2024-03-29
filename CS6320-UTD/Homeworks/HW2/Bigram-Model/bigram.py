#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 20:06:13 2020

@author: pratt
"""
import pickle as pickle

class Bigram:
    ''' Class bigram contains implementation for the bigram mode'''
    #the data below is populated by the methods
    __model = {}
    __model["zeroProbAddOne"] = {}
    __model["zeroProbGT"] = 0
    __model["unigrams"] = {}
    __goodTuring = []
    
    def __readAndFormatFile(self):
        ''' Loads the POS tagged corpus, appends the start and end line character, splits into lines'''
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
        ''' Counts the occurence of each unigram and returns a dictionary of the same'''
        count_dictionary = {}
        
        for line in split_content:
            for word in line:
                if word in count_dictionary.keys():
                    count_dictionary[word] += 1 
                else:
                    count_dictionary[word] = 1
        return count_dictionary
    
    
    def __bigramCounts(self,split_content): 
        ''' Counts the occurences of bigrams and returns the dictionary of the same'''
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
        ''' counts the total number of tokens in the vocabulary and returns that'''
        total_words = 0
        for key in count_dictionary.keys():
            total_words += count_dictionary[key]
        return total_words
        
    #print(total_words)
        
    def __computeBigrams(self,bigrams,count_dictionary):
        ''' The function calls the other functions and populates the model dictionary with all the values of c and p for the three types'''
            
        total_words = self.__getTotalWords(count_dictionary)
        
        self.__goodTuring = self.__goodTuringSmoothing(bigrams,count_dictionary)
            
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
           
            if first_word in self.__model['zeroProbAddOne'].keys():
                continue
            else:
                self.__model['zeroProbAddOne'][first_word] = first_word_count/(first_word_count+len(count_dictionary))
                
            
            if first_word in self.__model['unigrams'].keys():
                continue
            else:
                self.__model['unigrams'][first_word] = {"count":first_word_count,"prob": first_word_count/total_words}
            
            
            for x in goodTuring:
                if bigram_count == x[0]:
                    self.__model[bigram]['cStar-gt'] = x[1]['cStar']
                    self.__model[bigram]['prob-gt'] = x[1]['prob']
                

    
    def __unsmoothedBigram(self,bigram,bigram_count,first_word_count,vocab_count):
        ''' probability for unsmooth bigram '''
        return (bigram_count/first_word_count)
    
    def __laplaceBigram(self,bigram,bigram_count,first_word_count,vocab_count):
        ''' probability for add one smoothing bigram'''
        prob = (bigram_count + 1)/(first_word_count + vocab_count)
        cStar = ((bigram_count + 1) * first_word_count) / (first_word_count + vocab_count)
        return prob, cStar
    
    def __goodTuringSmoothing(self,bigrams,count_dictionary):
        ''' Implements the good turing smoothing that sets c* = 0 if Nc+1 = 0'''
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
        self.__model['zeroProbGT'] = freqOfFreqSorted[0][1]['value'] / len(bigrams)
        #print(freqOfFreqSorted)
        return freqOfFreqSorted
    
    def writeModelToFile(self):
        ''' writes the trained model to a file'''
        with open('bigrams.txt', 'wb') as file:
            file.write(pickle.dumps(str(self.__model))) # use `pickle.loads` to do the reverse
    
    def train(self):
        ''' trains the bigram model on the provided corpus'''
        split_content = self.__readAndFormatFile()
        unigramC = self.__unigramCounts(split_content)
        bigramC = self.__bigramCounts(split_content)    
        self.__computeBigrams(bigramC,unigramC)
        self.writeModelToFile()
        
    def test(self,sentence):
        ''' given a sentence it calculates the probability of the sentence'''
        testSen = sentence.split()
        z = []
        z.append("<s>")
        for word in testSen:
            word = word.split('_')[0]
            word = word.lower()
            z.append(word)
        z.append("</s>")
        #print(z)
        p = self.testBigram(z)
        q = self.testLaplaceSmoothBigram(z)
        r = self.testGTBigram(z)
        return p,q,r
        # '{:.60f}'.format(self.testGTBigram(z))
 
        
    def testBigram(self,sentence_arr):
        ''' calculates un smoothed bigram probability on test sentence'''
        prob = None
        for i in range(0,len(sentence_arr)-1):
            if i == 0:
                prob = self.__model['unigrams'][sentence_arr[i]]['prob']
            else:
                if (sentence_arr[i-1],sentence_arr[i]) in self.__model.keys():
                    bigramProb = self.__model[(sentence_arr[i-1],sentence_arr[i])]['prob']  
                    prob *= bigramProb
                else:
                    prob = 0
        return prob
    
    
    def testLaplaceSmoothBigram(self,sentence_arr):
        ''' calculates laplace smoothed probability on test sentence'''
        prob = None
        for i in range(0,len(sentence_arr)-1):
            if i == 0:
                prob = self.__model['unigrams'][sentence_arr[i]]['prob']
            else:
                bigramProb = 0
                if (sentence_arr[i-1],sentence_arr[i]) in self.__model.keys():
                    bigramProb = self.__model[(sentence_arr[i-1],sentence_arr[i])]['prob-addOne']
                    laplaceProb = bigramProb
                    prob *= laplaceProb
 
                    
        return prob
        
    def testGTBigram(self,sentence_arr):
        ''' calculates good turing discounting smoothing probability of the sentence ''' 
        prob = None
        for i in range(0,len(sentence_arr)-1):
            if i == 0:
                prob = self.__model['unigrams'][sentence_arr[i]]['prob']
            else:
                bigramProb = 0
                if (sentence_arr[i-1],sentence_arr[i]) in self.__model.keys():
                    #print(self.__model[(sentence_arr[i-1],sentence_arr[i])])
                    # bigramProb = self.__model[(sentence_arr[i-1],sentence_arr[i])]['prob-gt']
                    
                    for x in self.__goodTuring:
                        if x[0] == self.__model[(sentence_arr[i-1],sentence_arr[i])]['count']:
                            bigramProb = x[1]['prob']
                        
                    unigramProb = self.__model['unigrams'][sentence_arr[i-1]]["prob"]
                    gt = bigramProb/unigramProb
                    prob *= gt
                else:
                    unseenProb = self.__model['zeroProbGT']
                    if (sentence_arr[i-1]) in self.__model['unigrams'].keys():
                        unigramProb = self.__model['unigrams'][sentence_arr[i-1]]["prob"]
                        gt = unseenProb/unigramProb
                        prob *= gt
                    else:
                        prob = 0
        return prob