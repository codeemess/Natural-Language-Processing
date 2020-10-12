#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 01:04:35 2020

@author: konoha
"""

import sys

class POS_Tagging(object):
    
    def buildTagsAndWordTags(self):
        f1 = open("POS-Tagged-Corpus.txt","r")
        tags = {}
        word_tag = {}
        for line in f1:
            tokens = line.rstrip().split()
            # print(tokens)
            for token in tokens:
                if "<s>" in tags.keys():
                    tags["<s>"] += 1
                else:
                    tags["<s>"] = 1
                
                if "</s>" in tags.keys():
                    tags["</s>"] += 1
                else:
                    tags["</s>"] = 1
                if not token in word_tag.keys():
                    word_tag[token] = 1
                else:
                    word_tag[token] = word_tag[token] + 1
                token_split = token.split("_")
                tag = token_split[1]
                if not tag in tags.keys():
                    tags[tag] = 1
                else:
                    tags[tag] = tags[tag] + 1
        total_tags = sum(tags.values())
        
        return tags,word_tag,total_tags,self.TagsGivenTags()
    
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
    
    def TagsGivenTags(self):
        f1 = open('./POS-Tagged-Corpus.txt', 'r')
        Lines = f1.readlines() 
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
                tag = word.split('_')[1]
                z.append(tag)
            z.append("</s>")
            split_content.append(z)
        
        return self.__bigramCounts(split_content)
    
    def test(self,sentence):
        tags, word_given_tag, total_tags, tags_given_tags = self.buildTagsAndWordTags()
        split_sentence = sentence.split()
        f1 = open("result.txt","w")
        prediction = []
        for i in range(0, len(split_sentence)):
            prediction.append("NNP") #If everything is zero default is NNP
            
            if i==0:
                max_probability_tag = 0
                for tag in tags.keys():
                    prior = 0
                    likelihood = 0
                    if( ("<s>", tag) in tags_given_tags.keys()):
                        prior_of_tag = tags_given_tags[('<s>',tag)]/tags["<s>"]
                        prior = prior_of_tag
                    
                    word = split_sentence[i]
                    if word+"_"+tag in word_given_tag.keys():
                        likelihood = word_given_tag[word+"_"+tag]/tags[tag]
                    probability = prior * likelihood
                    f1.write("P("+tag.upper()+"|"+word+")"+":"+str(likelihood)+"\n")
                    f1.write("P("+tag.upper()+"|"+"<s>"+")"+":"+str(prior)+"\n")
                    if probability > max_probability_tag:
                        max_probability_tag = probability
                        prediction[i] = 0
                        prediction[i] = tag
           
            elif i==len(split_sentence):
                max_probability_tag = 0
                for tag in tags.keys():
                    prior = 0
                    likelihood = 0
                    if( (tag, "</s>") in tags_given_tags.keys()):
                        prior_of_tag = tags_given_tags[(tag, "</s>")]/tags[tag]
                        prior = prior_of_tag
                    
                    word = split_sentence[i]
                    if word+"_"+tag in word_given_tag.keys():
                        likelihood = word_given_tag[word+"_"+tag]/tags[tag]
                    probability = prior * likelihood
                    f1.write("P("+tag.upper()+"|"+word+")"+":"+str(likelihood)+"\n")
                    f1.write("P("+tag.upper()+"|"+prediction[i-1]+")"+":"+str(prior)+"\n")
                    if probability > max_probability_tag:
                        max_probability_tag = probability
                        prediction[i] = 0
                        prediction[i] = tag
                        
            else:
                max_probability_tag = 0
                for tag in tags.keys():
                    prior = 0
                    likelihood = 0
                    if( (prediction[i-1], tag) in tags_given_tags.keys()):
                        prior_of_tag = tags_given_tags[(prediction[i-1],tag)]/tags[prediction[i-1]]
                        prior = prior_of_tag
                    
                    word = split_sentence[i]
                    if word+"_"+tag in word_given_tag.keys():
                        likelihood = word_given_tag[word+"_"+tag]/tags[tag]
                    probability = prior * likelihood
                    f1.write("P("+tag.upper()+"|"+word+")"+":"+str(likelihood)+"\n")
                    f1.write("P("+"</s>"+"|"+tag.upper()+")"+":"+str(prior)+"\n")
                    if probability > max_probability_tag:
                        max_probability_tag = probability
                        prediction[i] = 0
                        prediction[i] = tag
                        
            
        return_sentence = ""
        for i in range(0,len(split_sentence)):
            x = ""
            x = split_sentence[i] +"_" + prediction[i] + " "
            return_sentence = return_sentence + x
        
        #print(return_sentence)
        return return_sentence
                

def main():
    P = POS_Tagging()
    print(sys.argv[1])
    print(P.test(sys.argv[1]))
    print("check file result.txt")

main()