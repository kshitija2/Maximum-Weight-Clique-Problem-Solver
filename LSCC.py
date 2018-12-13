
# coding: utf-8

# In[1]:


#This program implements LSCC algorithm.

import time
import copy
from random import *
import random

# Following section opens the instance file and read from it information about nodes and edges.

file = open('C:/Users/krta225/Downloads/ia-fb-messages.mtx', 'r') 
edgeList=[]
nodes=0
edges=0
for line in file:
    a=line.split()
    if len(a)==2:
        edgeList.append([int(a[0]),int(a[1])])
    if len(a)==3:
        nodes=int(a[0])
        edges=int(a[2])
print('Number of nodes:',str(nodes))
print('Number of edges',str(edges))

# As instances initially do not have weights associated with nodes. Authors calculate weights in following way 
#by taking mod 200 of the number of that node and add 1 to it
weights={}
for i in range(1,nodes+1):
    v=i%200+1
    weights.update({i:v})
    
#This dictionary stores age of nodes i.e.the number of steps since it was selected or not
age={}
for i in range(1,nodes+1):
    age.update({i:0})


cOptimal=[]

sumWeights=0    
startTime = time.time()
elapsedTime=0
cutoff=1000

while elapsedTime<cutoff:
    cOptimalWeight=0

    if len(cOptimal)>0:
        for key, value in weights.items():
            if key in cOptimal:
                cOptimalWeight=cOptimalWeight+value

    elapsedTime=elapsedTime+1
    confChange={}
    for i in range(1,nodes+1):
        confChange.update({i:1})

    w=[]
    for f in range(1,nodes+1):
        w.append(f)
    maxC=0
    c=[]
# This section greedily finds the clique with maximum weight

    for s in range(7):
        r=random.choice(w)
        while(weights.get(r)<50):
            r=random.choice(w)
        w.remove(r)
        cLocal=[r]
        while(1):
            flag=0
            for i in range(1,nodes+1):
                count=0
                for each in cLocal:
                    if [i,each] in edgeList or [each,i] in edgeList:
                        count=count+1
                if count==len(cLocal):
                    cLocal.append(i)
                    flag=1
            if flag==0:
                break

        CsumWeights=0
        for each in cLocal:
            CsumWeights=CsumWeights+weights.get(each)
        
        if CsumWeights>=maxC:
            maxC=CsumWeights
            c=cLocal
            


    cLocalBest=copy.deepcopy(c)

    sumWeights=0
    for each in cLocalBest:
        sumWeights=sumWeights+weights.get(each)

 # This section tries to find solution by using SCC strategy

    for i in range(10):

        addSet=[]
        swapSet=[]
        dropSet=[]

        for i in range (1,nodes+1):
            count=0
            for each in cLocalBest:
                if [i,each] in edgeList or [each,i] in edgeList:
                    count=count+1
            if count==len(cLocalBest):
                if i not in cLocalBest:
                    if i not in addSet:
                        addSet.append(i)
                        v=age.get(i)+1
                        age[i]=v

        maxAddSet=0
        maxNeighbour=0

        if addSet:
            for each in addSet:
                if weights.get(each)>maxAddSet and confChange.get(each)==1:
                    maxAddSet=weights.get(each)
                    maxNeighbour=each
                elif confChange.get(each)==0:
                    addSet.remove(each)
                
        dropSet=copy.deepcopy(cLocalBest)
        for each in cLocalBest:
            v=age.get(each)+1
            age[each]=v


        minDropSet=100000
        minNode=0

        if dropSet:
            for each in dropSet:
                if weights.get(each) < minDropSet:
                    minDropSet=weights.get(each)
                    minNode=each

        for each in cLocalBest:
            for i in range (1,nodes+1):
                count=0
                for each1 in cLocalBest:
                    if each1!=each:
                        if [i,each1] in edgeList or [each1,i] in edgeList:
                            count=count+1
                if count==(len(cLocalBest)-1):
                    if i not in cLocalBest:
                        if[each,i] not in swapSet:
                            swapSet.append([each,i])
                            v=age.get(i)+1
                            age[i]=v

        maxSwapSet=-100
        swapPair=[0,0]
        if swapSet:
            for each in swapSet:
                flag=0
                a=0
                b=0
                a=weights.get(each[0])
                b=weights.get(each[1])
                if confChange.get(each[1])==1:
                    d=b-a
                    if d > maxSwapSet:
                        maxSwapSet=d
                        swapPair=[each[0],each[1]]


        if len(addSet)!=0:
            x=sumWeights+maxAddSet
            y=sumWeights-swapPair[0]+swapPair[1]
            if x>=y:
                if maxNeighbour not in cLocalBest:
                    cLocalBest.append(maxNeighbour)
                    addSet.remove(maxNeighbour)
                    v=age.get(maxNeighbour)+1
                    age[maxNeighbour]=v

                    for i in range(1,nodes+1):
                        if [maxNeighbour,i] in edgeList or [i,maxNeighbour] in edgeList:
                            confChange[i]=1
            else:
                if swapPair[1] not in cLocalBest:
                    cLocalBest.append(swapPair[1])
                    v=age.get(swapPair[1])+1
                    age[swapPair[1]]=v
                    cLocalBest.remove(swapPair[0])
                    confChange[swapPair[0]]=0
                    swapSet.remove(swapPair)
                    for i in range(1,nodes+1):
                        if [swapPair[1],i] in edgeList or [i,swapPair[1]] in edgeList:
                            confChange[i]=1

        else:
            x=sumWeights-minDropSet
            y=sumWeights-swapPair[0]+swapPair[1]
            if swapPair!=[0,0]:
                if x>y:
                    if minDropSet in cLocalBest:
                        cLocalBest.remove(minDropSet)
                        dropSet.remove(minDropSet)
                        confChange[minDropSet]=0
                        
                else:
                    if swapPair[1] not in cLocalBest:
                        cLocalBest.append(swapPair[1])
                        v=age.get(swapPair[1])+1
                        age[swapPair[1]]=v

                        cLocalBest.remove(swapPair[0])
                        swapSet.remove(swapPair)
                        confChange[swapPair[0]]=0
                        for i in range(1,nodes+1):
                            if [swapPair[1],i] in edgeList or [i,swapPair[1]] in edgeList:
                                confChange[i]=1
                        
            elif swapPair==[0,0]:
                if minDropSet in cLocalBest:
                    cLocalBest.remove(minDropSet)
                    dropSet.remove(minDropSet)
                    confChange[minDropSet]=0


        sumWeights=0
        for each in cLocalBest:
            sumWeights=sumWeights+weights.get(each)
            

        if CsumWeights>sumWeights:
            cLocalBest=c
            
        sumWeights=0
        for each in cLocalBest:
            sumWeights=sumWeights+weights.get(each)

            
    if sumWeights>cOptimalWeight:
        cOptimal=cLocalBest
    e=0
    for each in cOptimal:
        e=e+weights.get(each)
    print('Maximum weight found so far: ',str(e))

    endTime = time.time()
    elapsedTime=endTime-startTime
    print('Elapsed Time: ',str(elapsedTime))

        
print('Final maximum weight found: ',str(cOptimal))                        
print('end')

