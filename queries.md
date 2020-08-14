# Queries

## Write and execute search query for terms

- There are analyze(full-text) queries and non-analyze

```
GET _search
{
  "query": {
    "match": {
      "text_entry": "to be or not to be"
    }
  }
}

```
- The above returns all the the documents which `text_entry` field matches, regardless upercase. The below matches in some analyze form (so the underline tokens are the same). The analyzer can be changed but defaults to whatever was defined in the `text_entry` field.

```
GET _search
{
  "query": {
    "match_phrase": {
      "text_entry": "to be or not to be"
    }
  }
}
```

- It is possible to do a `multi_match` query against several fields.

```json
GET _search
{
  "query": {
    "multi_match": {
      "query": "Crime",
      "fields": ["text_entry", "relatedContent.og:description"]
    }
  }
}
```

- This query below allows to use the query DSL (Kibana)

```
GET _search
{
  "query": {
    "query_string": {
      "default_field": "text_entry",
      "query": "romeo AND juliet"
    }
  }
}

GET _search
{
  "query": {
    "query_string": {
      "default_field": "text_entry",
      "query": "(romeo AND juliet) OR (mother AND father)"
    }
  }
}

{
  "took" : 188,
  "timed_out" : false,
  "_shards" : {
    "total" : 12,
    "successful" : 12,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 29,
      "relation" : "eq"
    },
    "max_score" : 27.037975,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_type" : "_doc",
        "_id" : "87141",
        "_score" : 27.037975,
        "_source" : {
          "type" : "line",
          "line_id" : 87142,
          "play_name" : "Romeo and Juliet",
          "speech_number" : 19,
          "line_number" : "3.2.127",
          "speaker" : "JULIET",
          "text_entry" : "Is father, mother, Tybalt, Romeo, Juliet,"
        }
      },
```

## Non-analyze queries



- *term* The search below does not get a match because lacks of analyzer, so `ROMEO` would return a hit.
```
# term level query

GET _search
{
  "query": {
    "term": {
      "speaker": {
        "value": "romeo"
      }
    }
  }
}
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 12,
    "successful" : 12,
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

- **multiple terms** on the same field.

```
# terms
GET _search
{
  "query": {
    "terms": {
      "speaker": [
        "ROMEO",
        "JULIET",
        "HAMLET"
        ]
    }
  }
}
```

- **range** this example searches for numerical data. It can be used for 2 dates as well.

```
# range (numerical)
GET _search
{
  "query": {
    "range": {
      "age":  {
        "gte": 40,
        "lt": 50
      }
    }
  }
}
```
- **wilcard** will use regular expressions for a given field.

```json
# wildcard
GET _search 
{
  "query":{
    "wildcard": {
      "city.keyword": {
        "value": "*ville"
      }
    }
  }
}
```

- **regex**   you need to escape the `.` and the escape character to avoid JSON to search for `\`.
```
# regex
GET _search
{
  "query": {
    "regexp": {
      "email.keyword": ".*@pyrami\\.com"
    }
  }
}
