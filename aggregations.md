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

