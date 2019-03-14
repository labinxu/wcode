import numpy as np
import os
# shape  reshape
# arange  ndim nbytes [:2,:2]
import copy
#[].copy()
# concatenate([x,y],axis=0 or 1)
#np.vstack([],[])
#np.zeros(3, dtype=int)
#np.zeros(4,dtype={'names':('name','age','weight'),'formats':('U10','i4','f8')})
name=['a','b']
age = [1,2,3]
weight= [4,5,6]
data = np.zeros(3,dtype = {"names":('name','age','weight'),'formats':('U10','i4','f8')})
data['name']=name
data['age'] = age
data['weight'] = weight
