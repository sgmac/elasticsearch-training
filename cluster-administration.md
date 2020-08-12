# Cluster administration

- Creating indices 

```
PUT /sample-1
{
  "settings": {
    "number_of_replicas": 0,
    "number_of_shards": 2
  }
}
```

- To see the allocation of shards:

```
GET _cat/shards/sample-1?v

index    shard prirep state   docs store ip             node
sample-1 1     p      STARTED    0  230b 172.31.125.109 data-2
sample-1 0     p      STARTED    0  230b 172.31.117.146 data-1
```

- Routing to specific node. This will happen only if the cluster remains in "GREEN" state.

```
PUT sample-1/_settings
{
  "index.routing.allocation.exclude._name": "data-2"
}
```

- To reset the previous changes is to set the previous setting to "null"

```
PUT sample-1/_settings
{
     "index.routing.allocation.exclude._name": null
}

GET _cat/shards/sample-1?v
index    shard prirep state   docs store ip             node
sample-1 1     p      STARTED    0  283b 172.31.117.146 data-1
sample-1 0     p      STARTED    0  283b 172.31.125.109 data-2
```

- We can do routing in cluster-wide level. Prepare the cluster for a node for maintenace, to exclude that node. If `data-2` was going to be in maintenance and assuming does not break the GREEN state, we could do this at a cluster level.

```
GET _cat/shards/sample-1?v
index    shard prirep state   docs store ip             node
sample-1 1     p      STARTED    0  283b 172.31.117.146 data-2
sample-1 0     p      STARTED    0  283b 172.31.117.146 data-2


# Now we avoid using data-2
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._name": "data-2"
  }
}

```

- The above example works becuase we only have 2 primary andn 0 replicas.

## Example of having replicas 

```

PUT sample-1/_settings
{
 "index": {
   "number_of_replicas": 1
 }
}

GET _cat/shards/sample-1?v
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.exclude._name": "data-2"
  }
}

index    shard prirep state   docs store ip             node
sample-1 1     p      STARTED    0  283b 172.31.117.146 data-1
sample-1 1     r      STARTED    0  283b 172.31.125.109 data-2
sample-1 0     p      STARTED    0  283b 172.31.117.146 data-1
sample-1 0     r      STARTED    0  283b 172.31.125.109 data-2
```

- The above change wouldn't have effect because breaks the GREEN state as the primary and the replicas can't be in the same node.

## Configure shard allocation

- We need to create a custom attribute in this case `zone`, this may represent 2 different AZs or region. I don't want to have replica shards in the same zone, but in different one to have more HA.

```
GET _cat/nodeattrs

data-1   172.31.117.146 172.31.117.146 ml.machine_memory 1893593088
data-1   172.31.117.146 172.31.117.146 temp              hot
data-1   172.31.117.146 172.31.117.146 ml.max_open_jobs  20
data-1   172.31.117.146 172.31.117.146 xpack.installed   true
data-1   172.31.117.146 172.31.117.146 zone              1
data-2   172.31.125.109 172.31.125.109 ml.machine_memory 1893593088
data-2   172.31.125.109 172.31.125.109 temp              warm
data-2   172.31.125.109 172.31.125.109 ml.max_open_jobs  20
data-2   172.31.125.109 172.31.125.109 xpack.installed   true
data-2   172.31.125.109 172.31.125.109 zone              2
master-1 172.31.126.150 172.31.126.150 ml.machine_memory 1893593088
master-1 172.31.126.150 172.31.126.150 xpack.installed   true
master-1 172.31.126.150 172.31.126.150 zone              1
master-1 172.31.126.150 172.31.126.150 ml.max_open_jobs  20
```
-  We can enable this from the config file or from the API. This is a good example of using "persistent". This can have mutliple attributes. This is going to set `primary` in one zone and `replicas` in a different zone.

```
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone"
  }
}
```

- If we had only 2 zones and we lose 1 of those zones. Let's say we lose `zone2`, how do we know we have enough resources in `zone1` to reallocate and replicate all that data from `zone2`? In most cases we won't have enough space. There is a configuration to ensure we do not overwelmed  the last awareness attribute. In this situation, we will leave all the replica shards `unassigned`. 

```
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.awareness.attributes": "zone",
    "cluster.routing.allocation.awareness.force.zone.values": "1,2"
  }
}
```

- Basically all the replicas from the "zone2" that are lost, will remain lost, therefore "yellow".


# Diagnose shard issues and repair cluster's health


1. Check your `_cat/nodes` to see if there is one missing. 
2. Check your `_cat/indices` to see if there is something wrong.
3. Check your `_cat/shards/<INDEX_NAME>`
4. Use cluster API to diagnose `_cluster/allocation/explain`
 

```
PUT sample-1
{
  "settings": {
    "number_of_replicas": 0,
    "number_of_shards": 1,
    "index.routing.allocation.exclude._name": "data-1,data-2"
  }
}
GET _cluster/allocation/explain
{
  "index" : "sample-1",
  "shard" : 0,
  "primary" : true,
  "current_state" : "unassigned",
  "unassigned_info" : {
    "reason" : "INDEX_CREATED",
    "at" : "2020-08-12T15:29:16.202Z",
    "last_allocation_status" : "no"
  },
  "can_allocate" : "no",
  "allocate_explanation" : "cannot allocate because allocation is not permitted to any of the nodes",
  "node_allocation_decisions" : [
    {
      "node_id" : "pHmN5SxAQ2ePqcZSdjyQ3g",
      "node_name" : "data-1",
      "transport_address" : "172.31.117.146:9300",
      "node_attributes" : {
        "ml.machine_memory" : "1893593088",
        "temp" : "hot",
        "ml.max_open_jobs" : "20",
        "xpack.installed" : "true",
        "zone" : "1"
      },
      "node_decision" : "no",
      "weight_ranking" : 1,
      "deciders" : [
        {
          "decider" : "filter",
          "decision" : "NO",
          "explanation" : """node matches index setting [index.routing.allocation.exclude.] filters [_name:"data-1 OR data-2"]"""
        }
      ]
    },
    {
      "node_id" : "DNy3CUGZTT23p5HsVkNs4w",
      "node_name" : "data-2",
      "transport_address" : "172.31.125.109:9300",
      "node_attributes" : {
        "ml.machine_memory" : "1893593088",
        "temp" : "warm",
        "ml.max_open_jobs" : "20",
        "xpack.installed" : "true",
        "zone" : "2"
      },
      "node_decision" : "no",
      "weight_ranking" : 2,
      "deciders" : [
        {
          "decider" : "filter",
          "decision" : "NO",
          "explanation" : """node matches cluster setting [cluster.routing.allocation.exclude] filters [_name:"data-2"]"""
        }
      ]
    }
  ]
}
```


**IMPORTANT**: Check if you have transient or persistent changes. Do not forget to check also the settings on a given index.

```
GET _cluster/settings

PUT sample-1/_settings                                             
{  
  "index.routing.allocation.exclude._name": "data-2"
}

GET sample-1/_settings                                             
{
  "sample-1" : {
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "exclude" : {
              "_name" : "data-2"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "sample-1",
        "creation_date" : "1597246156187",
        "number_of_replicas" : "2",
        "uuid" : "-IMbL80fQ_iEAib8RPEirA",
        "version" : {
          "created" : "7020199"
        }
      }
    }
  }
```


