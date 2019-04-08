[![Build Status](https://circleci.com/gh/StackStorm-Exchange/stackstorm-sql.svg?style=shield&circle-token=:circle-token)](https://circleci.com/gh/StackStorm-Exchange/stackstorm-sql) [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# SQL Integration Pack
Query, Insert, Update, and Delete information from PostgreSQL, MsSQL, MySQL, Oracle, Firebird Databases. Additional databases can be added by installing the pre-requisite packes and passing the driver name as documented at [SQLAlchemy Dialects Doc](https://docs.sqlalchemy.org/en/latest/dialects/index.html).

## Quick Start

1. Install the pack

    ``` shell
    st2 pack install sql
    ```

2. Execute an action (example: query)

    ``` shell
    st2 run sql.query host=test_serve.domain.tld username=test_user password=test_password database=test_database drivername=postgresql query="select * from test;"
    ```

## Included Drivers
This pack is already set up to connect to the databases listed above. Additional databases can be connected to but pre-requisite packages will need to be installed before the drivers will work. [SQLAlchemy Dialects Doc](https://docs.sqlalchemy.org/en/latest/dialects/index.html).

You can pass any of the following driver names without any additional packages needing installed:
* `postgresql` - PostgreSQL databases
* `mssql` - Microsoft SQL Server databases
* `mysql` - MySQL/MariaDB databases
* `oracle` - Oracle databases
* `firebird` - Firebird databases


## Configuration and Connecting to Databases
Connecting to different types of databases is shown below. Connecting to different databases is done in the same manner except with sqlite where all you need to pass is the path to the database in the database option. This is shown below. For more information about connections please refer to [SQLAlchemy Connection Docs](https://docs.sqlalchemy.org/en/latest/core/engines.html)

Copy the example configuration in [sql.yaml.example](./sql.yaml.example)
to `/opt/stackstorm/configs/sql.yaml` and edit as required.

It can contain an array of one or more sets of SQL connection parameters, like this:

``` yaml
---
connections:
  postgresql:
    host: postgresql_db.domain.tld
    username: stackstorm_svc@domain.tld
    password: Password
    database: TestDatabase
    port: 5432
    drivername: postgresql
  mysql:
    host: mysql_db.domain.tld
    username: stackstorm@domain.tld
    password: NewPassword
    database: TestDatabase
    drivername: mysql
  sqlite:
    database: /path/to/db.sqlite
    drivername: sqlite
```

Each entry should contain:

* `host` - Database hostname
* `username` - Username to authenticate to DB
* `password` - Password for DB authentication
* `database` - Database to use
* `port` - Port to connect to database on. If Default leave blank
* `drivername` - The type of database that is being connected to.

When running actions, you can pass in the name of a connection, e.g.

``` shell
st2 run sql.query connection="postgresql" query="SELECT * FROM test;"
```

Alternatively, when running an action, you can pass in the host, username, password, database, port, drivername parameters. These parameters can also be used for overrides if you wish to use the configs as well.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please remember to tell StackStorm to load these new values by running `st2ctl reload --register-configs`

# Usage

## Actions

| Action | Description |
|--------|-------------|
| query | Generic query action to get inforamtion from the database. |
| insert | Insert data into a database table. Insert data is passed as an object. |
| insert_bulk | Bulk insert data into a database table. Insert data is passed as an array of objects. |
| update | Update data in a database table. |
| delete | Delete data from a database table. |

### Action Example - sql.query

`sql.query` can run any SQL query against a database. This can be used for simple `SELECT` 
statements:

```shell
st2 run sql.query connection="postgresql" query="SELECT * FROM test;"
```

Workflow usage:

``` yaml
insert_data:
  action: sql.query
  input:
    connection: postgresql
    query: "SELECT * FROM test;"
```

This action is also the one to use if you have a complex SQL statement that you want to run,
but there isn't another action in this pack that supports what you're trying to do.
In this case, simply pass in your arbitrary SQL statement into the `query` parameter and
it will be executed:

```shell
st2 run sql.query connection="postgresql" query="SELECT * FROM test JOIN somecrazytable ON id;"
```

### Action Example - sql.insert

`sql.insert` is used to insert a single record into a table:

```shell
st2 run sql.insert connection="postgresql" table="people" data='{"name": "bob", "phone": "1234567890"}'
```

Workflow usage:

``` yaml
insert_data:
  action: sql.insert
  input:
    connection: postgresql
    table: "people"
    data:
      name: "bob"
      phone: "1234567890"
```

### Action Example - sql.insert_bulk

`sql.insert_bulk` is used to insert multiple records into a table. In this case the `data` 
parameter expects an array of objects, where each object is a record to insert.

```shell
st2 run sql.insert connection="postgresql" table="people" data='[{"name": "bob", "phone": "1234567890"}, {"name": "alice", "phone": "0987654321"}]'
```

Workflow usage:

``` yaml
bulk_insert_data:
  action: sql.insert_bulk
  input:
    connection: postgresql
    table: "people"
    data:
      - name: "bob"
        phone: "1234567890"
      - name: "alice"
        phone: "0987654321"
```

### Action Example - sql.update

`sql.update` is used to update records in a table using simple `WHERE` clauses. 
If you need to run complex `WHERE` conditions, then use the `sql.query` action instead.

```shell
st2 run sql.insert connection="postgresql" table="people" where='{"name": "bob"}' update='{"phone": "5551234"}'
```

Workflow usage:

``` yaml
update_data:
  action: sql.update
  input:
    connection: postgresql
    table: "people"
    where:
      name: "bob"
    update:
      phone: "5551234"
```

### Action Example - sql.delete

`sql.delete` is used to delete records in a table using simple `WHERE` clauses. 
If you need to run complex `WHERE` conditions, then use the `sql.query` action instead.

```shell
st2 run sql.insert connection="postgresql" table="people" where='{"name": "bob"}'
```

Workflow usage:

``` yaml
update_data:
  action: sql.update
  input:
    connection: postgresql
    table: "people"
    where:
      name: "bob"
```

## Where statements

The Update and Delete actions give the option to include where data into the query. This only works for AND statements.

Example (YAML for workflows):
```yaml
where:
  column_1: "value_1"
  column_2: "value_2"
```

Example (JSON for `st2` CLI):
```shell
where='{"column_1": "value_1", "column_2": "value_2"}'
```

Produces the SQL `WHERE` statement:

```sql
WHERE column_1 == 'value_1' AND column_2 == 'value_2'
```

For more complicated queries please use the `sql.query` action.
