'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file contains code to bridge between LLM and LTM implementation
'''

import llm
import ltm

# Other methods in class LLTM will be done later. Now it just includes a REPL for demo.

class LLTM():
    '''
    LLTM object, containing an LLM object with specified memory object

    Args:
        llm (LLM object): instance of LLM object, for interacting with LLM
        ltm (LTM object): instance of LTM object, for interacting with memory
    '''
    def __init__(self, llm_object: llm.LLM, ltm_object: ltm.LTM):
        self.llm = llm_object
        self.ltm = ltm_object

    '''
    Check and add summary to LTM
    Args:
        summary (str): summary from LLM
    '''
    def check_add_summary(self, summary):
        if summary != None:
            # Add private data for now
            self.ltm.add_private_data(summary)
    
    '''
    Check and print LLM response
    Args:
        response (str): response to user from LLM
    '''
    def check_print_response(self, response):
        if response != None:
            print("Bot:", response)

    '''
    Chat REPL
    '''
    def repl(self):
        while True:
            # Get user prompt
            user_prompt = input("User: ")

            # Feed user prompt to LLM
            self.llm.add_user_prompt(user_prompt)

            while True:
                # Get and parse respone
                br = self.llm.get_base_response()
                print(br)
                r = self.llm.parse_response(br)
                #print(r)

                # Process summary and response (if applicable)
                self.check_add_summary(r[1])
                self.check_print_response(r[2])
                
                # If there is whoosh search query -> ask whoosh
                if r[0] != None:
                    whoosh_r = self.ltm.content_search(r[0])
                    self.llm.add_whoosh_output(str(whoosh_r))
                else:
                    # No more work to do, waiting for input
                    break
