#!/usr/bin/env python
import argparse
import os
import sys

from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import Term, Variations


def _open_index():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    index_dir = os.path.join(script_dir, "indexes")
    ix = open_dir(index_dir)

    return ix

def _correct_query(searcher, query_term, user_query):
    corrected = searcher.correct_query(query_term, user_query)
    if corrected.query != query_term:
        print "Did you mean: {}?".format(corrected.string)

def _create_hyperlink(hit):
    hyperlink_prefix = ""
    ontology = hit["tag"].strip('"')
    if ontology == "SNOMEDCT_US":
        hyperlink_prefix = "http://www.snomedbrowser.com/Codes/Details/"
    elif ontology == "LNC":
         pass
    elif ontology == "ICD10CM":
        hyperlink_prefix = "http://www.cms.gov/medicare-coverage-database/staticpages/icd-10-code-lookup.aspx?KeyWord="
    elif ontology == "RXNORM":
        hyperlink_prefix = "http://purl.bioontology.org/ontology/RXNORM/"

    return hyperlink_prefix + hit["umls_id"]

def _get_results(searcher, query_term, filter_term):
    if filter_term:
        allow_query = Term("tag", filter_term.lower())
        results = searcher.search(query_term,
                                  limit=None,
                                  terms=True,
                                  filter=allow_query)
    else:
        results = searcher.search(query_term, limit=None, terms=True)

    all_results = []
    all_results.append(",".join(["Ontology", "ID", "Text"]))

    for hit in results:
         hyperlink = _create_hyperlink(hit)
         all_results.append(",".join([hit["tag"], hyperlink, hit.highlights("content")]))

    return all_results

def _write_to_output_file(all_results, output_fname):
    output_file = open(output_fname, "w")

    for result in all_results:
        output_file.write(result + "\n")

    output_file.close()

def _create_output_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(script_dir, "output")

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    output_fname = os.path.join(output_dir, "output.csv")

    return output_fname

def _query_data(args):
    ix =  _open_index()

    user_query= args.query
    filter_term = args.filter_results

    query_parser = QueryParser("content",
                               schema=ix.schema,
                               termclass=Variations)
    query_term = query_parser.parse(unicode(user_query, "UTF-8"))

    with ix.searcher() as searcher:
        _correct_query(searcher, query_term, user_query)
        all_results = _get_results(searcher, query_term, filter_term)

    return all_results

def _add_arg_parse():
    command_line_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("query",
                        help=("Query term to be searched against the indexed "
                              "documents"))
    parser.add_argument("--filter_results",
                        help=("Ontology name to filter the results by"))

    return parser.parse_args(command_line_args)

def main():
    args = _add_arg_parse()
    all_results = _query_data(args)
    output_fname =  _create_output_dir()
    _write_to_output_file(all_results, output_fname)

if __name__ == "__main__":
    main()

