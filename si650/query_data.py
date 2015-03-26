#!/usr/bin/env python
import argparse
import os
import sys

from whoosh.index import open_dir
from whoosh.qparser import QueryParser

def _open_index():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    index_dir = os.path.join(script_dir, "indexes")
    ix = open_dir(index_dir)

    return ix

def _get_results(searcher, query):
    results = searcher.search(query, limit=None, terms=True)
    print(results[:])

    for hit in results:
        print(hit.highlights("content"))

def _query_data(args):
    ix =  _open_index()

    query_term = args.query
    query_parser = QueryParser("content", schema=ix.schema)
    query = query_parser.parse(unicode(query_term, "UTF-8"))
    
    with ix.searcher() as searcher:
        _get_results(searcher, query)

def _add_arg_parse():
    command_line_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help=("Query term to be searched against "
                                       "the indexed documents"))

    return parser.parse_args(command_line_args)

if __name__ == "__main__":
    args = _add_arg_parse()
    _query_data(args)
