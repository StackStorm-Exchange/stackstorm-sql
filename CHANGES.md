# Change Log

## 1.2.0

* Fixed internal working of the query action compatible with sqlalchemy 2.0+
* Replaced row_to_dict tuple keys loop with sqlalchemy todict function

## 1.1.1

* Resolve issue where query is sometimes missing

## 1.1.0

* Update psycopg2 to 2.8 to support python 3.8

## 1.0.0

* Drop Python 2.7 support

## 0.1.3

- Pinned cx_Oracle<=7.3.0. Addresses #9

## 0.1.2

- Fixed issue with generic query where connection was being closed before query results were returned.
  Contributed by Bradley Bishop (Encore Technologies)

## v0.1.1

* Pack bump to update files from master to a tagged release.

## v0.1.0

* Initial Revision
