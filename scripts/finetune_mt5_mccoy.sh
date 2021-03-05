python ../models/run_seq2seq.py \
    --model_name_or_path mt5-base \
    --do_train \
    --do_eval \
    --task translation_src_to_tgt \
    --train_file ../data/mccoy2020/question_main.train.json \
    --validation_file ../data/mccoy2020/question_main.dev.json \
    --output_dir ../output/ \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --overwrite_output_dir \
    --predict_with_generate