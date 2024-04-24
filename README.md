# LLTM
An efford to combine prompt-engineering, LLM and Whoosh search library, to create a long-term-memory LLM, capable of remembering textual, visuals (and maybe even more) details about different user.

# Status
Work in progress. See tracklist:
- [x] Basic LLM interaction APIs
- [x] Crafted prompts for instructing LLM
- [x] Parse textual details
- [ ] Search APIs
- [ ] Knowledge base security
- [ ] REPL
- [ ] Parse visual details

# Demo for implemented parts

- LLM interaction APIs (LLM can requires searching):

```python
>>> import llm
>>> a = llm.LLM('None', model='gpt-4', endpoint='http://192.168.1.12:8080/v1')                                                                       
>>> a.add_user_prompt("Hello, I'm gvl610")
>>> br = a.get_base_response()                                                                                                                       
>>> br
'<whoosh>gvl610</whoosh>\n<summary>New user identified as gvl610. No additional information provided yet.</summary>\n<response>Hello gvl610! How can I assist you today?</response>\n'
>>> a.parse_response(br)
('gvl610', 'New user identified as gvl610. No additional information provided yet.', 'Hello gvl610! How can I assist you today?')
>>> r = a.parse_response(br) 
>>> r[0]
'gvl610'
>>> a.add_whoosh_output("[{'content': 'gvl610 ran Linux on Arduino UNO', 'time'='last year'}]")
>>> br = a.get_base_response() 
>>> br
"<summary>gvl610 has experience running Linux on Arduino UNO from last year.</summary>\n<response>That's quite an interesting project, gvl610! Running Linux on an Arduino UNO is no small feat. How has that experience been for you, and what brings you here today?</response>\n"
>>>
```

# Used libraries
- [`openai-python`](https://github.com/openai/openai-python)
- [`whoosh-reloaded`](https://github.com/Sygil-Dev/whoosh-reloaded)
