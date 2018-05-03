#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from importlib import reload
# pickle save objects
import pickle,gzip
import numpy as np
from itertools import * 

class rubik3 :
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

        self.moves= tuple(product([-1, 1],[0, 1, 2 ],[90,180,270])) 

        self.rubiks = tuple() 

        # the operator we want is a mapping of 
        # face_yz + moves -> face_yz_new 
        # rubic_new[face_yz] = operator= dict{(face_yz_new, move) : face_yz_old}

        self.create_mapping()
        self.init_rubiks()
        self.rubiks_to_status()
        print(self.rubiks)
    
    def init_rubiks (self) :
        for face in self.faces:
            self.pick_faces(face)
            self.paint_rubiks() 
            self.unpick_faces(face)

    def rubiks_to_status (self) :
        self.status = tuple(self.rubiks[cood][xyz]  for cood, xyz in self.coods_xyz)

    def status_to_rubiks(self) :
        for cood in self.coods : 
            v = tuple(self.status[self.coods_xyz.index((cood,n))] for n in range(3))
            self.rubiks.update({cood:v })

    def create_mapping (self):
        #  { data o : data o} -> {data n : data o}  ->  { id n : id o }
        self.mapping =() 
        for move in self.moves:
            self.rubiks = {cood: ((cood,0), (cood,1),(cood,2)) for cood in self.coods}
            self.rubiks_move(move)
            move_mapping= tuple(self.rubiks[cood][xyz]  for cood, xyz in self.coods_xyz) 
            self.mapping += (tuple(map(self.coods_xyz.index, move_mapping)),)
        
    def map_move(self, move_id):
        mapping = self.mapping[move_id]
        self.status = [self.status[mapping[cid]] for cid in
                       range(len(self.coods_xyz))]
    # This is not the most efficient way to twist a face. But it is how we
    # think in brain. The efficiency should be left for compiler to consider
    # All rubik moves could be composed by flip, select axies, rotate the
    # selected face to specific angle, then return the rubiks back to origional 
    # perspective for next move. 
    # move = ( pos or nag ,  xyz ,  angle/90 )  In total 2 * 3 * 3 = 18 moves 
    def rubiks_move(self, move):
        face =(move[0],move[1])
        self.pick_faces(face)
        for times in range(int(move[2]/90)):
            self.rotate_1yz_90()
        self.unpick_faces(face)

    def pick_faces(self,face):
        self.rotate_xyz_rubiks(face[1]) 
        if face[0] == -1: 
            self.flip_rubiks() 

    def unpick_faces(self,face):
        if face[0] == -1:
            self.flip_rubiks() 
        self.rotate_xyz_rubiks(3 - face[1] ) 


    def flip_rubiks (self):
        self.rubiks = { (-k[0],) + k[1:] : v for k,v in self.rubiks.items()}

    def rotate_xyz_rubiks (self, n):
        self.rubiks = {self.cshift_list(k,n) : self.cshift_list(v,n) for k,v in self.rubiks.items()}

    def rotate_1yz_90(self):
        return self.rubiks.update({(k[0], -k[2], k[1]): (v[0],v[2],v[1]) for k,v in
                      self.rubiks.items() if k[0] == 1})

    def paint_rubiks (self):
        co = next(self.color)
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

    def cshift_list(self, seq, n):
        n = n % len(seq)
        return seq[n:] + seq[:n]

def main():
    reload(sys)                         # 2
    rb = rubiks()
    print(list(rb.coods))

if __name__ == '__main__':
    main()

