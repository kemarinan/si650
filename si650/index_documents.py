#!/usr/bin/env python
import os
import re
import sys

from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import *
from whoosh.index import create_in


def _add_document(input_file, writer):
    file_reader = open(input_file, "r")
    for i, line in enumerate(file_reader.readlines()):
        doc_title = "_".join([os.path.basename(input_file), str(i + 1)])
        ontology, unique_id, doc_content = line.split("\t")
        writer.add_document(title=unicode(doc_title,"UTF-8"),
                            tag=unicode(ontology, "UTF-8"),
                            umls_id=unicode(unique_id, "UTF-8"),
                            content=unicode(doc_content, "UTF-8"))
    writer.commit()

def _create_writer(index_dir):
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True),
                    content=TEXT(analyzer=StemmingAnalyzer(),
                                 spelling=True,
                                 stored=True),
                    tag=TEXT(stored=True),
                    umls_id=TEXT(stored=True))

    ix = create_in(index_dir, schema)
    writer = ix.writer()

    return writer

def _check_index_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    index_dir = os.path.join(script_dir, "indexes")

    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    return index_dir

def _index_documents(input_tsv):
    index_dir = _check_index_dir()
    writer = _create_writer(index_dir)

    _add_document(input_tsv, writer)

def run():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    input_tsv = os.path.join([script_dir, "sample_data_quoted.tsv"])
    _index_documents(input_tsv)

if __name__ == "__main__":
    run()
