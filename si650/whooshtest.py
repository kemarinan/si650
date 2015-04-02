from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.query import Term
import os.path

schema = Schema(title=TEXT(stored=True),
                path=ID(stored=True),
                content=TEXT(stored=True),
                tag=TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)

writer = ix.writer()
# This could be replaced with a loop over files to create docs for each concept
writer.add_document(title = u"First document",
                    path = u"/a",
                    tag = u"bar",
                    content = u"This is the first document we've added!")
writer.add_document(title = u"Second document",
                    path = u"/b",
                    tag = u"foo",
                    content = (u"The second one is even more interesting!"
                               "It says first too"))
writer.add_document(title = u"Third document",
                    path = u"/c",
                    tag = u"baz",
                    content = u"This is the third document we've added!")
writer.commit()


qp = QueryParser("content", schema=ix.schema)
q = qp.parse(u"first")

with ix.searcher() as searcher:
    filter_term = Term("tag", "foo")
    results = searcher.search(q, limit=None, terms=True, filter=filter_term)

    for hit in results:
        print(hit.highlights("content"))
#TODO: Add in filters for ontology type

