#!/usr/bin/env python3

import json
from elasticsearch import Elasticsearch

es = Elasticsearch(
        hosts=[{'host': '192.168.1.63', 'port': 9200}]
        )

data = json.load(open("movies.json", 'r'))

n=1
for movie in data:
    res = es.index(index="movies", id=n, body=movie)
    print(res)
    n+=1
