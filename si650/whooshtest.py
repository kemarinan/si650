import os.path

from whoosh import fields
from whoosh.analysis import StemmingAnalyzer, StemFilter
from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.query import Term, Variations


schema = Schema(title=TEXT(stored=True),
                path=ID(stored=True),
                content=TEXT(analyzer=StemmingAnalyzer(),
                             spelling=True,
                             stored=True),
                tag=TEXT(stored=True))

if not os.path.exists("index"):
    os.mkdir("index")

ix = create_in("index", schema)

#u added to strings
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

desired_query = u"documets"
qp = QueryParser("content", schema=ix.schema, termclass=Variations)
q = qp.parse(desired_query)

with ix.searcher() as searcher:
    filter_term = Term("tag", "bar")
    corrected = searcher.correct_query(q, desired_query)
    if corrected.query != q:
        print "Did you mean: {}?".format(corrected.string)

    results = searcher.search(q, limit=None, terms=True, filter=filter_term)
    print results[:]

    for hit in results:
        print(hit.highlights("content"))

