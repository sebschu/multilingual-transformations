#SBATCH --gres=gpu:1
#!/bin/bash

#SBATCH --job-name=MT-base-finetune
#SBATCH --nodes=1 
#SBATCH --cpus-per-task=1 
#SBATCH --mem=20GB 
#SBATCH --time=10:00:00 



conda activate py38

python ../models/run_seq2seq.py \
    --model_name_or_path 'google/mt5-base' \
    --do_train \--gres=gpu:1

    --do_eval \
    --task translation_src_to_tgt \
    --train_file ../data/mccoy2020/question_main.train.json \
    --validation_file ../data/mccoy2020/question_main.dev.json \
    --output_dir $SCRATCH/mt5-mccoy-finetuning/	 \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --overwrite_output_dir \
    --predict_with_generate