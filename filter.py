# -*- coding:utf-8 -*-

import argparse
import elasticsearch
import json
from .similarity.get_score import GetScore


def parse_args():
    parser = argparse.ArgumentParser(
        description='remove similarity score that below a certain valueData')
    parser.add_argument(
        '-h', '--host', type=str,
        help='elasticsearch host',
        default='localhost',
        required=False)
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
    parser.add_argument(
        '-s', '--score', type=str,
        help='similary score',
        required=True)
    parser.add_argument(
        '-o', '--output', type=str,
        help='output file path',
        default='after_set.json',
        required=False)
    return parser.parse_args()


def main():
    """
    index = 'similar'
    doc_type = 'news'
    size = 15
    score = 85
    id = 1
    :return:
    """
    args = parse_args()
    es = elasticsearch.Elasticsearch([{'host': args.host}])
    doc_list = []

    count = es.count(index=args.name, doc_type=args.doc_type).get('count')

    for i in range(count):
        for s in GetScore.get_similarity(
                host=args.host, name=args.name, doc_type=args.doc_type, size=args.size, id=i + 1):
            if s[1] >= float(args.score):
                doc_list.append(
                    es.get(index=args.name, doc_type=args.doc_type, id=i + 1).get('_source'))
                pass
            else:
                break

    with open(args.output, 'w') as f:
        f.write(json.dumps(doc_list))
        pass


if __name__ == "__main__":
    main()
