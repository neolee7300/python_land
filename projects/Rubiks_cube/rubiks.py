#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys, os, re 
from importlib import reload
# pickle save objects
import pickle,gzip
from itertools import * 

class rubik3 :
    color = cycle('rgbwyp')

    def __init__(self) :

        self.n = 1 
        self.span =[x for x in range(-self.n, self.n + 1)] 

        # position in cubic - axies 
        self.coods = tuple(cood for cood in product(self.span, self.span, self.span)
                                              if -self.n in cood or self.n in cood) 

        # tool for rotating face, no guarantee what's in it. 
        self.rubiks = { cood: ['no_id','no_id','no_id'] for cood in self.coods}

        # face - position in current face
        self.faces =tuple(x for x in product([-self.n , self.n],[0, 1, 2 ])) # (pos-neg , axies)
        self.face_color = { face : next(self.color) for face in self.faces}

        yz= tuple(x for x in product(self.span, self.span)) # (pos in face)
        
        self.faces_yz= tuple(face_yz for face_yz in product(self.faces, yz))# (faces, (y,z)) index is id
        self.cood_axis = ()  # (cood,axis) index is id 
        self.map_cood_axis_id()

        self.moves= tuple(x for x in product(self.faces, [90,180,270])) 
        self.mapping = {} # {move : mapping = (new_id) } index of new_id is old_id  
        self.create_mapping() #

        self.init_rubiks()
        self.rubiks_to_status()
        print(self.rubiks)
    
    def init_rubiks (self) :
        for face in self.faces : 
            self.pick_faces(face)
            self.paint_rubiks() 
            self.unpick_faces(face)

    # grid is (cood, gn) = face,y,z is an object with (id, color, ... ),  
    def map_cood_axis_id (self):
        print(self.faces_yz)
        for id,(face,(y,z)) in enumerate(self.faces_yz) :
            self.pick_faces(face)
            cood, axis = (self.n,y,z), face[1] 
            self.rubiks = {cood :(id,-1,-1)} 
            self.unpick_faces(face)
            self.cood_axis += tuple((cood,axis) for cood in self.rubiks.keys())
 
    def rubiks_to_status (self) :
        self.status = tuple(self.rubiks[cood][axis] for cood, axis in self.cood_axis)

    def status_to_rubiks(self) :
        for cood in self.coods : 
            v = tuple(self.status[self.cood_axis.index((cood,n))] for n in range(3))
            self.rubiks.update({cood:v})

    def create_mapping (self):
        #  { data o : data o} -> {data n : data o}  ->  { id n : id o }
        # store the index structure direct in value    value[index_struct] = index_struct
        self.mapping = {}
        for move in self.moves:
            self.rubiks = {cood: ((cood,0), (cood,1),(cood,2)) for cood in self.coods}
            self.rubiks_move(move)
            move_mapping= tuple(self.rubiks[cood][axis] for cood,axis in self.cood_axis) 

            self.mapping.update({move:tuple(map(self.cood_axis.index, move_mapping))})
        
    def map_move(self, move):
        self.status = [self.status[nid] for nid in self.mapping[move]]
    # This is not the most efficient way to twist a face. But it is how we
    # think in brain. The efficiency should be left for compiler to consider
    # All rubik moves could be composed by flip, select axies, rotate the
    # selected face to specific angle, then return the rubiks back to origional 
    # perspective for next move. 
    # move = ( pos or nag ,  xyz ,  angle/90 )  In total 2 * 3 * 3 = 18 moves 
    def rubiks_move(self, move):
        face = move[0]
        self.pick_faces(face)
        for times in range(int(move[1]/90)):
            self.rotate_1yz_90()
        self.unpick_faces(face)

    def pick_faces(self,face):
        self.rotate_xyz_rubiks(face[1]) 
        if face[0] < 0 : 
            self.flip_rubiks() 

    def unpick_faces(self,face):
        if face[0] < 0 :
            self.flip_rubiks() 
        self.rotate_xyz_rubiks(3 - face[1] ) 

    def flip_rubiks (self):
        self.rubiks = { (-k[0],) + k[1:] : v for k,v in self.rubiks.items()}

    def rotate_xyz_rubiks (self, n):
        self.rubiks = {self.cshift_list(k,n) : self.cshift_list(v,n) for k,v in self.rubiks.items()}

    def rotate_1yz_90(self):
        return self.rubiks.update({(k[0], -k[2], k[1]): (v[0],v[2],v[1]) for k,v in
                      self.rubiks.items() if k[0] == self.n})

    def paint_rubiks (self):
        co = next(self.color)
        self.rubiks.update({k :((co,) + v[1:]) for k,v in self.rubiks.items()
                            if k[0] == self.n})

    def show_faces(self,face):
        print(face)
        self.pick_faces(face)
        for z in self.span :
            print( [self.rubiks[(self.n, y, z)][0] for y in self.span] )
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

