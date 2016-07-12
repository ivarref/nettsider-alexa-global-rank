#!/bin/bash

set -ex

rm *.sqlite

./log_changes.py | tail -n1 >> country_rank.tsv
git add country_rank.tsv
git commit -m "update"
git push

