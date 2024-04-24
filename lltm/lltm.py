'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file contains code to bridge between LLM and LTM implementation
'''

import llm
import ltm

class LLTM():
    '''
    LLTM object, containing an LLM object with specified memory object

    Args:
        llm (LLM object): instance of LLM object, for interacting with LLM
        ltm (LTM object): instance of LTM object, for interacting with memory
    '''
    def __init__(self, llm, ltm):
        self.llm = llm
        self.ltm = ltm
