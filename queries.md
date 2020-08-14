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
```

## Query boolean

- By default if you don't specify `minimum_should_match` does not show how many matches. Use `filter` to avoid modifying the relevance score.

```
GET _search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "gender.keyword": {
              "value": "F"
            }
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "state.keyword": {
              "value":"RI"
            }
          }
        }
        ],
        "should": [
          {
            "term": {
              "lastname.keyword": {
                "value": "Meyers"
              }
            }
          },
          {
          "term": {
              "lastname.keyword": {
                "value": "Owens"
              }
            }
          }
        ],
        "minimum_should_match": 1,
	"filter": {
	    "term":{ 
	       "city.keyword": "Jacksonburg"
	    }
	}
    }
  }
}
```

- An useful tip is to name queries using `_name` attribute, this way you can reduce the query by removing the less relevant information.

```
GET _search
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "gender.keyword": {
              "_name": "gender",
              "value": "F"
            }
          }
        }
      ],
      "must_not": [
        {
          "term": {
            "state.keyword": {
              "_name": "state",
              "value":"RI"
            }
          }
        }
        ],
        "should": [
          {
            "term": {
              "lastname.keyword": {
                "_name":"lastname_1",
                "value": "Meyers"
              }
            }
          },
          {
          "term": {
              "lastname.keyword": {
                "_name": "lastname_2",
                "value": "Owens"
              }
            }
          }
        ],
        "minimum_should_match": 1,
        "filter": {
          "term": {
            "city.keyword": "Jacksonburg"
          }
        }
    }
  }
}
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 12,
    "successful" : 12,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 7.2125177,
    "hits" : [
      {
        "_index" : "bank",
        "_type" : "_doc",
        "_id" : "51",
        "_score" : 7.2125177,
        "_source" : {
          "account_number" : 51,
          "balance" : 14097,
          "firstname" : "Burton",
          "lastname" : "Meyers",
          "age" : 31,
          "gender" : "F",
          "address" : "334 River Street",
          "employer" : "Bezal",
          "email" : "burtonmeyers@bezal.com",
          "city" : "Jacksonburg",
          "state" : "MO"
        },
        "matched_queries" : [
          "lastname_1",
          "gender"
        ]
      }
    ]
  }
}
```

## Highlight the search term in the response of a query


- How to highlight when doing analyze searches

```
GET _search
{
  "highlight": {
    "pre_tags": [
      "<strong>"
      ],
      "post_tags": [
        "</strong>"
        ],
      "fields": {
       "text_entry": {}
     }
  }, 
  "query": {
    "match": {
      "text_entry": "life"
    }
  }
}
```

## Sorting results

```
GET bank/_search
{
  "sort": [
    {
      "account_number": {
        "order": "asc"
      }
    }
]
}

GET bank/_search
{
  "sort": [
    {
      "age": {
        "order": "desc"
      }
    },
    {
      "balance": {
        "order": "desc"
      }
    }
  ]
}

GET bank/_search
{
  "sort": [
    {
      "firstname.keyword": {
        "order": "asc"
      }
    }
  ]
}
```

## Implement pagination of the results of a search


- This is how to get 21 elements, then the size is the offset for your pages `GET bank/_search?size=21&from=21`

```
GET bank/_search
{
  "size": 20,
  "from": 20,
}
```

## Use scroll API to retrieve large numbers of results

- By default `GET _search` returns 10k results


```json
#this returns and the scroll_id
GET _search?scroll=10m&size=1000

GET _search/scroll
{
  "scroll": "10m",
  "scroll_id": "DnF1ZXJ5VGhlbkZldGNoDAAAAAAAAABQFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAURZETnkzQ1VHWlRUMjNwNUhzVmtOczR3AAAAAAAAAHsWcEhtTjVTeEFRMmVQcWNaU2RqeVEzZwAAAAAAAABTFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAehZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAHkWcEhtTjVTeEFRMmVQcWNaU2RqeVEzZwAAAAAAAAB8FnBIbU41U3hBUTJlUHFjWlNkanlRM2cAAAAAAAAAeBZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAFIWRE55M0NVR1pUVDIzcDVIc1ZrTnM0dwAAAAAAAABUFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAfRZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAFUWRE55M0NVR1pUVDIzcDVIc1ZrTnM0dw"
}
```

- You have open a scroll, so you need to delete a scroll. If a document gets updated, you don't get the most recent data.

```

DELETE _search/scroll
{
  "scroll_id": "DnF1ZXJ5VGhlbkZldGNoDAAAAAAAAABQFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAURZETnkzQ1VHWlRUMjNwNUhzVmtOczR3AAAAAAAAAHsWcEhtTjVTeEFRMmVQcWNaU2RqeVEzZwAAAAAAAABTFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAehZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAHkWcEhtTjVTeEFRMmVQcWNaU2RqeVEzZwAAAAAAAAB8FnBIbU41U3hBUTJlUHFjWlNkanlRM2cAAAAAAAAAeBZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAFIWRE55M0NVR1pUVDIzcDVIc1ZrTnM0dwAAAAAAAABUFkROeTNDVUdaVFQyM3A1SHNWa05zNHcAAAAAAAAAfRZwSG1ONVN4QVEyZVBxY1pTZGp5UTNnAAAAAAAAAFUWRE55M0NVR1pUVDIzcDVIc1ZrTnM0dw"
}
```


- By default while using scroll sorting of result docs are not consistent, better to specifically request the order.

```
GET _search?scroll=10m&size=1000
{
  "sort": [
    {
      "_doc": {
        "order": "asc"
      }
    }
  ]
}
```

- Close all the scrolls `DELETE _search/scroll/_all`

- Slide scroll allows to have to slides in parallel, you just need to change your "id". The max number of slides is indicated by `max`

```
GET _search?scroll=10m
{
  "slice": {
    "id": 1,
    "max": 2
  },
  "sort": [
    {
      "_doc": {
        "order": "asc"
      }
    }
  ]
}
```

## Apply fuzzy matching to a query

- This is useful when the user makes a typo and try to search.

```
GET _search
{
  "query": {
    "match": {
      "text_entry": {
        "query": "shae",
        "fuzziness": 1
      }
    }
  }
}
```

- Whe can sort, search and highlight with tolerance to missing characters.

```
GET _search
{
  "sort": [
    {
      "_score": {
        "order": "asc"
      }
    }
  ], 
  "highlight": {
    "pre_tags": ["**"],
    "post_tags": ["**"]
    , "fields": {
      "text_entry": {}
    }
  }, 
  "query": {
    "match": {
      "text_entry": {
        "query": "shame",
        "fuzziness": 1
      }
    }
  }
}
```


- We can have fuzziness with analyze queries.

```
GET _search?size=1
{
 "query": {
   "fuzzy": {
     "play_name": {
       "value": "The Tempets"
     }
   }
 }
}

GET _search?size=1
{
 "query": {
   "fuzzy": {
     "play_name": {
       "value": "The Tempets",
       "fuzziness": 1,
       "transposition": true
     }
   }
 }
}

```

## Define and use a search template

- Capture user's input


```


GET _search/template
{
  "source": {
    "query": {
      "bool": {
        "must": [
          {
            "wildcard": {
              "firstname.keyword": {
                "value":"{{first}}"
              }
            }
          }
          ]
      }
    }
  },
  "params": {
    "first": "*"
  }
}
```

- Now if we want to be able to search without the user specifying the input.
- We need to use delimiter and the wilcard. By adding `{{^first}}`, even if
  params is removed, you get hits.

```
GET _search/template
{
  "source": {
    "query": {
      "bool": {
        "must": [
          {
            "wildcard": {
              "firstname.keyword": {
                "value":"{{first}}{{^first}}*{{/first}}"
              }
            }
          },
          {
            "wildcard": {
              "lastname.keyword": {
                "value":"{{last}}{{^last}}*{{/last}}"
              }
            }
          }
          ]
      }
    }
  }
}

- 

```json
POST _scripts/account_lookup_by_name
{
  "script": {
    "lang": "mustache",
    "source": {
      "query": {
        "bool": {
          "must": [
            {
              "wildcard": {
                "firstname.keyword": {
                  "value": "{{first}}{{^first}}*{{/first}}"
                }
              }
            },
            {
              "wildcard": {
                "lastname.keyword": {
                  "value": "{{last}}{{^last}}*{{/last}}"
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

- Then we can use that template

```

GET _search/template
{
  "id": "account_lookup_by_name",
  "params": {
    "last": "Duke"
  }
}


## Write and execute a query that searches across multiple clusters


- Query below searches the same index in the current cluster and a remote one.
```
GET c2:bank,bank/_search
{
  "query": {
    "term": {
      "firstname.keyword": {
        "value": "Amber"
      }
    }
  }
}

```
