# SQL Integration Pack
Query, Insert, Update, and Delete information from PostgreSQL, SQLite, MsSQL, MySQL, Oracle, Firebird, and Sybase Databases

## Pre-Requisites
This pack is set up to provide funcationality for the above databases. For MySQL and MsSQL we need to install 2 system packages.

#### MySQL
``` shell
yum install mysql-devel
```

#### MsSQL
https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017
``` shell
curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo
yum install msodbcsql17
yum install unixODBC-devel
```

## Quick Start

1. Install the pack

    ``` shell
    st2 pack install sql
    ```

2. Execute an action (example: query)

    ``` shell
    st2 run sql.query host=test_serve.domain.tld username=test_user password=test_password database=test_database database_type=postgresql query="select * from test;"
    ```

## Configuration
Copy the example configuration in [sql.yaml.example](./sql.yaml.example)
to `/opt/stackstorm/configs/sql.yaml` and edit as required.

It can contain an array of one or more sets of SQL connection parameters, like this:

``` yaml
---
sql:
  postgresql:
    host: postgresql_db.domain.tld
    username: stackstorm_svc@domain.tld
    password: Password
    database: TestDatabase
    database_type: postgresql
  mysql:
    host: mysql_db.domain.tld
    username: stackstorm@domain.tld
    password: NewPassword
    database: TestDatabase
    database_type: mysql
```

Each entry should contain

* ``host`` - Database hostname
* ``username`` - Username to authenticate to DB
* ``password`` - Password for DB authentication
* ``database`` - Database to use
* ``database_type`` - The type of database that is being connected to.

When running actions, you can pass in the name of a connection, e.g.
`st2 run sql.query connection="postgresql" query="select * from test;"`

Alternatively, when running an action, you can pass in the host, username, password, database, database_type parameters. These parameters can also be used for overrides if you wish to use the configs as well.

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please remember to tell StackStorm to load these new values by running `st2ctl reload --register-configs`

# Actions

| Action | Description |
|--------|-------------|
| query | Generic query action to get inforamtion from the database. |
| insert | Insert data into a database table. Insert data is passed as an object. |
| insert_bulk | Bulk insert data into a database table. Insert data is passed as an array of objects. |
| update | Update data in a database table. |
| delete | Delete data from a database table. |
