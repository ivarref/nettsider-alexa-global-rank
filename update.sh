#!/bin/bash

set -ex

git pull

rm -f *.sqlite

./log_changes.py | tail -n1 >> country_rank.tsv
cat country_rank.tsv | head -n1 > latest.tsv
cat country_rank.tsv | tail -n1 >> latest.tsv

git add country_rank.tsv
git add latest.tsv
git commit -m "update"
git push

