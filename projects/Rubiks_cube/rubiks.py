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

        # position in cubic - xyz faces
        self.coods = tuple(product([-1, 0, 1],[-1, 0, 1],[-1, 0, 1])) 
        self.coods_xyz = tuple(product(self.coods, [0,1,2])) 

        # xyz faces - position in face
        self.faces = tuple(product([-1, 1],[0, 1, 2 ])) # (pos-neg , xyz )
        self.1yz_cood = tuple(product([-1, 0, 1],[-1, 0, 1])) 
        self.faces_yz = tuple(product(self.faces, self.1yz_cood)) 
    
        self.moves= tuple(product([-1, 1],[0, 1, 2 ],[90,180,270])) 
        
        # the operator we want is a mapping of 
        # face_yz + moves -> face_yz_new 
        # rubic_new[face_yz] = operator= dict{(face_yz_new, move) : face_yz_old}

        self.phase = tuple(product([-1, 0, 1],[-1, 0, 1],[-1, 0, 1])) 
        self.opg = op_generator()
        self.ijk_cross = self.opg.ijk_cross_rules()
        self.rubiks = {cood: ('r','g','b') for cood in self.coods }
        self.init_rubiks()
        print(self.rubiks)
    
    def init_rubiks (self) :
        for face in self.faces:
            self.pick_faces(face)
            self.paint_rubiks() 
            self.unpick_faces(face)

    # This is not the most efficient way to twist a face. But it is how we
    # think in brain. The efficiency should be left for compiler to consider
    # move = ( pos or nag ,  xyz ,  angle/90 ) 
    def rubiks_move(self, move):
        face =(move[0],move[1])
        self.pick_faces(face)
        for times in range(int(move[2]/90)):
            self.rotate_1yz_90()
        self.unpick_faces(face)

    def pick_faces(self,face =(1 , 0)):
        self.rotate_xyz_rubiks(face[1]) 
        if face[0] == -1: 
            self.flip_rubiks() 

    def unpick_faces(self,face =(1 , 0)):
        if face[0] == -1:
            self.flip_rubiks() 
        self.rotate_xyz_rubiks(3 - face[1] ) 

    def flip_rubiks (self):
        self.rubiks = { (-k[0],) + k[1:] : v for k,v in self.rubiks.items()}

    def rotate_xyz_rubiks (self, n):
        self.rubiks = { self.opg.cshift_list(k,n) : self.opg.cshift_list(v,n) for k,v in self.rubiks.items()}

    def paint_rubiks (self):
        co = next(self.color)
        print(co)
        self.rubiks.update({k :((co,) + v[1:]) for k,v in self.rubiks.items() if k[0] == 1})

    def show_faces(self,face):
        print(face)
        self.pick_faces(face)
        for z in [-1, 0, 1] : 
            print( self.rubiks[(1,-1,z)][0], self.rubiks[(1,0,z)][0], self.rubiks[(1,1,z)][0]) 
        self.unpick_faces(face)

    def show_rubiks(self):
        for face in self.faces:
            self.show_faces(face) 

    def rotate_1yz_90(self):
        fa = {(k[0], -k[2], k[1]): (v[0],v[2],v[1]) for k,v in
              self.rubiks.items() if k[0] == 1}
        print(fa)
        return self.rubiks.update({(k[0], -k[2], k[1]): (v[0],v[2],v[1]) for k,v in
                      self.rubiks.items() if k[0] == 1})

class op_generator:

    idx_to_ijk = { 0: 'i' , 1: 'j',  2: 'k'} 
    ijk_to_vec = {'i': [1,0,0],  'j': [0,1,0],  'k': [0,0,1]} 
    vec_to_ijk = { (1,0,0):'i' ,   (0,1,0):'j', (0,0,1):'k'} 

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
