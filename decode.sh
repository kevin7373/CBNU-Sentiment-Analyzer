#!/bin/bash

MODEL=model/single.ckpt
EMBEDDING=wordvector/hani_AllSG200_7_50.txt
DATA=input_pre/CoNLL_csa.CoNLL
RESULT=input_pre/model_csa.txt

GPU_NUM=0




CUDA_VISIVLE_DIVICES=$GPU_NUM python decode_main.py --gpu /gpu:$GPU_NUM --inputData $DATA \
					 --embedding $EMBEDDING --result $RESULT --model $MODEL
