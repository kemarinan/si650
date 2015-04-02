from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.fields import *
import os.path

schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)

#u added to strings
writer = ix.writer()
# This could be replaced with a loop over files to create docs for each concept
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


qp = QueryParser("content", schema=ix.schema)
q = qp.parse(u"first")

with ix.searcher() as searcher:
    results = searcher.search(q, limit=None, terms=True)
    print(results[:])

    for hit in results:
        print(hit.highlights("content"))

#TODO: Add in filters for ontology type


