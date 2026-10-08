#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mapper2.py

Place this file here:
/Users/yuzhang/projects/UCI_Hadoop_Apache_Airflow/Assignments/Codebook/mapper2.py
"""

import sys
import io
import re

try:
    import nltk
    nltk.download("stopwords", quiet=True)
    from nltk.corpus import stopwords
    STOP_WORDS = set(stopwords.words("english"))
except Exception:
    # Fallback stopword list if nltk is not installed or cannot download data.
    STOP_WORDS = {
        "a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
        "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
        "to", "was", "were", "will", "with"
    }

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding="latin1")

for line in input_stream:
    line = line.strip().lower()
    line = re.sub(r"[^\w\s]", " ", line)
    words = line.split()

    for word in words:
        if word and word not in STOP_WORDS:
            print(f"{word}\t1")
