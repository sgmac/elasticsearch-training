# Mappings 

- The type `text` is broken with an analyzer. A relevance score is generated for each of the hits. This is for anything implemented full-search text.
- The type `keyword` there is not analyzer, if a word has empty spaces, you would have to look for them. (Name, things is going to be a name)

```
PUT sample-1
{
  "mappings": {
    "properties": {
      "name":{
        "type": "keyword"
      },
      "bio": {
        "type": "text"
      },
      "age": {
        "type": "short"
      },
      "interest_rate": {
        "type": "scaled_float",
        "scaling_factor": 10000
      },
      "geoip": {
        "type": "geo_point"
      },
      "ip":{
        "type": "ip"
      },
      "is_member": {
        "type": "boolean"
      },
      "last_modified": {
        "type": "date"
      }
    }
    }
}
```

- The `scaling_factor` determines how many decimals we want.
- The `geo_point` can be use to do graphs in Kibana

## Define a custom analyzer

```
POST _analyze
{
  "analyzer": "standard",
  "text": "The 3 QUICK Brown-foxes jumped over the neighbor's fence"
}

{
  "tokens" : [
    {
      "token" : "the",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "3",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "<NUM>",
      "position" : 1
    },
    {
      "token" : "quick",
      "start_offset" : 6,
      "end_offset" : 11,
      "type" : "<ALPHANUM>",
      "position" : 2
    },
    {
      "token" : "brown",
      "start_offset" : 12,
      "end_offset" : 17,
      "type" : "<ALPHANUM>",
      "position" : 3
    },
    {
      "token" : "foxes",
      "start_offset" : 18,
      "end_offset" : 23,
      "type" : "<ALPHANUM>",
      "position" : 4
    },
    {
      "token" : "jumped",
      "start_offset" : 24,
      "end_offset" : 30,
      "type" : "<ALPHANUM>",
      "position" : 5
    },
    {
      "token" : "over",
      "start_offset" : 31,
      "end_offset" : 35,
      "type" : "<ALPHANUM>",
      "position" : 6
    },
    {
      "token" : "the",
      "start_offset" : 36,
      "end_offset" : 39,
      "type" : "<ALPHANUM>",
      "position" : 7
    },
    {
      "token" : "neighbor's",
      "start_offset" : 40,
      "end_offset" : 50,
      "type" : "<ALPHANUM>",
      "position" : 8
    },
    {
      "token" : "fence",
      "start_offset" : 51,
      "end_offset" : 56,
      "type" : "<ALPHANUM>",
      "position" : 9
    }
  ]
}

```

- But Elasticsearch has many analyzers

```
POST _analyze
{
  "analyzer": "english",
  "text": "The 3 QUICK Brown-foxes jumped over the neighbor's fence"
}

{
  "tokens" : [
    {
      "token" : "3",
      "start_offset" : 4,
      "end_offset" : 5,
      "type" : "<NUM>",
      "position" : 1
    },
    {
      "token" : "quick",
      "start_offset" : 6,
      "end_offset" : 11,
      "type" : "<ALPHANUM>",
      "position" : 2
    },
    {
      "token" : "brown",
      "start_offset" : 12,
      "end_offset" : 17,
      "type" : "<ALPHANUM>",
      "position" : 3
    },
    {
      "token" : "fox",
      "start_offset" : 18,
      "end_offset" : 23,
      "type" : "<ALPHANUM>",
      "position" : 4
    },
    {
      "token" : "jump",
      "start_offset" : 24,
      "end_offset" : 30,
      "type" : "<ALPHANUM>",
      "position" : 5
    },
    {
      "token" : "over",
      "start_offset" : 31,
      "end_offset" : 35,
      "type" : "<ALPHANUM>",
      "position" : 6
    },
    {
      "token" : "neighbor",
      "start_offset" : 40,
      "end_offset" : 50,
      "type" : "<ALPHANUM>",
      "position" : 8
    },
    {
      "token" : "fenc",
      "start_offset" : 51,
      "end_offset" : 56,
      "type" : "<ALPHANUM>",
      "position" : 9
    }
  ]
}
```
- The `simple` anaylzer would split on everything  (the 's' for instance)
- The `whitespace` splits the word based on whitespace and therefore  you need to match the exact word. `QUICK`


## Create a custom analyzer

```
PUT analysis-1
{
  "mappings": {
    "properties": {
    "text": {
      "type": "text",
      "analyzer": "whitespace_lowercase"
    }
    }
  }, 
  "settings": {
    "analysis": {
      "analyzer": {
        "whitespace_lowercase": {
          "tokenizer": "whitespace",
          "filter": [
            "lowercase"
          ]
        }
      }
    }
  }
}


PUT analysis-1/_doc/1
{
  "text": "The 3 QUICK Brown-foxes jumped over the neighbor's fence"
}

```

- Then we can do a search 

```
GET analysis-1/_search 
{
  "query": {
    "match": {
      "text": "quick"
    }
  }
}

{
  "took" : 318,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.2876821,
    "hits" : [
      {
        "_index" : "analysis-1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.2876821,
        "_source" : {
          "text" : "The 3 QUICK Brown-foxes jumped over the neighbor's fence"
        }
      }
    ]
  }
}

POST analysis-1/_analyze
{
  "analyzer": "whitespace_lowercase",
  "text": "QUICK"
}

{
  "tokens" : [
    {
      "token" : "quick",
      "start_offset" : 0,
      "end_offset" : 5,
      "type" : "word",
      "position" : 0
    }
  ]
}
```

- Second example is more comples doing a mapping of emojis. Custom analyzer.

```

PUT analysis-2
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "analyzer": "standard_emoji"
      }
    }
  },
  "settings": {
    "analysis": {
      "analyzer": {
        "standard_emoji": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop"
          ],
          "char_filter": [
            "emoji"
          ]
        }
      },
      "filter": {
        "english_stop": {
          "type": "stop",
          "stopwords": "_english_"
        }
      },
      "char_filter": {
        "emoji": {
          "type": "mapping",
          "mappings": [
            ":) => happy",
            ":( => sad"
          ]
        }
      }
    }
  }
}
```

- Now the emoji match

```
UT analysis-2/_doc/1
{
  "text": "The 3 :) Brown-foxes jumped over the :( neighbor's fence."
}

GET analysis-2/_search
{
  "query": {
    "match": {
      "text": "happy"
    }
  }
}
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.2876821,
    "hits" : [
      {
        "_index" : "analysis-2",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.2876821,
        "_source" : {
          "text" : "The 3 :) Brown-foxes jumped over the :( neighbor's fence."
        }
      }
    ]
  }
}

POST analysis-2/_analyze
{
  "analyzer": "standard_emoji",
  "text": ":("
}
             
	     {
  "tokens" : [
    {
      "token" : "sad",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "<ALPHANUM>",
      "position" : 0
    }
  ]
}
```
## Define and use multi-fields with different data types and/or anlyzers

- The multi-field allows to use multiple analyzers for a given field. You can index a word just one time, and use the multi-field functionality.

```
PUT sample-2
{
  "mappings": {
    "properties": {
      "field_1":{ 
        "type": "keyword",
        "fields": {
          "standard": {
            "type": "text"
          },
          "simple": {
            "type": "text",
            "analyzer": "simple"
          },
          "english": {
            "type": "text",
            "analyzer": "english"
          }
        }
      }
    }
  }
```


## Nested array of objects
```
PUT nested_array_1/_doc/1
{
  "group": "LA instructors",
  "instructors": [
    {
      "firstname": "myles",
      "lastname": "young",
      "email": "mylest@la.com"
    },
      {
      "firstname": "himmy",
      "lastname": "fallon",
      "email": "hfallont@la.com"
    }
    ]
}
```

- The problem with this objets is doing queryes there is not relationship between the objects, for instance, the query below should not return a hit because those attributes are from different objects, not from the same.

```
GET nested_array_1/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "instructors.firstname.keyword": {
              "value": "myles"
            }
          }
        },
        {
          "term": {
            "instructors.lastname.keyword": {
              "value": "fallon"
            }
          }
        }
        
      ]
    }
  }
}
```

- This is because Elasticsearch stores them flatten:

```json
{
  "groups": "LA instructors",
  "instructors.firsname": ["myles", "himmy"],
  "instructors.email": ["mylest@la.com", "hfallon@la.com"]
}
```

- In  order to fix this, we need to specify a `mapping` of type `nested`.

```
PUT nested_array_2
{
  "mappings": {
    "properties": {
      "instructors": {
        "type": "nested"
      }
    }
  }
}
PUT nested_array_2/_doc/1
{
  "group": "LA instructors",
  "instructors": [
    {
      "firstname": "myles",
      "lastname": "young",
      "email": "mylest@la.com"
    },
      {
      "firstname": "himmy",
      "lastname": "fallon",
      "email": "hfallont@la.com"
    }
    ]
}
GET nested_array_2/_search
{
  "query": {
    "nested": {
      "path": "instructors",
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "instructors.firstname.keyword": {
                  "value": "myles"
                }
              }
            },
            {
              "term": {
                "instructors.lastname.keyword": {
                  "value": "fallon"
                }
              }
            }
          ]
        }
      }
    }
  }
}

{
  "took" : 14,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 0,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  }
}


```

- If `lastname` is changed  to `young` that would produce a hit, but showing both objects. If we want to show only one, we need a more advance query using `inner_hits`.

```

GET nested_array_2/_search
{
  "query": {
    "nested": {
      "path": "instructors",
      "query": {
        "bool": {
          "must": [
            {
              "term": {
                "instructors.firstname.keyword": {
                  "value": "myles"
                }
              }
            },
            {
              "term": {
                "instructors.lastname.keyword": {
                  "value": "young"
                }
              }
            }
          ]
        }
      },
      "inner_hits": {
        "highlight": {
          "fields": {
            "instructors.firstname.keyword": {},
            "instructors.lastname.keyword": {}
            }
          }
        }
      }
    }
  }
}
```

## Configure an index that implements a Parent/Child relationship

- ES uses flatten data, `denormalized` data. You don't want to break data, you want all the data in the same document. 
- DB you want to normalize data, not for ES.
- You can have only one parent, and answers with multiple children
- You should use explcit IDs.
- They need to be in the same shard

```json


PUT parent_child-1
{
  "mappings": {
    "properties": {
      "qa":{
        "type": "join",
        "relations":{
          "question": "answer"
        }
      }
    }
  }
}

PUT parent_child-1/_doc/
{
  "text": "Which mode type in Elasticsearch stores data?",
  "qa": {
    "name": "question"
  }
}

# route the doc 2 to the same shard than doc 1
PUT parent_child-1/_doc/2?routing=1
{
 "text": "Data node",
 "qa": {
   "name": "answer",
   "parent": "1"
 }
}
```



