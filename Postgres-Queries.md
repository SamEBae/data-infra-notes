## Postgres Queries

### Postgres Activity
Queries for process operations.

##### Monitor running queries:

```SQL
SELECT 
	pid, 
	age(clock_timestamp(), query_start), 
	usename, 
	query, 
	state
FROM pg_stat_activity
WHERE state NOT LIKE 'idle%' AND query NOT ILIKE '%pg_stat_activity%'
ORDER BY query_start desc;
```

##### Cancel a running query (soft cancel):

```SQL
SELECT pg_cancel_backend(pid); -- pid (process id)
```

##### Cancel a running query (hard cancel)

usually have to run this when idle deadlock.

```SQL
SELECT pg_terminate_backend(pid); -- pid (process id)
```

### Postgres Vacuum


### Postgres Permissions

Create a schema and grant it on a user/role (but ensures you're the owner so you can delete it after) so they can do anything on it (e.g. CREATE/DELETE/ALTER TABLE etc.)

```SQL 
CREATE SCHEMA <schema name>;
GRANT ALL PRIVILEGES ON SCHEMA <schema name> TO <user/role>;
```
