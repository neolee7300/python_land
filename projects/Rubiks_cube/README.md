== A python program that generates random cube layout and solve it with AI  

# Convert an operator rules to a table function  
I am going to need vector cross operation in this program. Instead of copy 
all the code of cross operator, I am going to generate it from a operator 
generator. 

## operator generator (op_generator) 

  1. op_generator takes rules of an operator
  1. op_generator applies rules on input parameters until getting result
  1. op_generator goes through all possible products of input parameters,
    applies the rules , get the results. (** result could be a function ** ) 
  1. op_generator encodes inputs to a tuple and decodes the tuple to inputs  
  1. op_generator compiles the input as dict key , results as the value   
  1. op_generator returns the dictionary as an operator function 

## Rules of cross operator
  1. i x j = k  
  1. i x i = 0 
  1. i x k = -j
  1. i j k are rotating invariant 


## ToDo
  With the op_generator, I will convert all Rubik's cube moves to a dictionary.
It sounds like a functional programming example. Right?   :)  

