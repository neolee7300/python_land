#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from importlib import reload
# pickle save objects
import pickle,gzip

# Aux functions
def cshift_list(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]

class op_generator:
    
    def ijk_cross_rules(self, inputs):   # inputs as tuple? 
        # rule1 :  i j k are rotating invariant 
        # i:0 , j :1 , k:2   ,   
        shift = inputs[0]
        p1, p2 =  0, inputs[1] - shift 
        # rule2  i x i = 0  i x j = k   i x k = -j
        rule2 = {(0, 0): [0,0,0] , (0, 1): [0,0,1]  , (0, 2 ) : [0,-1,0]} 
        return cshift_list(rule2[(p1,p2)] , -shift) 

def main():
    reload(sys)                         # 2

if __name__ == '__main__':
    main()
