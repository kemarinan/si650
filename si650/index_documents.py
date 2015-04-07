#!/usr/bin/env python
import argparse
import glob
import os
import re
import sys

from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import *
from whoosh.index import create_in


#TODO: add partial matching functionality (n-grams)
def _add_document(input_file, writer):
    file_reader = open(input_file, "r")
    for i, line in enumerate(file_reader.readlines()):
        doc_title = "_".join([os.path.basename(input_file), str(i + 1)])
        ontology, unique_id, doc_content = line.split("\t")
        writer.add_document(title=unicode(doc_title,"UTF-8"),
                            tag=unicode(ontology, "UTF-8"),
                            content=unicode(doc_content, "UTF-8"))
    writer.commit()

def _create_writer(index_dir):
    stem_analyzer = StemmingAnalyzer()
    schema = Schema(title=TEXT(analyzer=stem_analyzer, stored=True),
                    path=ID(stored=True),
                    content=TEXT(analyzer=stem_analyzer, stored=True),
                    tag=TEXT(analyzer=stem_analyzer, stored=True))

    ix = create_in(index_dir, schema)
    writer = ix.writer()

    return writer

def _check_index_dir():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    index_dir = os.path.join(script_dir, "indexes")

    if not os.path.exists(index_dir):
        os.mkdir(index_dir)

    return index_dir

def _index_documents(args):
    index_dir = _check_index_dir()
    writer = _create_writer(index_dir)

    input_dir = args.input_dir
    input_files = glob.glob(os.path.join(input_dir, "*"))

    for input_file in input_files:
        _add_document(input_file, writer)

def _add_arg_parse():
    command_line_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help=("Path to the input directory "
                                           "containing a collection of"
                                           "files to be indexed into documents"))

    return parser.parse_args(command_line_args)

if __name__ == "__main__":
    args = _add_arg_parse()
    _index_documents(args)
