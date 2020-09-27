import csv
import re

# https://ayaka.shn.hk/hanregex/
# 〇 本来也是汉字，但有时用作占位符，如 〇还是个孩子，故去掉
han_symbols_regex = re.compile(r'^[\u4e00-\u9fff\u3400-\u4dbf\U00020000-\U0002a6df\U0002a700-\U0002b73f\U0002b740-\U0002b81f\U0002b820-\U0002ceaf\U0002ceb0-\U0002ebef\U00030000-\U0003134f，·：]+$')
def is_han_string(s):
    return bool(han_symbols_regex.match(s))

d1 = []
d2 = []
d3 = []

with open('source.tsv') as f:
    next(f)
    for line in f:
        ci, yin, yi, _, _, gu = line.rstrip('\n').split('\t')
        if not any((ci, yin, yi, gu)):
            continue  # skip empty lines
        (d1 if not is_han_string(ci) else d2 if len(ci) == 1 else d3).append((ci, yin, yi, gu))

d1.sort(key=lambda xyz: (len(xyz[0]), xyz))
d2.sort(key=lambda xyz: (len(xyz[0]), xyz))
d3.sort(key=lambda xyz: (len(xyz[0]), xyz))

with open('lettered.tsv', 'w') as f:
    for ci, yin, yi, gu in d1:
        print(ci, gu, yin, yi, sep='\t', file=f)

with open('char.tsv', 'w') as f:
    for ci, yin, yi, gu in d2:
        print(ci, gu, yin, yi, sep='\t', file=f)

incorrect_set = set('頁涌')

with open('words.tsv', 'w') as f, open('words_certain.tsv', 'w') as g:
    for ci, yin, yi, gu in d3:
        if not gu or '/' in gu or '  ' in gu or any(ch in incorrect_set for ch in ci):  # contains uncertain pronunciations
            print(ci, gu, yin, yi, sep='\t', file=f)
        else:
            print(ci, gu, yin, yi, sep='\t', file=g)
