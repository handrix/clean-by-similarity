# -*- coding:utf-8 -*-

import argparse
import elasticsearch
from elasticsearch.exceptions import TransportError
import json
from similarity.get_score import GetScore
from similarity.build_index import IndexData


def parse_args():
    parser = argparse.ArgumentParser(
        description='remove similarity score that below a certain valueData')
    parser.add_argument(
        '-host', '--host', type=str,
        help='elasticsearch server host',
        default='localhost',
        required=False)
    parser.add_argument(
        '-i', '--input', type=str,
        help='json file input path',
        required=True)
    parser.add_argument(
        '-name', '--name', type=str,
        help='elasticsearch parameter: index name',
        default='default',
        required=False)
    parser.add_argument(
        '-type', '--doc_type', type=str,
        help='elasticsearch parameter: doc type',
        default='news',
        required=False)
    parser.add_argument(
        '-score', '--score', type=str,
        help='drop more than this similary score\'s data',
        default='85',
        required=False)
    parser.add_argument(
        '-o', '--output', type=str,
        help='output file path',
        default='result.json',
        required=False)
    parser.add_argument(
        '-size', '--size', type=str,
        help='data size of a batch',
        default='10',
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
    IndexData.index_data(
        args.input, args.host, args.name, args.doc_type)

    es = elasticsearch.Elasticsearch([{'host': args.host}])
    count = es.count(index=args.name, doc_type=args.doc_type).get('count')
    print('origin num: %s' % count)

    for i in range(int(count)):
        try:
            for s in GetScore.get_similarity(
                    host=args.host, name=args.name,
                    doc_type=args.doc_type, size=args.size,
                    id=i + 1):
                if s[1] >= float(args.score):
                    es.delete(index=args.name, doc_type=args.doc_type, id=s[0])
                else:
                    break
        except TransportError:
            pass

    count = es.count(
        index=args.name, doc_type=args.doc_type).get('count')
    doc_list = []
    print('after that: %s' % count)

    for i in range(count):
        try:
            doc_list.append(
                es.get(index=args.name, doc_type=args.doc_type, id=i + 1).get('_source'))
        except TransportError:
            pass

    with open(args.output, 'w') as f:
        f.write(json.dumps(doc_list))
    print('result path: %s' % args.output)


if __name__ == "__main__":
    main()
