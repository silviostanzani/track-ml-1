from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import concatenate,Input,Flatten
from keras.models import Model
from keras.models import load_model

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from random import seed
from random import randint

from numpy import array
import numpy as np

from math import sqrt

import sys
import os
import ntpath

import scipy.stats

import seaborn as sns

import pandas as pd

from pandas.plotting import register_matplotlib_converters

import datetime

import matplotlib.pyplot as plt
register_matplotlib_converters()

def plot_results_inferences(df22):
    sns.distplot(df22[0], color="blue") #, ax=axes[0,0], axlabel='X-original')
    #plt.show()

#def position_3D_approximation(y, result):
def position_3D_approximation(result):
    # result => predicted
    #yclone = np.copy(y)
    #dfyclone = pd.DataFrame.from_records(yclone)

    global dfyclone

    df3d = pd.DataFrame({'X':result[:,0],'Y':result[:,1],'Z':result[:,2]})

    df3d['X-pred'] = 0
    df3d['Y-pred'] = 0
    df3d['Z-pred'] = 0
    df3d['ch0'] = 0
    df3d['ch1'] = 0
    df3d['w'] = 0

    dfyclone = pd.DataFrame.from_records(yclone)

    #print(datetime.datetime.now())

    for index, row in df3d.iterrows():
        #print("1",datetime.datetime.now())
        #print("index ", index)
        #obtain the row with least geometric distance between predicted row and original rows (in yclone)
        Xpred=df3d.loc[index, 'X']
        Ypred=df3d.loc[index, 'Y']
        Zpred=df3d.loc[index, 'Z']
        #print("2",datetime.datetime.now())

        #dfyclone = pd.DataFrame.from_records(yclone)
        #dfyclone = pd.DataFrame.from_records(yclone)
        #print("shape: " , dfyclone.shape)

        dfyclone['geodist'] = ( ((dfyclone[0] - Xpred) **2) + ((dfyclone[1] - Ypred) **2)   + ((dfyclone[2] - Zpred) **2) )
        #print("3",datetime.datetime.now())


        row=dfyclone.loc[dfyclone['geodist'].idxmin()]
        #print("4",datetime.datetime.now())

        lowerGeodistIndex=row.name

        X=yclone[lowerGeodistIndex,0]
        Y=yclone[lowerGeodistIndex,1]
        Z=yclone[lowerGeodistIndex,2]
        ch0=yclone[lowerGeodistIndex,3]
        ch1=yclone[lowerGeodistIndex,4]
        #print("5",datetime.datetime.now())

        df3d.loc[index, 'X-pred'] = X
        df3d.loc[index, 'Y-pred'] = Y
        df3d.loc[index, 'Z-pred'] = Z
        df3d.loc[index, 'ch0'] = ch0
        df3d.loc[index, 'ch1'] = ch1
        #print("6",datetime.datetime.now())

        #remove the hit used as approximation
        dfyclone.drop(dfyclone.index[lowerGeodistIndex])
        #yclone = np.delete(yclone, lowerGeodistIndex, axis=0)
        #print("7",datetime.datetime.now())

    #print(datetime.datetime.now())

    #print("j ")
    df3d.drop('X', axis=1, inplace=True)
    df3d.drop('Y', axis=1, inplace=True)
    df3d.drop('Z', axis=1, inplace=True)

    #return the fourth hit of all tracks
    return(df3d)

seed(1)

#Read input file with first 3 hits to dataframe
event_prefix = sys.argv[1]
event_file_name=ntpath.basename(event_prefix)
event_prefix2 = sys.argv[2]

df = pd.read_csv(event_prefix)
df_all_hits = pd.read_csv(event_prefix2)
#dataframe with original values for evaluation
#dfeval = pd.read_csv(event_prefix)

#all tracks have at maximum 29 hits
hits = np.arange(0,29,1)

#print (hits)
firstHit=1
lastHit=4

#print ("begin")
df1 = df.iloc[:,1:25]
#print("!!-print(df1.shape) : ",df1.shape)

y=df_all_hits.iloc[:, [ 25,26,27,28,29 ]]

yclone = np.copy(y)
dfyclone = pd.DataFrame.from_records(yclone)

#for firstHit in range(1, 24):
for firstHit in range(1, 26):
#for firstHit in range(1, 2):
    #print("firstHit : ", firstHit)
    lastHit = lastHit + 1
    #begin with 3 know hits
    known_hits= np.arange(firstHit,lastHit,1)
    #next hit to predict
    hit_to_predict=known_hits[3]
    '''
    print(known_hits)
    print(hit_to_predict)
    print("print(df1.shape) : ",df1.shape)
    print ("X")
    print ( (hits[known_hits[0]]*6)+1,(hits[known_hits[0]]*6)+2,(hits[known_hits[0]]*6)+3 , (hits[known_hits[1]]*6)+1,(hits[known_hits[1]]*6)+2,(hits[known_hits[1]]*6)+3 , (hits[known_hits[2]]*6)+1,(hits[known_hits[2]]*6)+2,(hits[known_hits[2]]*6)+3)
    print ("Xfeat")
    print ( (hits[known_hits[0]]*6)+4,(hits[known_hits[0]]*6)+5 , (hits[known_hits[1]]*6)+4 , (hits[known_hits[1]]*6)+5  , (hits[known_hits[2]]*6)+4 , (hits[known_hits[2]]*6)+5)
    print ("Y")
    print ( (hits[hit_to_predict]*6)+1,(hits[hit_to_predict]*6)+2,(hits[hit_to_predict]*6)+3,(hits[hit_to_predict]*6)+4,(hits[hit_to_predict]*6)+5 )
    '''

    #cpton=((hits[known_hits[2]]*6)+5)+1
    #print("cpton ",cpton)
    #print((hits[known_hits[0]]*6)+1,(hits[known_hits[0]]*6)+2,(hits[known_hits[0]]*6)+3 , (hits[known_hits[1]]*6)+1,(hits[known_hits[1]]*6)+2,(hits[known_hits[1]]*6)+3 , (hits[known_hits[2]]*6)+1,(hits[known_hits[2]]*6)+2,(hits[known_hits[2]]*6)+3)
    #print((hits[known_hits[0]]*6)+4,(hits[known_hits[0]]*6)+5 , (hits[known_hits[1]]*6)+4 , (hits[known_hits[1]]*6)+5  , (hits[known_hits[2]]*6)+4 , (hits[known_hits[2]]*6)+5)

    dataX2=df1.iloc[:, [ (hits[known_hits[0]]*6)+1,(hits[known_hits[0]]*6)+2,(hits[known_hits[0]]*6)+3 , (hits[known_hits[1]]*6)+1,(hits[known_hits[1]]*6)+2,(hits[known_hits[1]]*6)+3 , (hits[known_hits[2]]*6)+1,(hits[known_hits[2]]*6)+2,(hits[known_hits[2]]*6)+3 ]]
    dataXfeatures=df1.iloc[:, [  (hits[known_hits[0]]*6)+4,(hits[known_hits[0]]*6)+5 , (hits[known_hits[1]]*6)+4 , (hits[known_hits[1]]*6)+5  , (hits[known_hits[2]]*6)+4 , (hits[known_hits[2]]*6)+5  ]]#dataXfeatures=df.iloc[:, [  hits[known_hits[0]]+4,hits[known_hits[0]]+5,hits[known_hits[0]]+6 , hits[known_hits[1]]+4,hits[known_hits[1]]+5,hits[known_hits[1]]+6 , hits[known_hits[2]]+4,hits[known_hits[2]]+5,hits[known_hits[2]]+6  ]]

    #prepare data to inference
    b = dataX2.values.flatten()
    bfeat=dataXfeatures.values.flatten()
    n_patterns=len(df)
    X     = np.reshape(b,(n_patterns,3,3))
    Xfeat = np.reshape(bfeat,(n_patterns,3,2))
    #Xfeat = np.reshape(b,(n_patterns,3,3))

    #original hit that will be predicted
    #yaux=df22.iloc[:, [ (hits[hit_to_predict]*6)+1,(hits[hit_to_predict]*6)+2,(hits[hit_to_predict]*6)+3,(hits[hit_to_predict]*6)+4,(hits[hit_to_predict]*6)+5 ]]
    #y=df.iloc[:, 25,26,27,28,29 ]]

    #perform the prediction
    model = load_model('/home/silvio/model.h5')

    result = model.predict([X, Xfeat],verbose=1)
    #print("position 3d")
    #pred = position_3D_approximation(y, result)
    pred = position_3D_approximation(result)
    #print("position 3d 2")
    #concat tracks with predicted positions
    df1= pd.concat([df1,pred],axis=1) #, keys=['One','Two'])

df1.to_csv('reconstructed_track.csv')


'''
    # evaluation
    dfglobal_original = np.hstack((dataX2,yaux))
    dfglobal_predicted = np.hstack((dataX2,pred))

    dftot = pd.DataFrame.from_records(dfglobal_predicted)
    dftot2 = pd.DataFrame.from_records(dfglobal_original)

    #print(dftot)
    #print(dftot2)

    dftotfinal = pd.DataFrame( abs(((dftot[9] - dftot2[9]) **2) + ((dftot[10] - dftot2[10]) **2)   + ((dftot[11] - dftot2[11]) **2)) )

    seriesObj = dftotfinal.apply(lambda x: True if x[0] == 0 else False , axis=1)
    numOfRows = len(seriesObj[seriesObj == True].index)
    print('equal 0 : ', numOfRows)

    maxV=dftotfinal[0].max()
    minV=dftotfinal[0].min()

    if ((maxV == 0) and (minV == 0)):
        print('max : ' , maxV )
        print('min : ' , minV )
    else:
        print('mean geodist from original values : ' , dftotfinal[0].mean())
        print('max : ' , maxV )
        print('min : ' , minV )
        #print('equal 0: ', dftotfinal[dftotfinal[0] == 0].sum()  )

    plot_results_inferences(dftotfinal)
'''

'''
    print('===========================================')
    print('X')
    print(X)
    print('===========================================')
    print('Xfeat')
    print(Xfeat)
    print('===========================================')
    print('y')
    print(y)
    print('===========================================')
'''

'''
    print('===========================================')
    print('dfglobal_original')
    print(dfglobal_original)
    print('===========================================')
    print('dfglobal_predicted')
    print(dfglobal_predicted)
    print('===========================================')
'''

    #dftotfinal['Xdiff'] = pd.DataFrame(abs(dftot[9]) - abs(dftot2[9])) + (abs(dftot[10]) - abs(dftot2[10])) + (abs(dftot[11]) - abs(dftot2[11]))
    #dftotfinal = pd.DataFrame( (abs((dftot[9] - dftot2[9]))) + (abs((dftot[10] - dftot2[10]))) + (abs(dftot[11]) - abs(dftot2[11])) )
    #df22=dftotfinal.sort_values(by='Xdiff')
    #print(dftotfinal)
    #print('sum : ' , dftotfinal[0].sum() )
    #print('max : ' , dftotfinal[0].max() )
    #print('min : ' , dftotfinal[0].min() )
    #print('shape : ' , dftotfinal.shape[0] )
    #ss=dftotfinal[0].sum()
    #sh=dftotfinal.shape[0]
    #av=ss/sh
    #print('av : ' , av )
