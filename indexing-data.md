# Indices

- Create indices with given requirements.

* alias
* mappings
* settings


## Create

```
PUT logs
{
  "mappings": {
    "properties": {
      "coordinates": {
        "type": "geo_point"
      }
    }
  },
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas":1
  }
}
PUT shakespeare
{
  "mappings": {
    "properties": {
      "speaker": {
        "type": "keyword"
      },
     "play_name": {
        "type": "keyword"
      },
     "line_id": {
        "type": "integer"
      },
     "speech_number": {
        "type": "integer"
      }
    }
  },
   "settings": {
    "number_of_shards": 1,
    "number_of_replicas":1
    }
}


PUT bank
{
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas":1
  }
}

```

## Bulk index

- How to create/index documents.

```json
GET _cat/indices

GET _cat/nodes?v

POST sample-1/_doc
{
  "firsname": "linus",
  "lastname": "torvalds"
  
}

GET sample-1/_doc/mQcF_ynfS9SaTpapVUUOxg
```

- Example of an update shows an update in the metadata version.

```json
POST sample-1/_update/_FOUyXMBxN-miMnwItlo
{
  "doc": {
    "lastname": "torres"
  }
}

{
  "_index" : "sample-1",
  "_type" : "_doc",
  "_id" : "_FOUyXMBxN-miMnwItlo",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 2,
    "failed" : 0
  },
  "_seq_no" : 2,
  "_primary_term" : 3
}

# This removes a field, therefore increments the version.
POST sample-1/_update/_FOUyXMBxN-miMnwItlo
{
  "script": {
    "lang": "painless",
    "source": "ctx._source.remove('middle')"
  }
}

``` 

# Using bulk 

- Download the following

```
$ curl -O https://raw.githubusercontent.com/linuxacademy/content-elast
ic-certification/master/sample_data/shakespeare.json
$ curl -O https://raw.githubusercontent.com/linuxacademy/content-elast
ic-certification/master/sample_data/logs.json
curl -O https://raw.githubusercontent.com/linuxacademy/content-elast
ic-certification/master/sample_data/accounts.json
```

- Doing a bulk operation looks like

```
curl -k -u elastic -H'Content-Type: application/x-ndjson' -X POST    
 'https://localhost:9200/bank/_bulk?pretty' --data-binary @accounts.json > accounts_bulk.json
```

# Define and use index aliases

- Alias is a way to refer to an index.

```

POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "bank",
        "alias": "accounts"
      }
    }
  ]
}
GET bank
GET accounts
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "bank",
        "alias": "accounts"
      }
    }
  ]
}
this removes the index.

```

- It's also posible to alias to a subset filtering.
```json
POST _aliases
{
  "actions": [
    {
      "add": {
        "index": "shakespeare",
        "alias": "henry_IV",
        "filter": {
          "term": {
            "play_name": "Henry IV"
          }
          
        }
      }
    }
  ]
}
```

- Of course we might need to remove indexes.

```
POST _aliases
{
  "actions": [
    {
      "remove": {
        "index": "bank",
        "alias": "sample-2"
      }
    },
    {
      "remove": {
        "index": "bank",
        "alias": "sample-1"
      }
    }
  ]
}
```

# Using index template

- This is an exmaple of creating a template. The feld index_patterns is mandatory

```
PUT _template/logs 
{
 "aliases": {
   "logs_sample": {}
 },
  "mappings": {
    "properties": {
      "field_1": {
        "type": "keyword"
      }
    }
  },
  "settings": {
    "number_of_shards": 1,
    "number_of_replicas": 1
  },
  "index_patterns": ["logs-*"]
}
PUT logs-2020-01-08
GET logs-2020-01-08
```

- So any  index created that mattches the regular expression `logs-*` will have a an alias `logs_sample` 
 and also  properties and settings as those indicated on the template.

# Dynamic Template for a set of requirements


```
PUT sample-3
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_to_keywords": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "keyword"
          }
        }
      },
      {
        "longs_to_integers": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "integer"
          }
        }
      }
    ]
  }
}

  "sample-2" : {
    "aliases" : { },
    "mappings" : {
      "properties" : {
        "firstname" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "lastname" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1596893438732",
        "number_of_shards" : "1",
        "number_of_replicas" : "1",
        "uuid" : "ISV-rNN5STyo-u8ufzdOzg",
        "version" : {
          "created" : "7020199"
        },
        "provided_name" : "sample-2"
      }
    }
  }
}
```

- Example 

```
PUT sample-4
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings_to_keywords": {
          "match_mapping_type": "string",
          "unmatch": "_text",
          "mapping": {
            "type": "keyword"
          }
        }
      },
      {
        "longs_to_integers": {
          "match_mapping_type": "long",
          "mapping": {
            "type": "integer"
          }
        }
      },
      {
        "strings_to_text": {
          "match_mapping_type": "string",
          "match": "_text",
          "mapping": {
            "type": "text"
          }
        }
      }
    ]
  }
}
  
POST sample-4/_doc
{
  "firstname": "jon",
  "lastname": "s",
  "age": 30,
  "bio_text": "so just a littlle bit of data"
}

{
  "sample-4" : {
    "aliases" : { },
    "mappings" : {
      "dynamic_templates" : [
        {
          "strings_to_keywords" : {
            "unmatch" : "_text",
            "match_mapping_type" : "string",
            "mapping" : {
              "type" : "keyword"
            }
          }
        },
        {
          "longs_to_integers" : {
            "match_mapping_type" : "long",
            "mapping" : {
              "type" : "integer"
            }
          }
        },
        {
          "strings_to_text" : {
            "match" : "_text",
            "match_mapping_type" : "string",
            "mapping" : {
              "type" : "text"
            }
          }
        }
      ],
      "properties" : {
        "age" : {
          "type" : "integer"
        },
        "bio_text" : {
          "type" : "keyword"
        },
        "firstname" : {
          "type" : "keyword"
        },
        "lastname" : {
          "type" : "keyword"
        }
      }
    },
    "settings" : {
      "index" : {
        "creation_date" : "1596894075011",
        "number_of_shards" : "1",
        "number_of_replicas" : "1",
        "uuid" : "Knmzp3ieRjiBzSji-jbv3A",
        "version" : {
          "created" : "7020199"
        },
        "provided_name" : "sample-4"
      }
    }
  }
}
```

# Re-index API and Query API


- You can run a script if required, if you don't use it remove it.

```

POST _reindex
{
  "source": {
    "index": "bank"
  },
  "dest": {
    "index": "bank_new"
  },
  "script": {
    
  }
}
```

## Enable remote re-index

In order to enable re-index remote:

- Edit elastisearch.yaml, we need to whitelist the 3 nodes from the other cluster
```
reindex.remote.whitelist: "172.31.126.150:9200, 172.31.117.146:9200, 172.31.125.109:9200"
reindex.ssl.verification_mode: certificate
reindex.ssl.truststore.type: PKCS12
reindex.ssl.keystore.type: PKCS12
reindex.ssl.truststore.path: certs/node-1
reindex.ssl.keystore.path: certs/node-1
```

- Then we need to specify the password for all the certificates.

```
./bin/elasticsearch-keystore  add reindex.ssl.truststore.secure_password
elastic_la

./bin/elasticsearch-keystore  add reindex.ssl.keystore.secure_password
elastic_la
```

## Executing re-index


```
POST _reindex
{
  "source": {
    "remote": {
      "host": "https://172.31.126.150:9200",
      "username": "elastic",
      "password": "elastic"
    }
    , "index": "bank"
  },
  "dest": {
    "index": "banks_new"
  }
}
```

## Re-index with a subset by using query

```
POST _reindex
{
  "source": {
    "remote": {
      "host": "https://172.31.126.150:9200",
      "username": "elastic",
      "password": "elastic"
    },
     "index": "bank",
    "query": {
      "term": {
        "gender.keyword": {
          "value": "M"
        }
      }
    }
  },
  "dest": {
    "index": "accounts_male"
  }
}
```
## Re-index and execute and script to remove some part

```
POST _reindex
{
  "source": {
    "remote": {
      "host": "https://172.31.126.150:9200",
      "username": "elastic",
      "password": "elastic"
    },
     "index": "bank",
    "query": {
      "term": {
        "gender.keyword": {
          "value": "M"
        }
      }
    }
  },
  "dest": {
    "index": "accounts_male"
  },
  "script": {
    "lang": "painless",
    "source": "ctx._source.remove('gender')"
  }
}
```

## Update by query

```
POST bank/_update_by_query
{
  "script": {
    "lang": "painless",
    "source":"""
     ctx._source.balance += ctx._source.balance * 0.03;
     if (ctx._source.transactions == null) {
        ctx_source.transactions = 1;
     }else {
        ctx._source.transactions++;
     }
    """
  }
}
```

## Define and use ingest pipeline

-  The only thing to catch here is the reference to field does not user `ctx._source` form, you access directly the field, therefore `ctx.gender`.

```
PUT _ingest/pipeline/test_pipeline
{
  "description": "Something descriptive about the pipeline",
  "processors": [
    {
      "remove": {
        "field": "account_number"
      }
    },
    {
      "set": {
        "field": "_source.fullname",
        "value": "{{_source.firstname}} {{_source.lastname}}"
      }
    },
    {
      "convert": {
        "field": "age",
        "type": "string"
      }
    },
    {
      "script": {
        "lang": "painless",
        "source": """
          if (ctx.gender == "M") {
            ctx.gender = "male"
          } else {
            ctx.gender = "female"
          }
        """
      }
    }
  ]
}
```

- This needs to run in a `ingest node`, so enabled that in a node. Then you can run the operation `reindex`

```
POST _reindex
{
  "source": {
    "index": "bank"
  },
  "dest": {
    "index": "bank_test",
    "pipeline": "test_pipeline"
  }
}
```
