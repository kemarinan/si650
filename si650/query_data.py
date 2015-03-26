#!/usr/bin/env python
import argparse
import os
import sys

from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Term

def _open_index():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    index_dir = os.path.join(script_dir, "indexes")
    ix = open_dir(index_dir)

    return ix

def _get_results(searcher, query_term, filter_term):
    allow_query = Term("tags", filter_term)
    if filter_term:
        results = searcher.search(query_term, filter=allow_query, limit=None, terms=True)
    else:
        results = searcher.search(query_term, limit=None, terms=True)
    print(results[:])

    for hit in results:
        print(hit.highlights("content"))

def _query_data(args):
    ix =  _open_index()

    user_query= args.query
    filter_term = args.filter_results
    query_parser = QueryParser("content", schema=ix.schema)
    query_term = query_parser.parse(unicode(user_query, "UTF-8"))
    
    with ix.searcher() as searcher:
        _get_results(searcher, query_term, filter_term)

def _add_arg_parse():
    command_line_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("query",
                        help=("Query term to be searched against the indexed "
                              "documents"))
    parser.add_argument("--filter_results",
                        help=("Ontology name to filter the results by"))

    return parser.parse_args(command_line_args)

if __name__ == "__main__":
    args = _add_arg_parse()
    _query_data(args)