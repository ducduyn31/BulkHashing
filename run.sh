#!/bin/bash

for v in 0 .. 10;
do
  python bulkhash.py -e jpg -i /home/duy/dataset/coco/train2017 -o result -b $v
done

for v in 0 .. 10;
do
  python bulkhash.py -e mp3 -i /home/duy/dataset/cv_corpus_v1/cv-valid-train -o result -b $v
done

for v in 0 .. 10;
do
  python bulkhash.py -e txt -i /home/duy/Projects/GoogleScrapingBot/txt -o result -b $v
done

for v in 0 .. 10;
do
  python bulkhash.py -e pdf -i /home/duy/Projects/GoogleScrapingBot/pdf -o result -b $v
done

for v in 0 .. 10;
do
  python bulkhash.py -e xml -i /home/duy/Projects/GoogleScrapingBot/xml -o result -b $v
done