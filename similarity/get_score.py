# -*- coding:utf-8 -*-

import elasticsearch


class GetScore(object):
    """
    基于elasticsearch内建的more like this API从而删除文本中的相似数据
    """
    @staticmethod
    def get_similarity(host, name, doc_type, size, id=1):
        es = elasticsearch.Elasticsearch([{'host': host}])

        query_body = {
            "query": {
                "bool": {
                    "must_not": [
                        {
                            "term": {
                                "_id": id
                            }
                        },
                    ],
                    "must": [
                        {
                            "more_like_this": {
                                "fields": ["content"],
                                "like": [
                                    {
                                        "_index": name,
                                        "_type": doc_type,
                                        "_id": id
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        ret = es.search(
            index=name,
            doc_type=doc_type,
            body=query_body,
            size=size
        )
        for hit in ret['hits']['hits']:
            yield hit['_id'], hit['_score']
        pass

    # @staticmethod
    # def remove_similarity_doc(score=float(SCORE)):
    #     count = es.count(index=INDEX, doc_type=DOC_TYPE).get('count')
    #     for i in range(count):
    #         try:
    #             for s in get_similarity(i + 1):
    #                 if s[1] >= score:
    #                     print(es.get(index='similar', doc_type='news', id=i + 1),
    #                           es.get(index='similar', doc_type='news', id=s[0]))
    #                     es.delete(index=INDEX, doc_type=DOC_TYPE, id=s[0])
    #                     pass
    #                 else:
    #                     break
    #         except TransportError:
    #             pass
    #         pass
    #     pass
    #
    # @staticmethod
    # def output_doc():
    #     doc_list = []
    #     count = es.count(index=INDEX, doc_type=DOC_TYPE).get('count')
    #     for i in range(count):
    #         try:
    #             doc_list.append(es.get(index=INDEX, doc_type=DOC_TYPE, id=i + 1).get('_source'))
    #         except TransportError:
    #             pass
    #
    #     print('%s docs after set' % len(doc_list))
    #     with open('after_set.json', 'w') as f:
    #         f.write(json.dumps(doc_list))
    #         pass
    #     pass
    # pass


# main
# index_data()
# print(es.get(index='similar', doc_type='news', id=5))
# remove_similarity_doc()
# print(es.count(index=INDEX, doc_type=DOC_TYPE).get('count'))
# output_doc()