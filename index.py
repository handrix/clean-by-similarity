# -*- coding:utf-8 -*-

import argparse
from .similarity.build_index import IndexData


def parse_args():
    parser = argparse.ArgumentParser(
        description='build index')
    parser.add_argument(
        '-i', '--input', type=str,
        help='The original json file',
        required=True)
    parser.add_argument(
        '-h', '--host', type=str,
        help='elasticsearch host',
        default='localhost',
        required=False)
    parser.add_argument(
        '-n', '--name', type=str,
        help='elasticsearch parameter',
        required=True)
    parser.add_argument(
        '-d', '--doc_type', type=str,
        help='elasticsearch parameter',
        required=True)
    return parser.parse_args()


def main():
    args = parse_args()
    IndexData.index_data(
        args.input, args.host, args.index, args.doc_type)


if __name__ == "__main__":
    main()
