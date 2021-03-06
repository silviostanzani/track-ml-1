#Cell for testing prediction model
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from keras.models import load_model

#sys.path.append('/home/silvio/git/track-ml-1')
from lib_data_manipulation import *

def dataprep(file):
    #Data preparation

    #load track file
    df = pd.read_csv(file)

    df1 = df.iloc[:,10:54]

    #Separate values and features for LSTM
    dataX2 = df1.iloc[:, [ 0,1,2,8,9,10,16,17,18,24,25,26]]
    dataXfeatures = df1.iloc[:, [ 6,14,22,30 ]]

    b = dataX2.values.flatten()
    bfeat = dataXfeatures.values.flatten()
    n_patterns = len(df)
    X     = np.reshape(b,(n_patterns,4,3))
    Xfeat = np.reshape(bfeat,(n_patterns,4,1))

    XMLP= df1.iloc[:, [ 2,3,4,9,10,11,12,17,18,19,20,24]]

    resorg= df1.iloc[:, [ 32,33,34]]
    resorgfile=diraux+'/resorg'
    resorg.to_csv(resorgfile, index = False)

    #prepare data to be approximated to inference data
    df_all_hits = df1.iloc[:, [ 31,32,33,34,35,36,37,38]]
    yy=df_all_hits.iloc[:,:]
    yclone = np.copy(yy)
    dfyclone = pd.DataFrame.from_records(yclone)

    return X, Xfeat, dfyclone, resorg

def evaluate_results(df3d, df3dapp, resorg):

    Res3file=diraux+'/Res3'
    beforemappingRes3file=diraux+'/beforemappingRes3'

    df3dapp.to_csv(Res3file, index = False)
    df3d.to_csv(beforemappingRes3file, index = False)

    dftemp = pd.DataFrame(index=range(len(resorg)),columns=range(12))
    dftemp[0]=resorg.iloc[:,[0]]
    dftemp[1]=resorg.iloc[:,[1]]
    dftemp[2]=resorg.iloc[:,[2]]

    dftemp[3]=df3d.iloc[:,[0]]
    dftemp[4]=df3d.iloc[:,[1]]
    dftemp[5]=df3d.iloc[:,[2]]

    dftemp[6]=df3dapp.iloc[:,[0]]
    dftemp[7]=df3dapp.iloc[:,[1]]
    dftemp[8]=df3dapp.iloc[:,[2]]

    dftemp[9]=   (((dftemp[0]-dftemp[3])**2)+((dftemp[1]-dftemp[4])**2)+((dftemp[2]-dftemp[5])**2)).pow(1./2)
    dftemp[10]=   (((dftemp[0]-dftemp[6])**2)+((dftemp[1]-dftemp[7])**2)+((dftemp[2]-dftemp[8])**2)).pow(1./2)
    dftemp[11]=   (((dftemp[3]-dftemp[6])**2)+((dftemp[4]-dftemp[7])**2)+((dftemp[5]-dftemp[8])**2)).pow(1./2)

    #print (dftemp.iloc[0:10,:])
    dftemp=dftemp.sort_values(by=[10])
    #print (dftemp)

    print ("average distance prediction" , dftemp[9].mean())
    print ("average distance approximation" , dftemp[10].mean())

    dftemp22 = dftemp[ dftemp[10] == 0]
    print ("0 diff" , dftemp22.shape[0])
    '''
    outputfig=diraux+"/plot-original-predicted.png"
    sns_plot = sns.distplot(dftemp.iloc[:,9:10])
    sns_plot.set(xlabel='Average Distance in MM - original x predicted ', ylabel='Frequency')
    plt.savefig(outputfig)

    outputfig=diraux+"/plot-original-approximated.png"
    sns_plot2 = sns.distplot(dftemp.iloc[:,10:11])
    sns_plot2.set(xlabel='Average Distance in MM - original x approximated ', ylabel='Frequency')
    plt.savefig(outputfig)
    '''
    #predicted
    data = dftemp.iloc[:,9:10]
    # Approximated
    data2 = dftemp.iloc[:,10:11]

    # Create a figure instance, and the two subplots
    fig = plt.figure(figsize=(16, 32))

    ax1 = fig.add_subplot(211)
    ax1.set_title('Predicted')
    ax1.set_xlabel('Error (Milimeter)')

    ax2 = fig.add_subplot(212)
    ax2.set_title('Approximated')
    ax2.set_xlabel('Error (Milimeter)')

    # Predicted
    sns.distplot( data, ax=ax1)
    # Approximated
    sns.distplot(data2, ax=ax2)
    outputfig=diraux+"/Predicted_Approximated.png"
    plt.savefig(outputfig)

def position_3D_approximation(result,dfyclone):
    # result => predicted

    #global dfyclone
    #print(type(dfyclone))
    #this dataframe receives all X,Y,Z predicted considering a set of hists
    df3d = pd.DataFrame({'X':result[:,0],'Y':result[:,1],'Z':result[:,2]})

    df3d['X-pred'] = 0
    df3d['Y-pred'] = 0
    df3d['Z-pred'] = 0
    df3d['hit_id'] = 0
    df3d['volume_id'] = 0
    df3d['layer_id'] = 0
    df3d['module_id'] = 0
    df3d['value'] = 0

    #for each predicted hit, we will approximate to the closest hit considering gemoetric distance
    for index, row in df3d.iterrows():
        #obtain the row with least geometric distance between predicted row and original rows (in yclone)
        Xpred=df3d.loc[index, 'X']
        Ypred=df3d.loc[index, 'Y']
        Zpred=df3d.loc[index, 'Z']

        #in this column we will create the geometric distance from all available hits and the current hit
        dfyclone['geodist'] = ( ((dfyclone[1] - Xpred) **2) + ((dfyclone[2] - Ypred) **2)   + ((dfyclone[3] - Zpred) **2) )

        dfyclone=dfyclone.sort_values(by=['geodist'])

        df3d.loc[index, 'X-pred'] = dfyclone[1].values[0]
        df3d.loc[index, 'Y-pred'] = dfyclone[2].values[0]
        df3d.loc[index, 'Z-pred'] = dfyclone[3].values[0]
        df3d.loc[index, 'hit_id'] = dfyclone[0].values[0]
        df3d.loc[index, 'volume_id'] = dfyclone[4].values[0]
        df3d.loc[index, 'layer_id'] = dfyclone[5].values[0]
        df3d.loc[index, 'module_id'] = dfyclone[6].values[0]
        df3d.loc[index, 'value'] = dfyclone[7].values[0]

        #Apagar da base de predições o registro que já foi associado
        #dfyclone.drop(dfyclone.index[0], inplace=True)

    df3d.drop('X', axis=1, inplace=True)
    df3d.drop('Y', axis=1, inplace=True)
    df3d.drop('Z', axis=1, inplace=True)

    #return the fourth hit of all tracks
    return(df3d)

#setup GPU environment
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)
set_session(sess)

#read parameters
NN  = int(sys.argv[1])
file = sys.argv[2]
h5file = sys.argv[3]
print ("parameters for inference: ",NN,file,h5file)

#Create Auxiliary directory if it does not exists
diraux, filename = os.path.split(h5file)
print("Auxiliary directory: ", diraux)

if (os.path.isdir(diraux) == False):
    os.mkdir(diraux)

#data preparation for inference
X, Xfeat, dfyclone, resorg = dataprep(file)

#Predict next hits
#load model
model = load_model(h5file)

result = model.predict([X, Xfeat],verbose=1)

#Predict X Y Z
df3d = pd.DataFrame({'X':result[:,0],'Y':result[:,1],'Z':result[:,2]})

#Approximate X Y Z to the set of hits
df3dapp=position_3D_approximation(result, dfyclone)

#evaluate results
#Compare Predicted X Y Z and Approximated X Y Z againt real X Y Z
evaluate_results(df3d, df3dapp, resorg)
