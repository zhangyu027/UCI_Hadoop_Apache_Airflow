#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reducer.py

Place this file here:
/Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Codebook/reducer.py
"""

import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip().lower()
    if not line:
        continue

    try:
        word, count = line.split("\t", 1)
        count = int(count)
    except ValueError:
        continue

    if current_word == word:
        current_count += count
    else:
        if current_word is not None:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word is not None:
    print(f"{current_word}\t{current_count}")
