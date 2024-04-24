'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file contains abstraction layer for interacting with LLM
You can customize the file for querying into your custom LLM
'''

from openai import OpenAI
import prompts

class LLM():
    # Chat history
    chat_history = []

    '''
    LLM object, an abstraction layer for interacting with LLM
    Args:
        api_key (str): API key.
        model (str): (optional) LLM name. Default is gpt-3.5-turbo
        endpoint (str): (optional) OpenAI-compatible API endpoint. Default is OpenAI's default endpoint.
    '''
    def __init__(self, api_key: str, model='gpt-3.5-turbo', endpoint=None):
        self.model = model
        
        # Create OpenAI client object
        self.client = OpenAI(api_key = api_key, base_url=endpoint)

        # Reset history
        self.reset_history()
    
    '''
    Add message to chat history
    Args:
        role (str): owner of the message
        content (str): content's message
    '''
    def add_message(self, role: str, content: str):
        self.chat_history.append({'role': role, 'content': content})
    
    '''
    Reset the chat history
    Actually replace it with the InitialChatHistory
    '''
    def reset_history(self):
        self.chat_history = prompts.InitialChatHistory
    
    '''
    Get base response from LLM
    This function just feed the chat history into LLM, but not actually parsing anything
    Return:
        (str) Response from LLM
    '''
    def get_base_response(self):
        reply = self.client.chat.completions.create(model=self.model, messages=self.chat_history).choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": reply})
        return reply
    
    '''
    Parse specific section in response
    Args:
        res (str): response string to be parsed
        start_separator (str): start separator of the section
        alternative_start (str): alternative separator of the section. Usually the end separator of the last section. Can use empty string if current section is the first section.
        end_separator (str): end separator of the section
        alternative_end (str): alternative separator of the section. Usually the start separator of the next section. Can use empty string if current section is the last section.
    Return:
        (str/Nonetype): Parsed result. If none found, return None
    '''
    def parse_response_section(self, res: str, start_separator: str, alternative_start: str, end_separator: str, alternative_end: str):
        # Check if none of primary tags exist
        if (not start_separator in res) and (not end_separator in res):
            return None
        
        # Take start tag as separator if it exist, else use alternative one if possible
        if (not start_separator in res) and (alternative_start != ""):
            start_separator = alternative_start
        
        # Parse first part
        first_parse = res.split(start_separator)[-1]

        # Take end tag as separator if it exist, else use alternative one
        if (not end_separator in res) and (alternative_end != ""):
            end_separator = alternative_end

        # Parse last part and return
        return first_parse.split(end_separator)[0]
    
    '''
    Parse response
    Args:
        res (str): response string to be parsed
    Return:
        (whoosh: str, summary: str, response: str) Phrased result from LLM response. If any of these sections does not
        found, it will be None
    '''
    def parse_response(self, res):
        # Parse whoosh string
        whoosh_r = self.parse_response_section(res, prompts.WhooshSepStart, "", prompts.WhooshSepEnd, prompts.SummarySepStart)
        
        # Parse summary string
        summary_r = self.parse_response_section(res, prompts.SummarySepStart, prompts.WhooshSepEnd, prompts.SummarySepEnd, prompts.ResponseSepStart)
    
        # Parse user response string
        user_r = self.parse_response_section(res, prompts.ResponseSepStart, prompts.SummarySepEnd, prompts.ResponseSepEnd, "")

        return (whoosh_r, summary_r, user_r)
    
    '''
    Feed user prompt into LLM
    Args:
        p (str): user prompt
    '''
    def add_user_prompt(self, p):
        self.add_message("user", prompts.PromptBeforeUserPayload + prompts.UserSepStart + p + prompts.UserSepEnd)
    
    '''
    Feed whoosh output into LLM
    Args:
        res (str): whoosh output
    '''
    def add_whoosh_output(self, res):
        self.add_message("user", prompts.PromptBeforeWhooshResponse + prompts.WhooshOutputStart + res + prompts.WhooshOutputEnd)
