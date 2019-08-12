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

These notes can be biased since I work with the following stack:
- AWS (platform)
- AWS RDS (database)
- gRPC
- protocol buffers



