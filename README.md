# track-ml

Output of Prepare_data_to_NN.py is a CSV file 

Each line is a particle and several hits of this particle 

Each line has 174 columns organized in the following way:

  - first 6 columns is particle information: tx, ty, tx, px, py, pz

  - 28 sets of 6 columns representing hits: tx,ty,tz, ch0, ch1, value
  
If the has less than 28 hits the remaings hits is fullfiled with zeros

the last colum 175 has 1 for fake hits and 0 for real hit

In oder to use more than one GPU in the same machine to train a keras model use the following comannd:

```
    multi_gpu_model(<keras_model>, gpus=<amout of GPUs>)
```

Code Sample:

```
classifier = Sequential()
classifier.add(Dense(2400, input_dim=120, activation='relu'))
classifierp = multi_gpu_model(classifier, gpus=2)
classifierp.compile(optimizer ='rmsprop',loss='binary_crossentropy', metrics =['accuracy'])
```

In order to use Python script: Prepare_data_to_NN.py you can setup your conda environment using trackenv.yml

```
conda env create -n trackml4 -f /data/trackenv.yml
```

After create the environment wil you need to install a kaggle track library to manage event files:

```
pip install --user git+https://github.com/LAL/trackml-library.git
```

Executing experiments with LSTM:

train the model:

```
CUDA_VISIBLE_DEVICES="0" python lstm-map-demo-div-v2.py track_real_for_lstm_experiment
```

the file model.h5 with NN model will be created

Evaluate the model:

```
CUDA_VISIBLE_DEVICES="0" python lstm-map-demo-div-v2-inf.py track_real_for_lstm_experiment
```
