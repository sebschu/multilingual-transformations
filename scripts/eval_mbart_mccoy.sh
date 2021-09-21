#!/bin/bash

#SBATCH --job-name=MBart-large-eval-dev-curve
#SBATCH --nodes=1 
#SBATCH --cpus-per-task=1 
#SBATCH --mem=20GB 
#SBATCH --time=10:00:00 
#SBATCH --gres=gpu:v100:1

singularity exec --nv --overlay $SCRATCH/overlay-50G-10M.ext3:ro /scratch/work/public/singularity/cuda10.2-cudnn7-devel-ubuntu18.04-20201207.sif /bin/bash -c "

source /ext3/env.sh
conda activate py38

CUDA_LAUNCH_BLOCKING=1 python ../models/run_seq2seq.py \
    --model_name_or_path /scratch/am12057/mbart-mccoy-have-finetuning/ \
    --do_eval \
	--do_learning_curve \
    --task translation_src_to_tgt \
	--source_lang en_XX \
	--target_lang en_XX \
	--use_fast_tokenizer False \
    --train_file ../data/mccoy2020/question_have.train.json \
	--validation_file ../data/mccoy2020/question_have.de.dev.json \
    --output_dir $SCRATCH/mbart-mccoy-finetuning/	 \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=16 \
    --overwrite_output_dir \
    --predict_with_generate
"
