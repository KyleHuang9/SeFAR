python setup.py build develop
python run_net_emamix.py \
  --cfg configs/TimeSformer_base_ssl.yaml \
  DATA.PATH_TO_DATA_DIR ./dataset/finegym/all99_5 \
  OUTPUT_DIR ./output/finegym_all99_5 \
  NUM_GPUS 1 \
  TRAIN.BATCH_SIZE 3 \
  TEST.BATCH_SIZE 48 \
  TRAIN.ENABLE True \
  TRAIN.FINETUNE False \
  TRAIN.CHECKPOINT_FILE_PATH ./output/checkpoint_epoch_00030.pyth
