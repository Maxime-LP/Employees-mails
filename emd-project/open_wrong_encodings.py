#!/usr/bin/env python3
import re
from time import time

fp0 = '/home/amait/Documents/Employees-mails/emd-project/wrong_encodings.txt'
with open(fp0, 'r') as paths:
    for fp in paths:
        print(f'fp: {fp}')
        with open(fp[:-1], 'r', encoding='iso-8859-1') as file:
            for line in file:
                pass