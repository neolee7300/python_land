#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from importlib import reload
# pickle save objects
import pickle,gzip
import numpy as np
from itertools import * 

class rubik3 :
    coods = ()
    color = cycle( ('r','g','b','w','y','p') )
    def __init__(self) :
        a = np.array([1,0,0])  
        b = np.array([0,1,0])  
        acb = np.cross(a,b)

        print(self.coods)
        self.coods = product([-1, 0, 1],[-1, 0, 1],[-1, 0, 1]) 
        self.opg = op_generator()
        self.ijk_cross = self.opg.ijk_cross_rules()
        self.rubiks = {cood: ('r','g','b') for cood in self.coods }
        self.init_rubiks()
        print(self.rubiks)
    
    def init_rubiks (self) :
        for i in range(0,3) :
            self.rotate_xyz_rubiks()
            self.paint_rubiks() 
            self.flip_rubiks() 
            self.paint_rubiks() 

    def flip_rubiks (self):
        self.rubiks = { (-k[0],) + k[1:] : v for k,v in self.rubiks.items()}

    def rotate_xyz_rubiks (self):
        self.rubiks = { self.opg.cshift_list(k,1) : v for k,v in self.rubiks.items()}

    def paint_rubiks (self):
        co = next(self.color)
        print(co)
        self.rubiks.update( { k :((co,) + v[1:]) for k,v in self.rubiks.items() if k[0] == 1})

    def vec_plus (self, a, b) :
        return list(map(lambda x, y: x+y, a, b))

    def vec_scale (self, s, v) :
        return [s * vi for vi in v] 

    def vec_cross (self, a, b) :
        result = [0, 0, 0]
        for x,y in product([0, 1, 2], [0, 1, 2]) :
            scale = a[x]*b[y]     
            input = (self.opg.idx_to_ijk[x] , self.opg.idx_to_ijk[y])
            result = self.vec_plus(result, self.vec_scale(scale, self.ijk_cross[input]))
        return result

    def rotate_1yz_90(self, coods):
        for cood in coods :
            if cood[0] == 1 :
                cood_r = ((cood[0],) + (- cood[2], cood[1]))
        return(cood_r)


    def rotate_rubiks(self, coods):
        return coods    

class op_generator:

    idx_to_ijk = { 0: 'i' , 1: 'j',  2: 'k'} 
    ijk_to_vec = {'i': [1,0,0],  'j': [0,1,0],  'k': [0,0,1]} 
    vec_to_ijk = { (1,0,0):'i' ,   (0,1,0):'j', (0,0,1):'k'} 

    def rotate_input(self, input, n):
        result = ()
        print(input)
        for ijk in input:
            vec = self.cshift_list(self.ijk_to_vec[ijk], n)
            result += tuple(self.vec_to_ijk[tuple(vec)])
        return result
    
    def flip_input(self, input,n1, n2 ):
        input = list(input);
        input[n1], input[n2] = input[n2] , input[n1]
        return (tuple(input)) 

    def ijk_cross_rules(self):   # inputs as tuple? 
        # rule0  i x i = 0  i x j = k   i x k = -j
        rule0 = {('i', 'i'): [0,0,0] , ('i', 'j'): [0,0,1] , ('i','k') : [0,-1,0]} 

        # rule1  rotate i, j k, results are the same in rotated ijk  
        for n in range(1,3) :
            rotate = {self.rotate_input(k,n) : self.cshift_list(v,n) for k,v in rule0.items()}
            rule0.update(rotate)

        # rule2 flip input, the result is negative 
        flip = {self.flip_input(k,0,1) : self.neg_vec(v) for k,v in rule0.items()}
        rule0.update(flip)

        return rule0 

    # Aux functions
    def cshift_list(self, seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]

    def neg_vec(self, vec):
        return [ -v for v in vec ]

def main():
    reload(sys)                         # 2
    opg = op_generator()
    cross_rules = opg.ijk_cross_rules()
    print(cross_rules)
    print(len(cross_rules))
    rb = rubiks()
    print(list(rb.coods))

if __name__ == '__main__':
    main()
