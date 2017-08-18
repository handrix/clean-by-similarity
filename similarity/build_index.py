# -*- coding:utf-8 -*-

import json
import elasticsearch


class IndexData(object):
    """
    使用elasticsearch建索引
    """
    @staticmethod
    def index_data(input, host, name, doc_type):
        es = elasticsearch.Elasticsearch([{'host': host}])

        with open(input) as f:
            items = json.loads(f.read())
        for num, item in enumerate(items):
            es.index(index=name, doc_type=doc_type, id=num + 1, body=item)
            # print(num + 1)
        print('data index done!')