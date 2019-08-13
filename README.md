# data-infra-notes

Notes I jot about articles, books, and other resources related to data infrastructure.
Inspired by: http://xyz.insightdataengineering.com/blog/pipeline_map/


## File SYS:

### Amazon S3

#### S3 Storage classes:
- general purpose
- infrequent access
- archive

Lifecycle policies can migrate b/w storage classes
	-> no application code needed to change

S3 is not block storage nor file storage. 
e.g. you can’t remote mount on S3 because it’s not a file system

- no capacity planning needed is needed
- only 100 buckets per account by default
- objects can be upto 5TB
- S3 is agonistic of filetypes: everything is a stream of bytes in eyes of S3
- http://bucket/key 

S3 operations:
- create/delete a bucket
- write an object
- read an object
- delete an object
	- MFA can be enabled for this by root user
- list keys in a bucket
	- supports prefixes and delimiters
	
S3 has 99.999999999% durability and 99.99% availability
S3 is eventually consistent 
S3 operations are atomic 

Access Control lists (ACL):
- allows fine-grained access controls (READ, WRITE, FULL-CONTROL)
	
Static web hosting with S3:
1. Bucket with same name as desired website hostname
2. Upload static files to bucket
3. Make all files public
4. Enable static hosting for bucket
5. <bucket-name>.s3-website-<AWS-region>.amazonaws.com.com
6. Create a DNS with Route 53
	
AWS KMS uses 256-bit encryption on S3

S3 objects are private by default (accessible only to the owner).

Encryption options:
* S3 (SSE-S3)
	* Each object is encrypted with a key. Amazon encrypts the key with a master key, which rotates regularly.
* AWS Key Management Service (SSE-KMS)
	* Allows you to audit trail (who and when used the key), extra cost and you manage the master key.
* Customer provided (SSE-C)
	* User manages the keys but encryption done by Amazon
	
Specifying **version ID** allows for versioning.

Multipart upload:
- Stages:   init -> upload -> completion (abort)
- great for network utilization
- can pause/resume

Range GETs: allows you to specify range of bytes of object
	-> good for getting first N bytes

Cross-region replication allows async replication of new objects

S3 can have server access logs enabled
S3 can send event notifications on the bucket level

#### S3 performance:
- avg of max ~100 reqs per second
- higher throughput achieved by using hash as prefix and random key distribution


### AWS Glacier
- for “cold data”; much cheaper but expected retrieval time 3-5 hours
- Data is stored in **archives** (upto 40TB of data) contains inside **vaults**


## Data Ingestion:

### Filebeat:
https://www.elastic.co/products/beats/filebeat

- aggregated "tail -f" as a service.
- automatically rate-limits itself. if Logstash is busy crunching data, file beat slows down its read until congestion is resolved.
- cannot send Filebeat output to AWS SQS

- [Filebeat directly to ElasticSearch without Logstash](https://aws.amazon.com/blogs/database/ek-is-the-new-elk-simplify-log-analytics-by-transforming-data-natively-in-amazon-elasticsearch-service/)

### Logstash:
- Transformer: E[T]L
- requires JVM


#### Deserialization:
- codecs can be used to deserialize data into Logstash events: https://www.elastic.co/guide/en/logstash/current/data-deserialization.html
e.g. avro, csv, xml, protobuf

**con**: for protobuf codec, requires the protobuf definitions to be compiled as Ruby file.


## Batch Processing:

## Stream Processing:

### Kafka:
"distributed commit log" and "distribtued streaming platform".

#### Kafka terms:

**Message**: 
- unit of data within Kafka
- analogous to a row in a database
- Type: byte array

**Key**:
- Optional metadata 
- used when messages are to be written to paritions in a more controlled manner
- Type: byte array


**Batch**:
- Collection of messages with same topic and partition
- Messages are written into Kafka in batches
- Typically compressed more more efficient data transfer


Kafka developers favor Apache Avro serialization:
- orginally developed for Hadoop


**Topic**:
- has multiple partitions
- analogous to a table in a database

**Partition**:
- provides redudancy and scalability
- messages are written to a partition in a append-only fashion
- each partition can be hosted on a different server. Single topic can horizontally scale across multiple servers.


**Producers**:
- create new messages to a topic
- producer can direct messages to specific partitions using message key and partitioner hashing the key and mapping the result of the hash.


**Consumers**:
- reads new messages from a topic
- keeps track of which messages it has already consumed using an offset.
- offset <int> is a counter that Kafka increments as message is produced.  Each message has a unique offset. offset allows consumer to stop/restart w/o losing its place. 
- work as part of **consumer group**, one or more consumers that work together for a topic. 
- Consumer group allows consumers to horizontally scale.

**Broker**:
- a single Kafka server
- a single broker cacn easily handle thousands of paritions and millions of messages per second

Broker steps:
- receives messages from producers
- assigns offsets
- commits messages to storage on disk
- services consumers: respond to fetch requests for paritions


**Kafka Cluster**:
- group of Kafka brokers
- one broker functions as **cluster controller** and is responsible for: assigning partitions to brokers and monitoring for broker failures.


**Kafka retention**:
- durable storage of message 
- can set a limit for time (10 days) and size (e.g. 1TB)
- once limit is reached, messages expire and are deleted


#### Kafka Reliability Gaurantees
- order guarentee: if message B was written after message A, consumers read message B after message A.
- produced messages are "committed" when written to the partion on all in-sync replicas.
- messages that are committed will not be lost as long as at least one replica remains alive
- consumers cacn only read messages that are committed


##### Replication:

a replica is in-sync if it is the leader for a partition or follower that:
- has an active sesion with Zookeeper
- Feteched messages from the leader in the last 10 seconds (configurable)
- fetched most recent messages from the leader in the last 10 seconds. 

If a replica loses connection to Zookeepr, stops fetching new messages, or falls behind and can't catch up within 10 seconds, the replica is out-of-sync.

- can set `default.replication.factor`, default value is 3. 3 is usually enough; some banks are known to run critical topics with 5 replicas.


When leader for a partition is no longer available, one of the in-sync replicas is chosen as the new leader.
- no loss of comitted data occurs during this leader selection.






#### Running Kakfka on AWS:

[Best practices for running Kafka on AWS](https://aws.amazon.com/blogs/big-data/best-practices-for-running-apache-kafka-on-aws/)




### Lambda:



## Data Store:

### Postgres:


Monitor running queries:
```SQL
SELECT 
	pid, 
	age(clock_timestamp(), query_start), 
	usename, 
	query, 
	state
FROM pg_stat_activity
WHERE state not like 'idle%' AND  query NOT ILIKE '%pg_stat_activity%'
ORDER BY query_start desc;
```

Cancel a running query:
```SQL
SELECT pg_cancel_backend(pid); -- pid is INT
```


### AWS Redshift:


### ElasticSearch:



## Workflow:


### Airflow:

**airflow trigger_dag execution_date is the next day**:
https://stackoverflow.com/questions/39612488/airflow-trigger-dag-execution-date-is-the-next-day-why

tl;dr because that's how cron-like schedulers are implemented.

#### Sensors:

### AWS Data Pipeline:
- a great starting point for small data engineering teams running on AWS stack

in my personal experience, a much worse Apache Airflow :) (at scale!)


---

## Glossary of Acronyms I use:
- SYS: System


### Other notes:

I work with the following stacks:
- AWS (platform)
- AWS RDS (database)
- gRPC
- protocol buffers



