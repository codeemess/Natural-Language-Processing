#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 01:04:35 2020

@author: konoha
"""
class POS_Tagging(object):
    tags = {}
    word_given_tag = {}
    tag_given_tag = {}
    
    def buildTagsAndWordTags(self):
        f1 = open("POS-Tagged-Corpus.txt","r")
        tags = {}
        word_tag = {}
        for line in f1:
            tokens = line.rstrip().split()
            # print(tokens)
            for token in tokens:
                if not token in word_tag.keys():
                    word_tag[token] = 1
                else:
                    word_tag[token] = word_tag[token] + 1
                token_split = token.split("_")
                word = token_split[0]
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
        
    
p = POS_Tagging()
p.TagsGivenTags()