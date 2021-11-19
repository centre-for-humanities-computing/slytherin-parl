#!/usr/bin/env bash

# input vars
VENVNAME=deadlypoison
TRAIN=false

# test environment
if [ -d $VENVNAME ] 
then
    echo "[INFO] activate: $VENVNAME"
    source deadlypoison/bin/activate
else
    echo "[INFO] build: $VENVNAME"
    #bash create_venv.sh
    #source sickern/bin/activate
    #python -m spacy download da_core_news_sm
    #python -m nltk.downloader punkt
    #echo "[INFO] activate: $VENVNAME"
fi
# meta data model
python src/subject_profiler.py
python src/signal_extractor.py
python src/signal_viz.py