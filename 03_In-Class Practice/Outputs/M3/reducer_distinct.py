#!/usr/bin/env python3
import sys

previous = None

for line in sys.stdin:
    word = line.strip()
    if not word:
        continue
    if word != previous:
        print(word)
        previous = word
