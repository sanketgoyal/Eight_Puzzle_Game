import numpy as np
import itertools
from sys import argv
import ast

script, nodeinfo, nodepath, nodes = argv

#The matrix is feeded as input from the user, and then defined the name, "first_matrix
#[1,2,3],[4,5,6],[0,7,8]

#Feeding the matrix:
input_str=input("Enter nine numbers in this form: [1,2,3],[4,5,6],[7,8,0] \n")
input_list=ast.literal_eval(input_str)
first_matrix=np.array(input_list).reshape(3,3)  

#The goal matrix is given as:
Goal_matrix = np.array([[1,2,3],[4,5,6],[7,8,0]])

#Converting the matrix into a string as required in the output text files
def matrix_str(J):
	chain = list(itertools.chain(*J.T))
	G = ' '.join(map(str, chain))
	return G

#To check, if the given input matrix has a solution. 
#If there is no solution, the code exit's iteself
def solvable(node):
    x=node.ravel()
    x=x.tolist()
    x=[a for a in x if a != 0]
    count=0
    for i in range(0,len(x)):
        y=x[i]
        c=0
        for j in range(i,len(x)):
            if (x[j]<y):
                c=c+1
        count=count+c
    if(count%2==0):
        return ("True")
    else:
        print("The given input has no solution, please rearrange the numbers")

        out_file = open(nodeinfo, 'w')
        out_file.close()

        out_file = open(nodepath, 'w')
        out_file.close()

        out_file = open(nodes, 'w')
        out_file.close()

        exit()


#Find the position of '0' in the parent matrix
def find_zero(first_matrix,num):
        for i,j in enumerate(first_matrix):
            for k,l in enumerate(j):
                if l==num:
                    x=i
                    y=k
        return x,y


#Function to call different functions to swap zero
def move(x,y):
	down(x,y)
	right(x,y)
	up(x,y)
	left(x,y)

#Function to swap downwards
def down(x,y):
	a, b = x, y
	x = x+1
	replace(x, y, a, b)

#Function to swap upwards
def up(x,y):
	a, b = x, y
	x = x-1
	replace(x, y, a, b)

#Function to swap left
def left(x,y):
	a, b = x, y
	y = y - 1
	replace(x, y, a, b)

#Function to swap right
def right(x,y):
	a, b = x, y
	y = y + 1
	replace(x, y, a, b)

#Swapping the zero according to down-up-left-right from above functions
def replace(x, y, a, b):
	if x in range(0, 3) and y in range(0,3):
		M=np.array(first_matrix)
		M[a,b]=M[x,y]
		M[x,y]=0
		M1=matrix_str(M)
		append_matrix(np.array(M),M1)

#Adding the value into the original matrix
def append_matrix(L,S):
	while True:
		count=0

		if S not in All_m:
			All_m.append(S)
			All_matrix.append(np.array(L).tolist())
			updated_child.append(S)
		else:
			break

#Calling back the parent and child matrices when the final matrix is reached
def backtrack():
        H=list(zip(parent_node,child_node))	#Making columns for node indexes
        H1=list(zip(child_node,parent_node))
        l=newl-1
        final0=H[l][0]
        final1=H[l][1]
        m=final1
        path_index.append(m)
        m=final0
        path_index.append(m)
        
        for q in range(0,len(H)):		#Method to call and backtrack
            if H[l-1-q][1] == m:
                m=H[l-1-q][0]
                path_index.append(m)
                if m==0:
                    break

#Creating the three required text files

        #Nodeinfo : Child and Parent node indexes
        out_file = open(nodeinfo, 'w')
        for s in H1:
            out_file.write(str(s) + '\n')
        out_file.close()
        #Node Path : Solution Matrices
        out_file = open(nodepath, 'w')
        for s in path_index[::-1]:
            out_file.write(str(All_m[s]) + '\n')
        out_file.close()
	#Nodes : All the nodes created
        out_file = open(nodes, 'w')
        for s in All_m:
            out_file.write(str(s) + '\n')
        out_file.close()


#Defining the initial parameters and various empty lists as required in the code
G=matrix_str(first_matrix)
F=matrix_str(Goal_matrix)
flag=0
parent_node=[]			#Index of parent node
child_node=[]			#Index of child node
path_index = []			#The index of the path being generated to reach goal node
updated_child = []		#Updated child node after each loop is run
All_m=[]			#Node codes to cross verify matrices
All_matrix = []			#Final matrix where all the nodes found are stored
All_matrix.append(np.array(first_matrix).tolist())
All_m.append(G)
x=0
y=0


#Calling the solvable function to check if the input matrix is solvable
solvable(first_matrix)

#Starting the code with original parent node and re-running for various child nodes
for k in All_matrix:

    if F in updated_child:
        newl=All_m.index(F)
        flag=1

    if flag==1:
        break
    else:
        first_matrix=k
        x,y = find_zero(first_matrix,0)
        e = len(All_matrix)
        updated_child.clear()
        move(x,y)
        f = len(All_matrix)
        z = f-e
        for j in range(0,z):
            parent_node.append(All_matrix.index(k))
            child_node.append(j-z+f)

#Once the goal is reached, calling backtracking function to generate the flow of the nodes 
backtrack()

print("The solution of the given matrix is generated and stored in text files.")
