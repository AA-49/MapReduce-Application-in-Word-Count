#!/usr/bin/env python3
"""
reducer.py - Custom Hadoop Streaming Reducer for Task 2 Chained Pipeline
Course: COS20028 Big Data Architecture and Application
Assignment 1: MapReduce Application in Word Count

Input: Sorted key-value stream emitted by mapper.py
       Format per line: <clean_word>\t<count>
Output: Emits aggregated totals: <clean_word>\t<total_count>
"""

import sys

def main():
    current_word = None
    current_count = 0

    # Read each line from standard input passed after Hadoop Shuffle & Sort
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # Split key and value on the tab character
        parts = line.split('\t')
        if len(parts) != 2:
            continue

        word, count_str = parts

        # Verify that count is numeric using Python's native .isdigit() method
        if not count_str.isdigit():
            continue

        count = int(count_str)

        # If current line has the same word, accumulate the count
        if current_word == word:
            current_count += count
        else:
            # When word changes, emit the previous word's aggregated count
            if current_word is not None:
                print("{}\t{}".format(current_word, current_count))
            current_word = word
            current_count = count

    # Emit the last word if exists
    if current_word is not None:
        print("{}\t{}".format(current_word, current_count))

if __name__ == "__main__":
    main()
