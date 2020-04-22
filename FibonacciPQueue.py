#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Gosia Kukiełka
"""
from random import shuffle

class Node:
    def __init__(self, key):
        self.key=key
        self.child=self.parent=None
        self.left=self.right=self 
        self.degree=0 #number of children
        
    def __str__(self):
        return str(self.key)

class PQueue:   
    """
    Priority queue based on Fibonacci heap with the following properties:
    -> it consits of a collection of heap-ordered trees
    -> the roots of all trees are linked using a circular doubly linked list
    -> each node is of at most O(log to n to base phi)
       where phi = (1+5^0.5)/2)
"""    
    def __init__(self, L, cmp=lambda x,y: x<y): 
        self.cmp=cmp
        self.n=0
        self.min=None
        if L:  #add L elements to the heap
            for i in L: self.Insert(i)
    
    def __len__(self):
        return self.n
        
    def isEmpty(self): #O(1)
        return self.min==None
    
    def AddToRoots(self, node):
        if self.min!=None:
            node.left = self.min
            node.right = self.min.right
            self.min.right = node
            node.right.left = node
            
            if self.cmp(node.key, self.min.key):
                self.min = node
        else:
            self.min=node
    
    def RemoveFromRoots(self, node): 
        if self.min!=None and self.min.left!=None:
            node.left.right = node.right
            node.right.left = node.left 

    def Insert(self, value): #O(1)
        node=Node(value)
        self.AddToRoots(node)
        self.n+=1
      
    def ExtractMin(self): #logarytmiczna  (O(logn), amortyzowana)
        min_node=self.min
        if min_node:
            if min_node.degree>0: 
               #add MIN's children to the root list - O(degree)
                child_tmp=min_node.child.left
                while min_node.child.parent!=None:
                    child_tmp.parent=None
                    next_child=child_tmp.left
                    self.AddToRoots(child_tmp)
                    child_tmp=next_child

            #remove from the root list
            self.RemoveFromRoots(min_node)
            
            if min_node == min_node.right: 
                self.min=None
            else:
                self.min=min_node.right
                self.Consolidate() #O(log n)
            self.n -=1
        return min_node.key
    
    def Consolidate(self): 
        #array of roots with i-th degree; A[i] = root node with i children
        A=[None for i in range(int(math.log(self.n, (1 + math.sqrt(5)) / 2)) + 1)]
        
        #diversify degrees of root noddes
        while self.min:
            x=self.min
            self.min=None if x.left == x else x.left
            self.RemoveFromRoots(x)
            x.right=x.left = x
            d=x.degree
            
            while A[d]!=None:
                y=A[d]
                if not self.cmp(x.key, y.key):
                        x ,y = y, x
                self.HeapLink(y,x)
                A[d]=None
                d+=1
            A[d]=x
        #add new roots and update MIN
        for node in A:
            if node:
                if self.min ==None:
                    self.min = node
                else:
                    self.AddToRoots(node)
            
    def HeapLink(self, y, x):
        self.RemoveFromRoots(y)
        y.parent=x
        if x.child==None:
            y.left=y.right=y
            x.child=y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right = y
            y.right.left = y
        x.degree+=1
        
    def FindMin(self): 
        if not self.isEmpty():
            return self.min.key
        else:
            return self.min
        
    def FindSecond(self):
        first=self.ExtractMin()
        second=self.FindMin()
        self.Insert(first)
        return second
    
    def ExtractSecond(self): 
        first=self.ExtractMin()
        second=self.ExtractMin()
        self.Insert(first)
        return second
    
    def Merge(self, PQ2): 
        #złożoność stała, bo zmieniam tylko dołączenia w liście korzeni 
        #dla 3ch węzłów i aktualizuję min (jedno porównanie)
        if self.min==None: 
            self.min=PQ2.min
        elif PQ2.min!=None:
            
            #merge PQ2's root list roots of self
            PQ1_min_right=self.min.right 
            PQ2_min_left=PQ2.min.left
            self.min.right = PQ2.min
            PQ2.min.left = self.min
            PQ1_min_right.left=PQ2_min_left
            PQ2_min_left.right=PQ1_min_right

            #update MIN 
            if self.cmp(PQ2.min.key, self.min.key):
                self.min = PQ2.min
            self.n += PQ2.n

def test():
        R = [0,1,2,4,7,8,423,67,8,4,2,46]
        shuffle(R)
        Q=PQueue(R)
        assert Q.FindMin()==0, "Fails to find min: should be 0"
        assert Q.FindSecond()==1, "Fails to find 2nd min: should be 1"
        res=Q.ExtractMin()
        assert res==0, "Fails to extract min: should be 0"
        assert Q.FindMin()==1, "Fails to find min after extraction: should be 1"
        assert Q.FindSecond()==2, "Fails to find 2nd min after extraction: should be 2"
        
        #Merge tests 
        S = [2,5,7,3,76]
        shuffle(S)
        Q.Merge(PQueue(S))
        assert Q.FindMin()==1, "Fails to find min: should be 1"
        assert Q.FindSecond()==2, "Fails to find 2nd min: should be 2"
        out=[1, 2, 2, 2, 3, 4, 4, 5, 7, 7, 8, 8, 46, 67, 76, 423]
        L=[Q.ExtractMin() for i in range(Q.n)]
        assert L==out, "Fails to merge!"
       
        #Different CMP test
        Q2=PQueue(L, cmp=lambda x,y: x>y)
        assert Q2.FindMin()==423, \
        "Fails to find min with different CMP function: should be 423"
        print("OK!")

    
if __name__ == "__main__":
    test()