# A program generates cube layout and AI solve it 

## Convert operator rules to a table function  
I am going to need vector cross operation in this program. Instead of copy 
all the code of cross operator, I am going to generate it from a operator 
generator. 

### operator generator (op_generator) 

  1. op_generator takes rules of an operator
  1. op_generator applies rules on input parameters until getting result
  1. op_generator goes through all possible products of input parameters, applies the rules , get the results. (**
     result could be a function ** ) 
  1. op_generator encodes inputs to a tuple and decodes the tuple to inputs  
  1. op_generator compiles the input as dict key , results as the value   
  1. op_generator returns the dictionary as an operator function 

### Rules of cross operator

  1. i x j = k  
  1. i x i = 0 
  1. i x k = -j
  1. i j k are rotating invariant 


## ToDo
  With the op_generator, I will convert all Rubik's cube moves to a dictionary.
It sounds like a functional programming example. Right?   :)  

## Logics
A Nth rank Rubik cubic has six faces (+x, -x, +y...), 6 * N * N grids

1. We know how to rotate Rubik face (+x) 90 degree   

1. All Rubik movements is equivalent to rotate it in different coordinates 
  * The coordinate could be a rotate of xyz
  * The coordinate could be a flit of axis yxz
  * There are six coordinates of 3D space in total

1. It is easy to rotate a Rubik in data format ((x,y,z), (cx,cy,cz)). Because all rotation related data are there. This
   format has follow cons:
  *  Lots of data are useless at large Rubik rank N
  *  Change coordinates need to modify both (x,y,z) and (cx,cy,cz)
1. We could Store Rubik data in format (face, (fx,fy), c). This format has following 
  Pro, and Cons. 
  * It is easy to id and assign c for each grids
  * There is no useless data
  * Hard to do Rubik rotation on it since all three grids in( (x,y,z), (cx,cy,cz) ) could have very different face,
  (fx,fy) 
1. We need a bi-direction converting function between the two data formats
  * convert (face, fx, fy) to  (x,y,z),(cx,cy,cz) is very easy for the face +x
  * It is actually a special Rubik movement - 0 degree rotation movement

  Now we can have some further thinking. 

1. There are two kind of operations: 
  * changing coordinates, 
  * rotating one Rubik face. 
1. There are some invariants for each operation. 
  * invariants (objects, things … ) means we can assign ID to it
  * invariants (ID) could have associate variable(appearance, descriptions, properties … ) in different perspectives. 
  * An operation is actually a function that changes the ID associated variables to different values 
  Property_before -> Property_after = F_op (Property_before)
  * When the operation is not so complex, we can create a dictionary of {Property_before:Property_after} This dictionary
    is equivalent to the op itself. 
    - When we say an operation is "simple", we mean the total possible properties are in small number. 
    - The difficulty of ((x,y,z),(cx,cy,cz)) is : it is a group of IDs but a single ID object. Though it is convenient
      to apply the rotation on it. It is very hard to create a mapping between groups of IDs, In this data structure,
      the most nature way to describe an ID is ((x,y,z),axis). Then it is much easier to understand what happened the
      group of three IDs under face rotations.  (TODO: This could be a better idea to totally use it replace
      (face,(y,z)) property.) 

1. Apply multiple operations could create new operations. 
  * Some complex operations can be constructed through a series simple operations.
  * Some operations are quite simple in one coordinate(perspective) while very difficult in another coordinate
    - switch coordinate need a way to convert one property set to the property set in new coordinate. This convert is
    also an operation and 
    - we can construct an operation in an easier coordinate in following steps: 
      - switch to new coordinate : op1
      - do the real operation in new coordinate : op2
      - switch back to the original coordinate : op3
      - once we got the combined operation, we can save it as a new dictionary between IDs 

 
## Procedure to create operation mappings

1. Create a list that use ID as key, coordinates as values. {ID : (cood1, cood2 ,cood3 … )} 
1. Go through this dictionary, create dictionaries that return the ID of given coordinates 
1. Pick up the most convenient coordinates, do the operation to get the dictionary of operation {ID : (cood1 ,
   {cood2_old : cood2_new }, cood3, …) }
1. Since the operation are identical as mapping of IDs,  we can convert the operation dictionary to dictionary of
   {ID_old : ID_new}, then convert it in other coordinates to get the description of operation in other coordinates.
   With the help of ID-cood  cood-ID dictionaries, this process is almost free.  
1. After get the mapping of operation in all coordinates, we can always do the next operation in other most convenient
   coordinates and construct complex operations. 
1. Pick up the most convenient coordinates, do the operation to get the dictionary of operation {ID : (cood1 ,
   {cood2_old : cood2_new }, cood3, …) }
1. Since the operation are identical as mapping of IDs,  we can convert the operation dictionary to dictionary of
   {ID_old : ID_new}, then convert it in other coordinates to get the description of operation in other coordinates.
   With the help of ID-cood  cood-ID dictionaries, this process is almost free.  
1. After get the mapping of operation in all coordinates, we can always do the next operation in other most convenient
   coordinates and construct complex operations. 
1. Once you had the dictionary of operation, you needn't do the actual operation anymore, just apply the dictionaries
1. Flip the key and value in dictionary , then you get the reverse operation Op' 
1. Those dictionaries that use sorted ID as key could be replaced by list or tuple

## Rubik's cubic related operations 

1. Create the dictionary {ID : (cood,aix)} and reverse dictionary. 
1. Construct operation of rotate the +X face 90 degree   R90 
1. Construct operation of rotate the +X face 180, 270 , 0 degree R90 ^2 ,3  
1. Construct operation of flipping the +X axis to -X axis  Fx
1. Construct operation of shift XYZ axises and keep the hand order   Sxyz 0 1 2 
1. Construct operation change other faces to x axis     Fa2xi = Sxyz Fx  
1. Construct all moves of Rubik cubic   Fa2x Fx R90 ^ m Fx' Fa2x' = M(move)


## Pitfalls

1. (cood: (x,y,z)) is not an ID but a group of three IDs,  (cood,x) (cood,y) (cood,z)  
1. Some operations on  (cood, (x,y,z)) are just linear combination of operations on (cood,x) (cood,y) (cood,z) such as
   op flip(Fx), shift XYZ (Sxyz). While other operation can not be derived from operations on (cood,x), such as rotating
   the +X 90 degree (R90)
1. shift XYZ in right hand order is a different operation from rotate +X plane  
1. ID descriptions such as (cood,x) could serve as dictionary keys. While the  ID group should use dictionary in
   dictionary to store values.  



