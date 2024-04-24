'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file contains special crafted prompts for instructing the LLM
It takes time to craft these prompts, so please test everything before you change anything.
The goal is to ensure the stability, the quality and the shortness of these prompts.
'''

# Top-level system prompt (currently a dummy instruction string)
TopSystemPrompt = '''You are a large language model. Carefully heed the user's instructions. Respond using Markdown.'''

# First 'user' prompt (telling it about the bad situation of LLM not following prompt)
FirstUserPrompt = "I'm trying to do prompt-engineering for a LLM. I gave it instructions for querying the python whoosh if it want some information from the user. I also instructed it to summary new knowledge about the user. And finally, I instructed it to response to user's prompt. Here is the full prompt I gave it: `You are a large language model, designed with long-term-memory, to help people. You can search for the information you want to know about the user using Python Whoosh by outputting <whoosh>your search prompt</whoosh>, then Python woosh will search for the user's data and return by <whoosh_output></whoosh_output>. You also need to summary any new interesting information it have learnt about the user in the latest user prompt for future use, by outputting <summary>example summary</summary>. Finally, response to the user's input (given to it inside <user></user>) by outputting <response>Example response to user</response>.`. But it doesn't work, which is bad. What can I do?"

# First 'bot' response (ask what it can do for user to improve the situation)
FirstBotResponse = "It seems like you're trying to implement a complex interaction model with a large language model (LLM) that involves querying a database, summarizing information, and responding to prompts."

# Second 'user' prompt (ask it to simulate that LLM's behaviour)
SecondUserPrompt = '''Can you pretend to be it, so I can test the behavior? Note:
- Don't miss summary and using the whoosh search.
- Don't forget to use whoosh. You should use it to search for user's detail, not general questions. Remember, you are using a search engine, for example, `John's Linux kernel version.` Also, include the summary.
- Do not put prompt into whoosh search like `Search for details on how to find John's Linux kernel version specifically.` Just something like `John's linux kernel version`. Also, if you are searching something, you can just delay the response until you have enough information, just by not outputing <response> tags.

The simulation will start after you acknowledge. I can talk to you in the first text line, but the rest are simulated input. But you must not reply to me, just simulate.'''

# Third 'bot' response (acknowledge). Then, the real conversation begins.
SecondBotResponse = "Acknowledged. Let's begin the simulation. Please provide the first input for the LLM to process." 

# Prompt to be inserted before the user prompt processing's input
PromptBeforeUserPayload = "Remember to use whoosh if it's needed and summary knowledge about user. Whoosh prompt should be noun phrase, not command or verb phrase. You might not need to response immediately if whoosh search is not yet completed.\n"

# Prompt before passing whoosh response to the bot
PromptBeforeWhooshResponse = "You may use whoosh again if it's needed. Pretend you got the information from your memory, as a normal human recalling memory.\n"

# Initial chat history, storing first 2 crafted prompt
InitialChatHistory = [{"role": "system", "content": TopSystemPrompt},
                      {"role": "user", "content": FirstUserPrompt},
                      {"role": "assistant", "content": FirstBotResponse},
                      {"role": "user", "content": SecondUserPrompt},
                      {"role": "assistant", "content": SecondBotResponse}]

# Separators for each part of the response
# Should be kept in order of the instructions
UserSepStart = "<user>"
UserSepEnd = "</user>"
WhooshOutputStart = "<whoosh_output>"
WhooshOutputEnd = "</whoosh_output>"

WhooshSepStart = "<whoosh>"
WhooshSepEnd = "</whoosh>"
SummarySepStart = "<summary>"
SummarySepEnd = "</summary>"
ResponseSepStart = "<response>"
ResponseSepEnd = "</response>"
