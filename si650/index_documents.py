#!/usr/bin/env python
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.fields import *
import os

def _add_documents(writer):
    writer.add_document(title = u"First document",
                        path = u"/a",
                        content = u"This is the first document we've added!")
    writer.add_document(title = u"Second document",
                        path = u"/b",
                        content = (u"The second one is even more interesting!"
                                   u"It says firstly too"))
    writer.add_document(title = u"Third document",
                        path = u"/c",
                        content = u"This is the third document we've added!")
    writer.commit()

def main():
    if not os.path.exists("index"):
        os.mkdir("index")
    
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True),
                    content=TEXT(stored=True))
    ix = create_in("index", schema)
    
    writer = ix.writer()

    _add_documents(writer)

if __name__ == "__main__":
    main()