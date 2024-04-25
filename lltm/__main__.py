'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file serve as a demo for LLTM
'''

import sys
from llm import LLM
from ltm import LTM
from lltm import LLTM

if __name__ == "__main__":
    llm_o = LLM(sys.argv[1], sys.argv[2], sys.argv[3])
    ltm_o = LTM(sys.argv[4], sys.argv[5])
    lltm_o = LLTM(llm_o, ltm_o)
    lltm_o.repl()
