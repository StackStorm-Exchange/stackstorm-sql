from st2common.runners.base_action import Action
import sqlalchemy
from sqlalchemy.engine.url import URL
import decimal
import datetime
from contextlib import contextmanager

#                         (key, required, default)
CONFIG_CONNECTION_KEYS = [('host', False, ""),
                          ('username', False, ""),
                          ('password', False, ""),
                          ('database', True, ""),
                          ('port', False, None),
                          ('drivername', True, "")]

DEFAULT_KNOWN_DRIVER_CONNECTORS = {
    'postgresql': 'postgresql+psycopg2',
    'mysql': 'mysql+pymysql',
    'oracle': 'oracle+cx_oracle',
    'mssql': 'mssql+pymssql',
    'firebird': 'firebird+fdb'
}


class BaseAction(Action):
    def __init__(self, config):
        """Creates a new BaseAction given a StackStorm config object (kwargs works too)
        :param config: StackStorm configuration object for the pack
        :returns: a new BaseAction
        """
        super(BaseAction, self).__init__(config)

    def get_del_arg(self, key, kwargs_dict, delete=False):
        """Attempts to retrieve an argument from kwargs with key.
        If the key is found, then delete it from the dict.
        :param key: the key of the argument to retrieve from kwargs
        :returns: The value of key in kwargs, if it exists, otherwise None
        """
        if key in kwargs_dict:
            value = kwargs_dict[key]
            if delete:
                del kwargs_dict[key]
            return value
        else:
            return None

    def merge_dicts(self, dicts):
        """ Merge Array of dictionaries into 1 single Dictionary
        and return.
        """
        result = {}
        for d in dicts:
            if d:
                result.update(d)
        return result

    def row_to_dict(self, row):
        """When SQLAlchemy returns information from a query the rows are
        tuples and have some data types that need to be converted before
        being returned.
        returns: dictionary of values
        """
        return_dict = {}
        for column in row.keys():
            value = getattr(row, column)

            if isinstance(value, datetime.date):
                return_dict[column] = value.isoformat()
            elif isinstance(value, decimal.Decimal):
                return_dict[column] = float(value)
            else:
                return_dict[column] = value

        return return_dict

    def generate_where_clause(self, sql_table, sql_obj, where_dict):
        """Generate WHERE Clause for sql queries with the proper
        SQLAlchemy syntax and binding to the proper parameters with
        overrides.
        Returns Query object
        """
        return_dict = {}
        for key in where_dict.keys():
            value = where_dict[key]
            # All column names are reserved. Adding a '_' to the begging of the name
            new_key = "_" + key

            # Add WHERE statement to the update object
            sql_obj = sql_obj.where(sql_table.c.get(key) == sqlalchemy.sql.bindparam(new_key))

            # Add correct key and value to the new dictionary so it can be returned and
            # used in the query
            return_dict[new_key] = value

        return (sql_obj, return_dict)

    def generate_values(self, sql_obj, data_dict):
        """Generate values statement for sql queries with the proper
        SQLAlchemy syntax and binding to the proper parameters with
        overrides.
        Returns Query object
        """
        for key in data_dict.keys():
            key_dictionary = {key: sqlalchemy.sql.bindparam(key)}
            sql_obj = sql_obj.values(**key_dictionary)

        return sql_obj

    @contextmanager
    def db_connection(self, kwargs_dict):
        """Connect to the database and instantiate necessary methods to be used
        later.
        """
        # Get the connection details from either config or from action params
        connection = self.resolve_connection(kwargs_dict)

        # Update Driver with a connector
        default_driver = DEFAULT_KNOWN_DRIVER_CONNECTORS.get(connection['drivername'], None)
        if default_driver:
            connection['drivername'] = default_driver

        # Format the connection string
        database_connection_string = URL(**connection)

        self.engine = sqlalchemy.create_engine(database_connection_string, echo=False)
        self.meta = sqlalchemy.MetaData()
        conn = self.engine.connect()

        try:
            yield conn
        finally:
            conn.close()

    def validate_connection(self, connection, connection_name):
        """Ensures that all required parameters are in the connection. If a
        required parameter is missing a KeyError exception is raised.
        :param connection: connection to validate
        :returns: True if the connection is valid
        """
        for key, required, default in CONFIG_CONNECTION_KEYS:
            # ensure the key is present in the connection?
            if key in connection and connection[key]:
                continue

            # skip if this key is not required
            if not required:
                continue

            if connection_name:
                raise KeyError("config.yaml mising: sql:{0}:{1}"
                               .format(connection_name, key))
            else:
                raise KeyError("Because the 'connection' action parameter was"
                               " not specified, the following action parameter"
                               " is required: {0}".format(key))
        return True

    def resolve_connection(self, kwargs_dict):
        """Attempts to resolve the connection information by looking up information
        from action input parameters (highest priority) or from the config (fallback).
        :param kwargs_dict: dictionary of kwargs containing the action's input
        parameters
        :returns: a dictionary with the connection parameters (see: CONFIG_CONNECTION_KEYS)
        resolved.
        """
        connection_name = self.get_del_arg('connection', kwargs_dict, True)
        config_connection = None
        if connection_name:
            config_connection = self.config['connections'].get(connection_name)
            if not config_connection:
                raise KeyError("config.yaml missing connection: sql:{0}"
                               .format(connection_name))

        action_connection = {}

        # Override the keys in creds read in from the config given the
        # override parameters from the action itself
        # Example:
        #   'username' parameter on the action will override the username
        #   from the credential. This is useful for runnning the action
        #   standalone and/or from the commandline
        for key, required, default in CONFIG_CONNECTION_KEYS:
            if key in kwargs_dict and kwargs_dict[key]:
                # use params from cmdline first (override)
                action_connection[key] = self.get_del_arg(key, kwargs_dict)
            elif config_connection and key in config_connection and config_connection[key]:
                # fallback to creds in config
                action_connection[key] = config_connection[key]
            else:
                if not required and default:
                    action_connection[key] = default

            # remove the key from kwargs if it's still in there
            if key in kwargs_dict:
                del kwargs_dict[key]

        self.validate_connection(action_connection, connection_name)

        return action_connection
