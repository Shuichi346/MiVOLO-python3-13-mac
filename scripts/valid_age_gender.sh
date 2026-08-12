#!/usr/bin/env bash

# inference utk
uv run python eval_pretrained.py \
  --dataset_images data/utk/images \
  --dataset_annotations data/utk/annotation \
  --dataset_name utk \
  --batch-size 512 \
  --checkpoint pretrained/model_imdb_cross_person_4.24_99.46.pth.tar \
  --split valid \
  --with-persons \
  --device "auto"

# inference fairface
uv run python eval_pretrained.py \
  --dataset_images data/FairFace/fairface-img-margin125-trainval \
  --dataset_annotations data/FairFace/annotations \
  --dataset_name fairface \
  --batch-size 512 \
  --checkpoint pretrained/model_imdb_cross_person_4.24_99.46.pth.tar \
  --split val \
  --with-persons \
  --device "auto"

# inference adience
uv run python eval_pretrained.py \
  --dataset_images data/adience/faces \
  --dataset_annotations data/adience/annotations \
  --dataset_name adience \
  --batch-size 512 \
  --checkpoint pretrained/model_imdb_cross_person_4.24_99.46.pth.tar \
  --split adience \
  --with-persons \
  --device "auto"

# inference agedb
uv run python eval_pretrained.py \
  --dataset_images data/agedb/AgeDB \
  --dataset_annotations data/agedb/annotation \
  --dataset_name agedb \
  --batch-size 512 \
  --checkpoint pretrained/model_imdb_cross_person_4.24_99.46.pth.tar \
  --split 0,1,2,3,4,5,6,7,8,9 \
  --device "auto"
