#!/bin/bash

#Track Reconstruction Workflow

#am -> amount of tracks to be reconstructed

user_dir=`echo ~`
dir="$user_dir"/input_files_for_track

if [ -d $dir ] ; then

am=1000

#obtain a subset of tracks to be reconstructed
head -n $am /data/trackMLDB/analysis/pt1p0_train_2_realv3 > ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname`

#create a file with all hits to be reconstructed
~/git/track-ml-1/input-for-lstm-inf.sh ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname` ~/input_files_for_track/train_2_"$am"_inferences_`hostname`

# reconstruct tracks
#echo python ~/git/track-ml-1/lstm-map-demo-div-v2-inf.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am" ~/input_files_for_track/train_2_"$am"_inferences ~/input_files_for_track/model.h5 ~/input_files_for_track/reconstructed_track.csv
python ~/git/track-ml-1/lstm-map-demo-div-v2-inf.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname` ~/input_files_for_track/train_2_"$am"_inferences_`hostname` ~/input_files_for_track/model_`hostname`.h5 ~/input_files_for_track/reconstructed_track_LSTM_`hostname`.csv 0
python ~/git/track-ml-1/lstm-map-demo-div-v2-inf.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname` ~/input_files_for_track/train_2_"$am"_inferences_`hostname` ~/input_files_for_track/model_`hostname`.h5 ~/input_files_for_track/reconstructed_track_RANDOM_`hostname`.csv 1

#echo python ~/git/track-ml-1/lstm-map-Evaluate.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am" ~/input_files_for_track/reconstructed_track.csv
python ~/git/track-ml-1/lstm-map-Evaluate.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname` ~/input_files_for_track/reconstructed_track_LSTM_`hostname`.csv ~/input_files_for_track/outputhist_LSTM_`hostname`.png
python ~/git/track-ml-1/lstm-map-Evaluate.py ~/input_files_for_track/pt1p0_train_2_realv3_"$am"_`hostname` ~/input_files_for_track/reconstructed_track_RANDOM_`hostname`.csv ~/input_files_for_track/outputhist_RANDOM_`hostname`.png

else
    echo "Error: Directory ~/input_files_for_track does not exists."
fi
