# Installing master

This can be followed [here](https://www.elastic.co/guide/en/elasticsearch/reference/master/setup.html).


- Add user `elastic`
- Add entry below /etc/security/limits.conf

```
elastic - nofile 65536
```
- Edit /etc/sysctl.conf
```
vm.max_map_count= 262144
```

- To load  `sysctl -p`


## Configuration

This is only to list the elegible master nodes.
```
discovery.seed_hosts: ["host1", "host2"]
```

Network host

```
cluster.name: c1
node.name: master-1
node.attr.zone: 1
network.host: [_local_, _site_]
cluster.initial_master_nodes: ["master-1"]

node.master: true
node.data: false
node.ingest: false

xpack.security.enabled: true
xpack.security.transport.ssl.enabled: true
xpack.security.transport.ssl.verification_mode: certificate
xpack.security.transport.ssl.keystore.path: certs/master-1
xpack.security.transport.ssl.truststore.path: certs/master-1
```

- Once you have the previous configuration, a password for the services needs to be set `./elasticsearch/bin/elasticsearch-setup-passwords  interactive`. Then modify the configuration to accept SSL connections, restart Elastic search.

```
xpack.security.http.ssl.enabled: true
xpack.security.http.ssl.keystore.path: certs/master-1
xpack.security.http.ssl.truststore.path: certs/master-1

```

- At this point you should be able to do `curl -k -u elastic https://localhost:9200`


## Kibana


```
server.port: 80

server.host: "172.31.126.150"
server.name: "kibana"
elasticsearch.hosts: ["https://localhost:9200"]
elasticsearch.username: "elastic"
elasticsearch.password: "elastic"
elasticsearch.ssl.verificationMode: none
```


## Security


## Create certificates

```
/home/elastic/elasticsearch/bin/elasticsearch-certutil  cert --ca config/certs/ca --ca-pass elastic_la --name master-1 --out config/certs/master-1 --pass elastic_la
/home/elastic/elasticsearch/bin/elasticsearch-certutil  cert --ca config/certs/ca --ca-pass elastic_la --name data-1 --out config/certs/data-1 --pass elastic_la
/home/elastic/elasticsearch/bin/elasticsearch-certutil  cert --ca config/certs/ca --ca-pass elastic_la --name data-2 --out config/certs/data-2 --pass elastic_la
/home/elastic/elasticsearch/bin/elasticsearch-certutil  cert --ca config/certs/ca --ca-pass elastic_la --name data-2 --out config/certs/node-1  --pass elastic_la
/home/elastic/elasticsearch/bin/elasticsearch-certutil  cert --ca config/certs/ca --ca-pass elastic_la --name d node-1 --out config/certs/node-1  --pass elastic_la
cd certs/
```


## Set password 

```
elasticsearch/bin/elasticsearch-keystore  add xpack.security.transport.ssl.keystore.secure_password
elasticsearch/bin/elasticsearch-keystore  add xpack.security.transport.ssl.truststore.secure_password
elasticsearch/bin/elasticsearch-keystore  add xpack.security.http.ssl.keystore.secure_password
elasticsearch/bin/elasticsearch-keystore  add xpack.security.http.ssl.truststore.secure_password
```


# Roles and users

- Below is an exmaple to create or update a role, is the same.
```
POST _security/role/sample
{
  "indices": [
    {
      "names": ["sample-*"],
      "privileges": ["read", "write", "delete"]
    }
  ]
}
POST _security/user/sgm
{
  "roles": ["superuser"]
}

GET _security/role/sample
GET _security/user/sgm
```

