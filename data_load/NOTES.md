# Examples of exercises

The movies dataset is a good example to practice aggregations or queries. The test elasticsearch environment runs 3 instances and 1 kibana in Docker containers. This is set to 3 shards and 2 replicas at the moment, this is the max you can get.


#### How many unique films where published per year? Get the output sorted

This is an aggregation use case. When using "year" we imply is text field. In case it fails
you can verify checking the mappings for that index `GET movies/_mappings`
```
GET movies/_search
{
 "size": 0,
 "aggs": {
   "unique_films_per_year": {
     "terms": {
       "field": "year"
     }
     
   }
 },
 "sort": [
   {
     "year": {
       "order": "asc"
     }
   }
 ]
}
```

#### How many movies are per genre? What about actors in movies?

Using an aggregation we can answer this question. Replace agg with `cast.keyword`.

```
GET movies/_search?size=0
{
 "aggs": {
   "movies_genre": {
     "terms": {
       "field": "genres.keyword",
       "size": 10
     }
   }
 }
}
```
