'''
LLTM - Lite long-term-memory implementation for LLM
Created by gvl610

This file contains abstract layers for interacting with Whoosh search
'''

import os

from whoosh import index
from whoosh.fields import Schema, TEXT, ID, DATETIME, KEYWORD
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser
from whoosh.index import create_in, open_dir
from whoosh.query import Variations

from datetime import datetime, timezone
from dateutil import tz
from uuid_extensions import uuid7str

NUMBER_OF_SEARCH_RESULT = 5

class LTM():
    '''
    Abstract class for interacting with Whoosh search
    Args:
        index_dir (str): directory to save indexed result into
    '''
    def __init__(self, user_id, index_dir='ltm_data'):
        self.user_id = user_id

        # Create schema
        self.schema = self.create_schema()

        # Open indexed directory, or create new if none is found
        self.index_dir = index_dir
        if not os.path.exists(self.index_dir):
            os.mkdir(self.index_dir)
            self.ix = create_in(self.index_dir, self.schema)
        else:
            self.ix = open_dir(self.index_dir)

    '''
    Create new schema
    '''
    def create_schema(self):
        return Schema(
            id=ID(unique=True, stored=True), # Unique UUID7 of the document
            content=TEXT(analyzer=StemmingAnalyzer(), stored=True),       # Content
            time=DATETIME(stored=True),      # UTC time creation of the document
            user_id=ID(stored=True),         # The user whom this document is created for
            privacy=KEYWORD(stored=True),    # Privacy (public, private, shared)
            access_list=KEYWORD(stored=True) # List of user_id (others than owner) who will be able to access the document. Only applicable if privacy == "shared".
        )

    '''
    Add document to index
    Each document should be represented by a dictionary of the following format:
    {
        "content": "document's content",
        "user_id": "user123",
        "privacy": "public", # Can be public/private/shared
        "access_list": "user345,user678" # List of users (other than owner) who can access
    }
    Args:
        data (dict): dictionary containing schema-formated information
    Return:
        UUID7 string of the document
    '''
    def add_data(self, data):
        writer = self.ix.writer()
        uid = uuid7str()
        writer.add_document(
            id = uid, # UUID7 for better indexing
            content = data["content"], # Actual content
            time = datetime.now(timezone.utc), # UTC time (will be converted back to local time later)
            user_id = data["user_id"], # Owner 
            privacy = data["privacy"], # Privacy
            access_list = data["access_list"] # Access list
        )
        
        # Commit the new documents
        writer.commit()

        # Return UUID7
        return uid
    
    '''
    Add private knowledge field
    Args:
        data (str): knowledge field
    Return:
        UUID7 string of the document
    '''
    def add_private_data(self, data):
        return self.add_data({
            "content": data,
            "user_id": self.user_id,
            "privacy": "private",
            "access_list": ""
        })

    '''
    Remove data from index
    Args:
        id (str): UUID7 ID of the document
    '''
    def remove_data(self, id):
        writer = self.ix.writer()
        writer.delete_by_term('id', id)
        writer.commit()
    
    '''
    Update document fields
    Args:
        id (str): UUID7 ID of the document
        **fields: fields to update
    '''
    def update_document_fields(self, id, **fields):
        writer = self.ix.writer()
        writer.update_document(id=id, **fields)
        writer.commit()

    '''
    Multiple fields search
    Args:
        fields_to_search (list): list of strings of field names to seach for. Eg: ['content', 'privacy']
        query_terms (str): query terms. Eg: 'content:some thing privacy:public'
        n_search_result (int): max number of search results. Default is NUMBER_OF_SEARCH_RESULT
    '''
    def multifield_search(self, fields_to_search, query_terms, n_search_result=NUMBER_OF_SEARCH_RESULT):
        with self.ix.searcher() as searcher:
            # Use MultifieldParser to search across multiple fields
            query = MultifieldParser(fields_to_search, self.ix.schema, termclass=Variations).parse(query_terms)
            results = searcher.search(query, limit=n_search_result)

            # Return a list of dictionaries with the document content
            r = [result.fields() for result in results]

            # Search result post-processing
            for i in range(len(r)):
                # Do security checks
                # If document is not owned by user_id
                if r[i]["user_id"] != self.user_id:
                    # If document is private and not shared for current user_id
                    if (r[i]["privacy"] == "private") and (not self.user_id in r[i]["access_list"]):
                        # -> remove document
                        r.pop(i)

                # Remove ID + security fields
                r[i].pop('id', None)
                r[i].pop('user_id', None)
                r[i].pop('privacy', None)
                r[i].pop('access_list', None)

                # Replace UTC time object with local time string
                r[i]["time"] = str(r[i]["time"].replace(tzinfo=tz.tzutc()).astimezone(tz.tzlocal()))
            
            return r
    
    '''
    Content search
    Args:
        content (str): search content
        n_search_result (int): max number of search results. Default is NUMBER_OF_SEARCH_RESULT
    '''
    def content_search(self, content, n_search_result=NUMBER_OF_SEARCH_RESULT):
        return self.multifield_search(["content"], "content:" + content, n_search_result)
