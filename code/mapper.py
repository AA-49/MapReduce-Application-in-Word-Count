#!/usr/bin/env python3
"""
mapper.py - Custom Hadoop Streaming Mapper for Task 2 Chained Pipeline
Course: COS20028 Big Data Architecture and Application
Assignment 1: MapReduce Application in Word Count

Input: Intermediate output block (part-r-00000) from Task 1 (Java WordCount)
       Format per line: <raw_token>\t<count>
Output: Emits cleaned key-value pairs: <clean_word>\t<count>
"""

import sys
import re

# Hardcoded comprehensive list of standard English stopwords
STOPWORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and',
    'any', 'are', 'aren\'t', 'as', 'at', 'be', 'because', 'been', 'before', 'being',
    'below', 'between', 'both', 'but', 'by', 'can\'t', 'cannot', 'could', 'couldn\'t',
    'did', 'didn\'t', 'do', 'does', 'doesn\'t', 'doing', 'don\'t', 'down', 'during',
    'each', 'few', 'for', 'from', 'further', 'had', 'hadn\'t', 'has', 'hasn\'t',
    'have', 'haven\'t', 'having', 'he', 'he\'d', 'he\'ll', 'he\'s', 'her', 'here',
    'here\'s', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'how\'s', 'i',
    'i\'d', 'i\'ll', 'i\'m', 'i\'ve', 'if', 'in', 'into', 'is', 'isn\'t', 'it',
    'it\'s', 'its', 'itself', 'let\'s', 'me', 'more', 'most', 'mustn\'t', 'my',
    'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other',
    'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'shan\'t',
    'she', 'she\'d', 'she\'ll', 'she\'s', 'should', 'shouldn\'t', 'so', 'some',
    'such', 'than', 'that', 'that\'s', 'the', 'their', 'theirs', 'them', 'themselves',
    'then', 'there', 'there\'s', 'these', 'they', 'they\'d', 'they\'ll', 'they\'re',
    'they\'ve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up',
    'very', 'was', 'wasn\'t', 'we', 'we\'d', 'we\'ll', 'we\'re', 'we\'ve', 'were',
    'weren\'t', 'what', 'what\'s', 'when', 'when\'s', 'where', 'where\'s', 'which',
    'while', 'who', 'who\'s', 'whom', 'why', 'why\'s', 'with', 'won\'t', 'would',
    'wouldn\'t', 'you', 'you\'d', 'you\'ll', 'you\'re', 'you\'ve', 'your', 'yours',
    'yourself', 'yourselves'
}

def clean_word(token):
    """
    Cleans a raw token by stripping non-alphabetical punctuation and normalizing case.
    Uses .isdigit() validation as specified in the assignment guidelines.
    """
    # Remove leading/trailing non-alphanumeric punctuation
    token = re.sub(r'^[^\w]+|[^\w]+$', '', token)
    
    # Strip common typographical quotes and symbols (e.g., curly quotes, brackets, underscores)
    token = token.replace('’', '').replace("'", '').replace('_', '').replace('"', '')
    
    # Normalize to lower case for case-insensitive counting
    clean_token = token.strip().lower()
    
    # Verification using native .isdigit() method to reject purely numeric entries
    if not clean_token or clean_token.isdigit():
        return None
    
    # Check if the token contains any numerical digits; filter them out if present
    has_digit = False
    for char in clean_token:
        if char.isdigit():
            has_digit = True
            break
    if has_digit:
        return None
        
    return clean_token

def main():
    # Process standard input stream line-by-line (from HDFS block part-r-00000)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        
        # In Task 1 output, lines are formatted as: <token>\t<count>
        # We also handle general whitespace separation
        parts = line.split('\t')
        if len(parts) >= 2:
            raw_token = parts[0]
            count_str = parts[1]
        else:
            # Fallback if space-separated
            tokens = line.split()
            if len(tokens) >= 2 and tokens[-1].isdigit():
                raw_token = ' '.join(tokens[:-1])
                count_str = tokens[-1]
            else:
                raw_token = line
                count_str = "1"
        
        # Verify count is a valid integer string
        if not count_str.isdigit():
            continue
        
        count = int(count_str)
        
        # Perform text data cleansing
        cleaned = clean_word(raw_token)
        
        # Skip empty strings, invalid tokens, or words in the Stopwords list
        if not cleaned or cleaned in STOPWORDS:
            continue
        
        # Emit cleansed key-value pair to standard output
        print("{}\t{}".format(cleaned, count))

if __name__ == "__main__":
    main()
