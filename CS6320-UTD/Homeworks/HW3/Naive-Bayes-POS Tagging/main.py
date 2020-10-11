#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 05:50:43 2020

@author: pratt
"""
import sys
from bigram import Bigram
def main():
    bg = Bigram()
    bg.train()
    print(sys.argv[1])
    p,q,r = bg.test(sys.argv[1])
    print("------Unsmooth Probability---------")
    print('{:.60f}'.format(p))
    print("------Laplace Smooth Prob---------")
    print('{:.60f}'.format(q))
    print("------Good Turing Prob---------")
    print('{:.60f}'.format(r))
    
main()