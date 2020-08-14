# Aggregations

- Ask question to the data for analytics.

## Metric and bucket aggregations

- Cardinality, unique of elements.  The are two types of string fields.
- **text** field for full-text search. (very expensive for aggs)
- **keyword** for aggregations.

```
GET logs/_search
{
  "aggs": {
    "unique_clients": {
      "cardinality": {
        "field": "clientip"
      }
    }
  }
}

# this would failed trying to use `clientip` because is a text field.
 "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "Fielddata is disabled on text fields by default. Set fielddata=true on [clientip] in order to load fielddata in memory by uninverting the inverted index. Note that this can however use significant memory. Alternatively use a keyword field instead."
      }
```
- We can see the number of unique clients but discarding the results.

```
GET logs/_search?size=0
{
  "aggs": {
    "unique_clients": {
      "cardinality": {
        "field": "clientip.keyword"
      }
    }
  }
}
```

- Aggregations `sum, avg`

```json

GET logs/_search 
{
  "size": 0,
  "aggs": {
    "avg_of_bytes": {
      "avg": {
        "field": "bytes"
      }
    }
  }
}

{
  "took" : 9,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "avg_of_bytes" : {
      "value" : 5651.861977865048
    }
  }
}

```

- How may response different 200 error

```
GET logs/_search 
{
  "size": 0,
  "aggs": {
    "response_codes": {
      "terms": {
        "field": "response.keyword",
        "size": 10
      }
    }
  }
}

{
  "took" : 117,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "response_codes" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "200",
          "doc_count" : 12871
        },
        {
          "key" : "404",
          "doc_count" : 693
        },
        {
          "key" : "503",
          "doc_count" : 441
        }
      ]
    }
  }
}
```

- How many requests per day

```json
GET logs/_search
{
  "size": 0,
  "aggs": {
    "requests_per_day": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "day"
      }
    }
  }
}
```

## Sub aggregations

- Bucket example counting the types of images extension.

```
GET logs/_search
{
  "size": 0,
  "aggs": {
    "extensions": {
      "terms": {
        "field": "extension.keyword",
        "size": 10
      }
    }
  }
}
```
- Get the `sum_of_bytes` of the the different type of extensions.

```

GET logs/_search
{
  "size": 0,
  "aggs": {
    "extensions": {
      "terms": {
        "field": "extension.keyword",
        "size": 10,
        "order": {
          "sum_of_bytes": "desc"
        }
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        }
      }
    }
  }
}
```

- Get the number of unique clients per hour

```
GET logs/_search
{
  "size": 0,
  "aggs": {
    "per_hour": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "hour"
      },
      "aggs": {
        "unique_clients": {
          "cardinality": {
            "field": "clientip.keyword"
          }
        }
      }
    }
  }
}
```

## Pipelines aggregations

- **Sibbling aggregations**

```
GET logs/_search
{
  "size": 0,
  "aggs": {
    "extensions": {
      "terms": {
        "field": "extension.keyword",
        "size": 10,
        "order": {
          "sum_of_bytes": "desc"
        }
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        }
      }
    },
    "total": {
      "sum_bucket": {
        "buckets_path": "extensions>sum_of_bytes"
      }
    }
  
  }
}
{
  "took" : 16,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "extensions" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "jpg",
          "doc_count" : 9165,
          "sum_of_bytes" : {
            "value" : 5.1107834E7
          }
        },
        {
          "key" : "png",
          "doc_count" : 1303,
          "sum_of_bytes" : {
            "value" : 1.3310171E7
          }
        },
        {
          "key" : "css",
          "doc_count" : 2253,
          "sum_of_bytes" : {
            "value" : 1.2366506E7
          }
        },
        {
          "key" : "php",
          "doc_count" : 397,
          "sum_of_bytes" : {
            "value" : 1942746.0
          }
        },
        {
          "key" : "gif",
          "doc_count" : 887,
          "sum_of_bytes" : {
            "value" : 427070.0
          }
        }
      ]
    },
    "total" : {
      "value" : 7.9154327E7
    }
  }
}
```

**parent aggregations**

- This is accumulative in respect the previous bucket.

```

GET logs/_search
{
  "size": 0,
  "aggs": {
    "per_hour": {
      "date_histogram": {
        "field": "@timestamp",
        "calendar_interval": "hour"
      },
      "aggs": {
        "sum_of_bytes": {
          "sum": {
            "field": "bytes"
          }
        },
      "cumulative_sum_of_bytes": {
        "cumulative_sum": {
          "buckets_path": "sum_of_bytes"
        }
      },
      "bytes_per_second": {
        "derivative": {
          "buckets_path": "cumulative_sum_of_bytes",
          "unit": "second"
        }
      }
      }
    }
  }
}
{
  "took" : 28,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10000,
      "relation" : "gte"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "per_hour" : {
      "buckets" : [
        {
          "key_as_string" : "2015-05-18T00:00:00.000Z",
          "key" : 1431907200000,
          "doc_count" : 5,
          "sum_of_bytes" : {
            "value" : 30674.0
          },
          "cumulative_sum_of_bytes" : {
            "value" : 30674.0
          }
        },
        {
          "key_as_string" : "2015-05-18T01:00:00.000Z",
          "key" : 1431910800000,
          "doc_count" : 3,
          "sum_of_bytes" : {
            "value" : 15382.0
          },
          "cumulative_sum_of_bytes" : {
            "value" : 46056.0
          },
          "bytes_per_second" : {
            "value" : 15382.0,
            "normalized_value" : 4.272777777777778
          }
        },
        {
          "key_as_string" : "2015-05-18T02:00:00.000Z",
          "key" : 1431914400000,
          "doc_count" : 23,
          "sum_of_bytes" : {
            "value" : 124196.0
          },
          "cumulative_sum_of_bytes" : {
            "value" : 170252.0
          },
          "bytes_per_second" : {
            "value" : 124196.0,
            "normalized_value" : 34.49888888888889
          }
        },
        {
          "key_as_string" : "2015-05-18T03:00:00.000Z",
          "key" : 1431918000000,
          "doc_count" : 38,
          "sum_of_bytes" : {
            "value" : 183612.0
          },
          "cumulative_sum_of_bytes" : {
            "value" : 353864.0
          },
          "bytes_per_second" : {
            "value" : 183612.0,
            "normalized_value" : 51.00333333333333
          }
        },
```
