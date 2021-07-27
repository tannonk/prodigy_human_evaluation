#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
from collections import Counter
import pandas as pd

def iter_lines(file):
    with open(file, 'r', encoding='utf8') as f:
        for line in f:
            yield json.loads(line.strip())

def main(annotation_file):

    df = pd.DataFrame([line for line in iter_lines(annotation_file)])
    breakpoint()


if __name__ == '__main__':
    annotation_jsonl_file = sys.argv[1] #'annotated.jsonl'
    main(annotation_jsonl_file)


# draws = Counter()
# draws = Counter()
# for task in iter_lines(annotation_file):
#     result = None
#     # src_text = task['src_text']
#     score = float(task['score'])
#     answer = task['answer']
#     if -10 < score < 10:
#         result = f"{task['options']['a']['id']} == {task['options']['b']['id']}"
#     elif score < 0:
#         result = f"{task['options']['a']['id']} > {task['options']['b']['id']}"
#     elif score > 0:
#         result = f"{task['options']['b']['id']} > {task['options']['a']['id']}"

#     print(answer, result)

